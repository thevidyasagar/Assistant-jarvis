# ui/console.py

from PyQt6 import QtWidgets, QtCore, QtGui

class JarvisConsole(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis Console")
        self.resize(800, 500)
        self.setWindowFlags(
            QtCore.Qt.WindowType.Window |
            QtCore.Qt.WindowType.WindowStaysOnTopHint
        )

        layout = QtWidgets.QVBoxLayout(self)

        # log panel
        self.log = QtWidgets.QTextEdit(self)
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        # input box
        self.input = QtWidgets.QLineEdit(self)
        self.input.setPlaceholderText("Type a command or question...")
        layout.addWidget(self.input)

        self.input.returnPressed.connect(self.on_enter)

        self.on_command = None  # callback (main.py assigns)

    def on_enter(self):
        text = self.input.text().strip()
        if not text:
            return
        self.log.append("> " + text)
        self.input.clear()

        if self.on_command:
            reply = self.on_command(text)
            if reply:
                self.log.append(reply)

    def append(self, msg):
        self.log.append(msg)
