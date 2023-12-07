# install packages
#   python3 --m pip install pysimplegui
# create exe
#   pyinstaller --noconsole --windowed --noconfirm --onefile D:\_projects\_my\mycrypto.py

# crypto stuff taken from https://stackoverflow.com/questions/2490334/simple-way-to-encode-a-string-according-to-a-password
import secrets
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


import PySimpleGUI as sg

# Define the window's contents
layout = [[sg.Text("Message:")],
          [sg.Input(key='message')],
          [sg.Text("Password:")],
          [sg.Input(key='pwd', password_char='*')],
          [sg.Button('Encrypt'), sg.Button('Decrypt')],
          [sg.Multiline(size=(40,3), key='-OUTPUT-')],
          [sg.Button('Quit')]]

# Create the window
window = sg.Window('MyCrypto', layout)

# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break
    if event == 'Encrypt':
        window['-OUTPUT-'].update(password_encrypt(bytes(values['message'], "utf-8"), values['pwd'], 10).decode())
    elif event == 'Decrypt':
        window['-OUTPUT-'].update(password_decrypt(bytes(values['message'], "utf-8"), values['pwd']).decode())

    # Output a message to the window
    
    #window['-OUTPUT-'].update('Hello ' + values['-INPUT-'] + "! Thanks for trying PySimpleGUI")

# Finish up by removing from the screen
window.close()
