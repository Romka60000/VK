from MainWindow import *
from OAuthWindow import OAuthWindow
from VKAPI import VKAPI
from PyQt5.QtWidgets import QApplication
import sys

def main():
    app_id = '5682446'
    app = QApplication(sys.argv)
    vkapi = VKAPI(app_id)
    oauth = OAuthWindow(vkapi)

    mainWindow = MainWindow(vkapi)
    oauth.loginSuccess.connect(mainWindow.loginSuccess)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()