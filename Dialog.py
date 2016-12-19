from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QFont


class Dialog(QLabel):

    def __init__(self):
        super(Dialog, self).__init__()
        self.__peer_id = ''
        self.setStyleSheet('*:hover { background-color: rgb(220,220,250);} * { padding-left: 10px }')
        self.setFont(QFont('Sans-serif', 11))

    @property
    def peer_id(self):
        return self.__peer_id

    @peer_id.setter
    def peer_id(self, value):
        self.__peer_id = value
