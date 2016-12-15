from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QObject, QFile
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtGui import QIcon
import vk
import pickle
import json
from vk.exceptions import VkAuthError, VkAPIError

class OAuthWindow(QObject):
    loginSuccess = pyqtSignal()

    def __init__(self, VKAPI):
        super(OAuthWindow, self).__init__()
        self.__web_view = QWebView()
        self.__web_view.setFixedSize(400,400)
        self.__web_view.setWindowIcon(QIcon('pics/TitleIcon.png'))
        self.__web_view.setWindowTitle("Authorization")
        self.__web_view.show()
        self.__web_view.setUrl(QUrl('https://oauth.vk.com/authorize?client_id=' + VKAPI.app_id +
                                    '&display=mobile&redirect_uri=http:' +
                               '//vk.com&scope=offline, messages, groups&response_type=code&v=5.60'))
        self.__VKAPI = VKAPI
        self.__web_view.loadFinished.connect(self.loaded)

    def loaded(self):
        if '#code=' in self.__web_view.url().toString():
            code = self.__web_view.url().toString()[self.__web_view.url().toString().index("code=")+5:]
            self.__web_view.setUrl(QUrl('https://oauth.vk.com/access_token?client_id=' + self.__VKAPI.app_id +
                                        '&client_secret=aW4JW9GEqR997m3O0rDW&redirect_uri=http://vk.com&code=' + code))
        elif 'access_token' in self.__web_view.page().mainFrame().toPlainText():
            access_token = (json.loads(self.__web_view.page().mainFrame().toPlainText().replace("'","\""))["access_token"])
            self.__web_view.hide()
            self.__VKAPI.login(access_token)
            with open('acc.pickle', 'w+b') as file:
                pickle.dump(access_token, file)
            self.loginSuccess.emit()