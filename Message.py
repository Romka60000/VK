from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class Message(QLabel):

    def __init__(self):
        super(QLabel, self).__init__()
        self.setFont(QFont('Sans-serif', 11))
        self.setStyleSheet('* :hover { background-color: rgb(220,220,250);} * { padding-left: 5px }')
        self.setWordWrap(True)
        self.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)