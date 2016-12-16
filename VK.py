from MainWindow import *
from OAuthWindow import OAuthWindow
from VKAPI import VKAPI
from PyQt5.QtWidgets import QApplication
import pickle
import sys

def main():
    app_id = '5682446'
    app = QApplication(sys.argv)
    vkapi = VKAPI(app_id)
    mainWindow = MainWindow(vkapi)

    try:
        with open('acc.pickle', 'r+b') as file:
            access_token = pickle.load(file)
            vkapi.login(access_token=access_token)
            mainWindow.loginSuccess()

    except:
        oauth = OAuthWindow(vkapi)
        oauth.loginSuccess.connect(mainWindow.loginSuccess)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()