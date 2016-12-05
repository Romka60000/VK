from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QTextEdit, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize
import vk
from Button import Button
from VKAPI import VKAPI

class MainWindow(QWidget):
    def __init__(self, VKAPI):
        super(MainWindow, self).__init__()
        self.setMinimumSize(900, 580)
        self.setWindowTitle("VK Standalone")
        self.setWindowIcon(QIcon("pics/TitleIcon.png"))
        self.setStyleSheet("background-color: rgb(210,210,255);")
        self.__vkapi = VKAPI

        self.__dialog_list_widget = QListWidget()
        self.__dialog_list_widget.setStyleSheet("background-color: white;")
        self.__dialog_list_widget.verticalScrollBar().setStyleSheet("QScrollBar::handle:vertical {" +
                                                                    "background: rgb(210,210,255); }" +
                                                                    "QScrollBar:vertical { background: white; }")
        self.__dialog_list_widget.setFixedWidth(300)

        self.__messages_list_widget = QListWidget()
        self.__messages_list_widget.setStyleSheet("background-color: white")

        self.__send_message_btn = Button("Send")
        self.__send_message_btn.setFixedSize(80,50)

        self.__edit_new_message = QTextEdit()
        self.__edit_new_message.setStyleSheet("background-color: white")
        self.__edit_new_message.setFixedHeight(50)

        self.__hbox1 = QHBoxLayout()
        self.__hbox1.addWidget(self.__edit_new_message)
        self.__hbox1.addWidget(self.__send_message_btn)

        self.__vbox1 = QVBoxLayout()
        self.__vbox1.addWidget(self.__dialog_list_widget)

        self.__vbox2 = QVBoxLayout()
        self.__vbox2.setAlignment(Qt.AlignBottom)
        self.__vbox2.setSpacing(10)
        self.__vbox2.addWidget((self.__messages_list_widget))
        self.__vbox2.addItem(self.__hbox1)

        self.__hbox = QHBoxLayout()
        self.__hbox.addItem(self.__vbox1)
        self.__hbox.addItem(self.__vbox2)

        self.setLayout(self.__hbox)

    def loginSuccess(self):
        self.show()

        for i in self.__vkapi.getMessagesList():
            item = QListWidgetItem()
            self.__dialog_list_widget.addItem(item)
            self.__dialog_list_widget.setItemWidget(item, i)

        for i in range(self.__dialog_list_widget.count()):
            self.__dialog_list_widget.item(i).setSizeHint(QSize(20, 50))
