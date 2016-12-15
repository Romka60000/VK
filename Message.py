from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont


class Message(QLabel):

    def __init__(self):
        super(QLabel, self).__init__()
        self.setFont(QFont('Sans-serif', 11))
        self.setStyleSheet('* :hover { background-color: gray;} * { padding-left: 5px }')
        self.setWordWrap(True)