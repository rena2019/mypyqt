# install packages
#   python3 --m pip install pysimplegui
# build EXE
#   pyinstaller --noconsole --windowed --noconfirm --onefile --hidden-import "cryptography" D:\_projects\_my\mycrypto.py

# crypto stuff taken from https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
# import PySimpleGUI as sg
import secrets, cryptography
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
iterations = 100_000

def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))

def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)

# Define the window's contents
# layout = [[sg.Text("Message:")],
#           [sg.Input(key='message')],
#           [sg.Text("Password:")],
#           [sg.Input(key='pwd', password_char='*')],
#           [sg.Button('Encrypt'), sg.Button('Decrypt')],
#           [sg.Multiline(size=(40,3), key='-OUTPUT-')],
#           [sg.Button('Quit')]]

# # Create the window
# window = sg.Window('MyCrypto', layout)

# # Display and interact with the Window using an Event Loop
# while True:
#     event, values = window.read()
#     # See if user wants to quit or window was closed
#     if event == sg.WINDOW_CLOSED or event == 'Quit':
#         break
#     if event == 'Encrypt':
#         window['-OUTPUT-'].update(password_encrypt(bytes(values['message'], "utf-8"), values['pwd'], 10).decode())
#     elif event == 'Decrypt':
#         window['-OUTPUT-'].update(password_decrypt(bytes(values['message'], "utf-8"), values['pwd']).decode())

#     # Output a message to the window
    
#     #window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

# # Finish up by removing from the screen
# window.close()

import wx

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='MyCrypto')
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        #message
        sizer_message = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(panel, -1, 'Message:')
        self.text_message = wx.TextCtrl(panel)
        sizer_message.Add(label, 0, wx.ALL, 5)
        sizer_message.Add(self.text_message, 0, wx.ALL|wx.EXPAND, 5)
        my_sizer.Add(sizer_message, flag=wx.ALIGN_CENTER_HORIZONTAL)
        #password
        sizer_pwd = wx.BoxSizer(wx.HORIZONTAL)
        label_pwd = wx.StaticText(panel, -1, 'Password:', style= wx.TE_CENTER)   
        self.text_pwd = wx.TextCtrl(panel, -1, '', style=wx.TE_PASSWORD)
        sizer_pwd.Add(label_pwd, 0, wx.ALL, 5)
        sizer_pwd.Add(self.text_pwd, 0, wx.ALL|wx.EXPAND, 5)
        my_sizer.Add(sizer_pwd, flag=wx.ALIGN_CENTER_HORIZONTAL)
        #buttons     
        sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)   
        my_btn_encrypt = wx.Button(panel, label='Encrypt')
        my_btn_encrypt.Bind(wx.EVT_BUTTON, self.on_encrypt)
        my_btn_decrypt = wx.Button(panel, label='Decrypt')
        my_btn_decrypt.Bind(wx.EVT_BUTTON, self.on_decrypt)
        sizer_buttons.Add(my_btn_encrypt, 0, wx.ALL, 5)   
        sizer_buttons.Add(my_btn_decrypt, 0, wx.ALIGN_CENTRE, 5)
        my_sizer.Add(sizer_buttons,  flag=wx.ALIGN_CENTER_HORIZONTAL)
        #text output
        self.text_output = wx.TextCtrl(panel, style = wx.TE_MULTILINE)  
        my_sizer.Add(self.text_output, 0, wx.ALL | wx.EXPAND, 5)  
        
        panel.SetSizer(my_sizer) 
        my_sizer.Fit(self)       
        self.Show()

    def on_encrypt(self, event):
        value = self.text_message.GetValue()
        pwd = self.text_pwd.GetValue()
        self.text_output.SetValue(password_encrypt(bytes(value, "utf-8"), pwd, 10).decode())
    
    def on_decrypt(self, event):
        value = self.text_message.GetValue()
        pwd = self.text_pwd.GetValue()
        self.text_output.SetValue(password_decrypt(bytes(value, "utf-8"), pwd).decode())

def test_encrypt_decrypt():
    message= "hello world"
    pwd = "geheim"
    en = password_encrypt(bytes(message, "utf-8"), pwd, 10).decode()
    en = 'yqLcyeP7MkEXKtYwmZfqPAAAAAqAAAAAAGVx_KF5KdXzLkyeYlfYaASa56x5-j8AWnhcTmE41JKWDAY_eNVDms3W-UwssnaqtF0BEDHYsZlyokGkor8kbQISwBYN'
    txt = password_decrypt(en, pwd).decode()
    print(txt)

if __name__ == '__main__':
    #test_encrypt_decrypt()
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
