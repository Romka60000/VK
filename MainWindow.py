from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import vk
from Button import Button

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setMinimumSize(900, 580)
        self.setWindowTitle("VK Standalone")
        self.setWindowIcon(QIcon("pics/TitleIcon.png"))
        self.setStyleSheet("background-color: white;")

        btnProfile = Button("Profile", "pics/Profile.png")
        btnFriends = Button("Friends", "pics/Friends.png")
        btnMessages = Button("Messages", "pics/Message.png")
        btnNews = Button("News", "pics/News.png")
        btnPhotos = Button("Photos", "pics/Photos.png")
        btnMusic = Button("Music", "pics/Music.png")
        btnVideos = Button("Videos", "pics/Video.png")
        btnCommunities = Button("Communities", "pics/Communities.png")

        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.addWidget(btnProfile)
        vbox.addWidget(btnFriends)
        vbox.addWidget(btnMessages)
        vbox.addWidget(btnNews)
        vbox.addWidget(btnCommunities)
        vbox.addWidget(btnPhotos)
        vbox.addWidget(btnMusic)
        vbox.addWidget(btnVideos)
        self.setLayout(vbox)