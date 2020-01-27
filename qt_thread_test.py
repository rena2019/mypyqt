# taken from
# when use QThread Debug PyQt app, breakpoint not work,while wing IDE can debug #176 https://github.com/Microsoft/vscode-python/issues/176
# QT5 Threads not captured in the debugger via VSCode #428 https://github.com/microsoft/ptvsd/issues/428

import time
import sys
import ptvsd

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel

class Worker(QObject):
    sig_msg = pyqtSignal(str)  # message to be shown to user

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def work(self):
        # necessary for using native thread APIs (such as the Win32 CreateThread function rather than the Python threading APIs) https://code.visualstudio.com/docs/python/debugging#_troubleshooting
        # 
        ptvsd.debug_this_thread()
        # breakpoint vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        self.sig_msg.emit('Hello from inside the thread!')

        result = 1 + 1
        result2 = 1 + 2


class MyWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Thread Example")

        form_layout = QVBoxLayout()

        self.setLayout(form_layout)
        self.resize(400, 200)

        self.button_start_threads = QPushButton("Start")
        self.button_start_threads.clicked.connect(self.start_threads)

        self.label = QLabel()

        form_layout.addWidget(self.label)
        form_layout.addWidget(self.button_start_threads)

        QThread.currentThread().setObjectName('main')

        self.__threads = None

    def start_threads(self):
        self.__threads = []

        worker = Worker()
        thread = QThread()
        thread.setObjectName('thread')
        self.__threads.append((thread, worker))  # need to store worker too otherwise will be gc'd
        worker.moveToThread(thread)

        worker.sig_msg.connect(self.label.setText)

        thread.started.connect(worker.work)
        thread.start() 


if __name__ == "__main__":
    app = QApplication([])

    form = MyWidget()
    form.show()

    sys.exit(app.exec_())
