from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt

class Button(QLabel):

    mouse_clicked = False

    def __init__(self, message, pic):
        super(Button, self).__init__()
        self.setText("<img src=" + pic + "><br>"+message)
        self.setFixedSize(150, 70)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Arial", 15))

    def enterEvent(self, *args, **kwargs):
        self.setStyleSheet("background-color: rgb(220,220,220); border-radius: 3px;")

    def leaveEvent(self, *args, **kwargs):
        self.setStyleSheet("background-color:;")