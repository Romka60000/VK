from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class MessageLabel(QLabel):

    def __init__(self, text, msg):
        super(MessageLabel, self).__init__()
        self.setFont(QFont('Sans-serif', 11))
        self.setStyleSheet('* :hover { background-color: rgb(220,220,250);} * { padding-left: 5px }')
        self.setText(text)

        if msg:
            self.setTextInteractionFlags(Qt.TextBrowserInteraction)
            self.setWordWrap(True)
            self.setOpenExternalLinks(True)

    def setStylePressed(self):
        self.setStyleSheet("color: white; background-color: rgb(150,150,255);" + "padding-left: 10px")

    def setStyleFree(self):
        self.setStyleSheet('* :hover { background-color: rgb(220,220,250);} * { padding-left: 5px }')