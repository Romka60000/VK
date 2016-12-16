from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont
from PyQt5.Qt import pyqtSignal, Qt

class EditMessage(QTextEdit):
    enterPressed = pyqtSignal()

    def __init__(self):
        super(EditMessage, self).__init__()
        self.setStyleSheet("background-color: white")
        self.setFixedHeight(50)
        self.setFont(QFont('Sans-serif', 11))
        self.verticalScrollBar().setStyleSheet("QScrollBar::handle:vertical {background: rgb(210,210,255); }" +
                                                                    "QScrollBar:vertical { background: white; }")

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return) and Qt.ShiftModifier != event.modifiers():
            self.enterPressed.emit()
        else:
            super(EditMessage, self).keyPressEvent(event)
