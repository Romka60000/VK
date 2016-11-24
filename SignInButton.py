
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, pyqtSignal

class SignInButton(QLabel):

    mouse_clicked = False
    clicked = pyqtSignal()

    def __init__(self, message):
        super(SignInButton, self).__init__()
        self.setText(message)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Arial", 15))
        self.setStyleSheet("background-color: rgb(153, 169, 255); border-radius: 3px; margin-left: 14px; margin-right: 14px;")


    def enterEvent(self, *args, **kwargs):
        self.setStyleSheet("background-color: rgb(127,144,220); border-radius: 3px; margin-left: 14px; margin-right: 14px;")

    def leaveEvent(self, *args, **kwargs):
        self.setStyleSheet("background-color: rgb(153, 169, 255); border-radius: 3px; margin-left: 14px; margin-right: 14px;")

    def mousePressEvent(self, QMouseEvent):
        self.clicked.emit()