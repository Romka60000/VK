from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize
from EditMessage import EditMessage
from MessageLabel import MessageLabel
from time import sleep
from threading import Thread
from Button import Button


class MainWindow(QWidget):

    def __init__(self, VKAPI):
        super(MainWindow, self).__init__()
        self.setMinimumSize(900, 580)
        self.setWindowTitle("VK Standalone")
        self.setWindowIcon(QIcon("pics/TitleIcon.png"))
        self.setStyleSheet("background-color: rgb(210,210,255);")
        self.__vkapi = VKAPI
        self.__old_dlg = None

        # self.__dialogsList = []

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
        self.__dialog_list_widget.itemPressed.connect(self.dialogPressed)

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

        self.__edit_new_message = EditMessage()
        self.__edit_new_message.enterPressed.connect(self.sendMessage)

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
        self.hide()

    def loginSuccess(self):

        self.getDialogs()
        self.show()

    def dialogPressed(self):
        if self.__old_dlg is not None:
            self.__old_dlg.setStyleFree()
        self.__dialog_list_widget.itemWidget(self.__dialog_list_widget.currentItem()).setStylePressed()
        self.__old_dlg = self.__dialog_list_widget.itemWidget(self.__dialog_list_widget.currentItem())
        self.__messages_list_widget.clear()
        try:
            self.getMessagesFromDialog()
        except:
            sleep(1.5)
            self.getMessagesFromDialog()
        self.__messages_list_widget.scrollToBottom()

    def getDialogs(self):
        self.__dialog_list_widget.clear()
        for i in self.__vkapi.getDialogsList():
            shortLabel = MessageLabel(i.getShortText(), False, i.getPeerId())
            item = QListWidgetItem()
            item.setSizeHint(QSize(20, 60))
            self.__dialog_list_widget.addItem(item)
            self.__dialog_list_widget.setItemWidget(item, shortLabel)

    def getMessagesFromDialog(self):
        idx = self.__dialog_list_widget.itemWidget(self.__dialog_list_widget.currentItem()).peer_id
        for i in self.__vkapi.getMessagesList(idx):
            fullLabel = MessageLabel(i.getFullText(), True, i.peer_id)
            item = QListWidgetItem()
            self.__messages_list_widget.addItem(item)
            item.setSizeHint(fullLabel.sizeHint())
            self.__messages_list_widget.setItemWidget(item, fullLabel)

        # for i in list(reversed(self.__vkapi.getMessagesList(
        #         self.__dialog_list_widget.itemWidget(self.__dialog_list_widget.currentItem()).peer_id))):
        #     item = QListWidgetItem()
        #     self.__messages_list_widget.addItem(item)
        #     item.setSizeHint(i.sizeHint())
        #     self.__messages_list_widget.setItemWidget(item, i)

    def timer(self):
        while True:
            if self.__dialog_list_widget.currentItem is not None:
                self.getMessagesFromDialog()
                sleep(1.5)

    def sendMessage(self):
        try:
            self.__vkapi.sendMessage(self.__dialog_list_widget.itemWidget(
                self.__dialog_list_widget.currentItem()).peer_id, self.__edit_new_message.toPlainText())
            self.__edit_new_message.clear()
            self.__messages_list_widget.scrollToBottom()
        finally:
            pass