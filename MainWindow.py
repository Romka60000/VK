from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import vk
from Button import Button
from VKAPI import VKAPI

class MainWindow(QWidget):
    def __init__(self, VKAPI):
        super(MainWindow, self).__init__()
        self.setMinimumSize(900, 580)
        self.setWindowTitle("VK Standalone")
        self.setWindowIcon(QIcon("pics/TitleIcon.png"))
        self.setStyleSheet("background-color: white;")
        self.__vkapi = VKAPI

        # self.__btnProfile = Button("Profile", "pics/Profile.png")
        # self.__btnFriends = Button("Friends", "pics/Friends.png")
        # self.__btnMessages = Button("Messages", "pics/Message.png")
        # self.__btnNews = Button("News", "pics/News.png")
        # self.__btnPhotos = Button("Photos", "pics/Photos.png")
        # self.__btnMusic = Button("Music", "pics/Music.png")
        # self.__btnVideos = Button("Videos", "pics/Video.png")
        # self.__btnCommunities = Button("Communities", "pics/Communities.png")
        #
        # self.__vbox = QVBoxLayout()
        # self.__vbox.setAlignment(Qt.AlignTop)
        # self.__vbox.addWidget(self.__btnProfile)
        # self.__vbox.addWidget(self.__btnFriends)
        # self.__vbox.addWidget(self.__btnMessages)
        # self.__vbox.addWidget(self.__btnNews)
        # self.__vbox.addWidget(self.__btnCommunities)
        # self.__vbox.addWidget(self.__btnPhotos)
        # self.__vbox.addWidget(self.__btnMusic)
        # self.__vbox.addWidget(self.__btnVideos)
        #
        # self.setLayout(self.__vbox)

    def loginSuccess(self):
        self.show()
        #self.__vkapi.getMessagesList()
        self.__vkapi.getMessagesHistory()