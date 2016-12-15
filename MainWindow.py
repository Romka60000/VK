from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QTextEdit, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize, pyqtSignal
import emoji
# import vk
from Button import Button
# from VKAPI import VKAPI

class MainWindow(QWidget):

    def __init__(self, VKAPI):
        super(MainWindow, self).__init__()
        self.setMinimumSize(900, 580)
        self.setWindowTitle("VK Standalone")
        self.setWindowIcon(QIcon("pics/TitleIcon.png"))
        self.setStyleSheet("background-color: rgb(210,210,255);")
        self.__vkapi = VKAPI
        self.__old_dlg = None

        self.__dialogs_label = QLabel()
        self.__dialogs_label.setFont(QFont('Calibri', 14))
        self.__dialogs_label.setText('Dialogs')
        self.__dialogs_label.setStyleSheet('color: white')

        self.__messages_label = QLabel()
        self.__messages_label.setFont(QFont('Calibri', 14))
        self.__messages_label.setText('Messages')
        self.__messages_label.setStyleSheet('color: white')

        self.__dialog_list_widget = QListWidget()
        self.__dialog_list_widget.setStyleSheet("* { background-color: white; }")
        self.__dialog_list_widget.verticalScrollBar().setStyleSheet("QScrollBar::handle:vertical {" +
                                                                    "background: rgb(210,210,255); }" +
                                                                    "QScrollBar:vertical { background: white; }")

        self.__dialog_list_widget.setFixedWidth(300)
        self.__dialog_list_widget.itemPressed.connect(self.clickedDialog)

        self.__messages_list_widget = QListWidget()
        self.__messages_list_widget.setStyleSheet("background-color: white;")
        self.__messages_list_widget.verticalScrollBar().setStyleSheet("QScrollBar::handle:vertical {" +
                                                                    "background: rgb(210,210,255); }" +
                                                                    "QScrollBar:vertical { background: white; }")
        self.__messages_list_widget.horizontalScrollBar().setStyleSheet("QScrollBar::handle:horizontal {" +
                                                                        "background: rgb(210,210,255); }" +
                                                                    "QScrollBar:horizontal { background: white; }")


        self.__send_message_btn = Button("Send")
        self.__send_message_btn.setFixedSize(80,50)
        self.__send_message_btn.mouseClick.connect(self.sendMessage)

        self.__edit_new_message = QTextEdit()
        self.__edit_new_message.setStyleSheet("background-color: white")
        self.__edit_new_message.setFixedHeight(50)
        self.__edit_new_message.setFont(QFont('Sans-serif', 11))


        self.__hbox1 = QHBoxLayout()
        self.__hbox1.addWidget(self.__edit_new_message)
        self.__hbox1.addWidget(self.__send_message_btn)

        self.__vbox1 = QVBoxLayout()
        self.__vbox1.setSpacing(5)
        self.__vbox1.addWidget(self.__dialogs_label)
        self.__vbox1.addWidget(self.__dialog_list_widget)

        self.__vbox2 = QVBoxLayout()
        self.__vbox2.setAlignment(Qt.AlignBottom)
        self.__vbox2.setSpacing(5)
        self.__vbox2.addWidget(self.__messages_label)
        self.__vbox2.addWidget(self.__messages_list_widget)
        self.__vbox2.addItem(self.__hbox1)

        self.__hbox = QHBoxLayout()
        self.__hbox.addItem(self.__vbox1)
        self.__hbox.addItem(self.__vbox2)

        self.setLayout(self.__hbox)

    def loginSuccess(self):
        self.show()

        for i in self.__vkapi.getDialogsList():
            item = QListWidgetItem()
            item.setSizeHint(QSize(20, 60))
            self.__dialog_list_widget.addItem(item)
            self.__dialog_list_widget.setItemWidget(item, i)

    def clickedDialog(self):
        sender = self.sender()
        if self.__old_dlg is not None:
            self.__old_dlg.setStyleSheet("* { color: black; background-color: white; padding-left: 10px; }" +
                                "*:hover { background-color: rgb(220,220,250);} * { padding-left: 10px }")

        sender.itemWidget(sender.currentItem()).setStyleSheet("color: white; background-color: rgb(150,150,255);" +
                                                              "padding-left: 10px")
        self.__old_dlg = sender.itemWidget(sender.currentItem())
        self.__messages_list_widget.clear()

        for i in list(reversed(self.__vkapi.getMessagesList(sender.itemWidget(sender.currentItem()).peer_id))):
            item = QListWidgetItem()
            self.__messages_list_widget.addItem(item)
            item.setSizeHint(i.sizeHint())
            self.__messages_list_widget.setItemWidget(item, i)

    def sendMessage(self):
        try:
            self.__vkapi.sendMessage(self.__dialog_list_widget.itemWidget(
                self.__dialog_list_widget.currentItem()).peer_id, self.__edit_new_message.toPlainText())
            self.__edit_new_message.clear()

        finally:
            pass