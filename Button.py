from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont, QCursor
from PyQt5.QtCore import Qt, pyqtSignal

class Button(QLabel):

    mouseClick = pyqtSignal()

    def __init__(self, message):
        super(Button, self).__init__()
        self.setText(message)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(QFont("Arial", 15))
        self.setStyleSheet("background-color: white; border-radius: 3px; border: 1px solid black;")

    def enterEvent(self, *args, **kwargs):
        self.setStyleSheet("background-color: rgb(220,220,220); border-radius: 3px; border: 1px solid black;")
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def leaveEvent(self, *args, **kwargs):
        self.setStyleSheet("background-color: white; border-radius: 3px; border: 1px solid black;")

    def mousePressEvent(self, event):
        self.mouseClick.emit()

