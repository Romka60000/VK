from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QObject
from PyQt5.QtWebKitWidgets import QWebView
import vk
import json
from vk.exceptions import VkAuthError, VkAPIError

class OAuthWindow(QObject):
    success_login = pyqtSignal()


    def __init__(self, VKAPI):
        super(OAuthWindow, self).__init__()
        self.web_view = QWebView()
        self.web_view.setFixedSize(400,400)
        self.web_view.show()
        self.web_view.setUrl(QUrl('https://oauth.vk.com/authorize?client_id=' + VKAPI.app_id +'&display=mobile&redirect_uri=http://vk.com&scope=offline,wall,messages,audio,video,friends&response_type=code&v=5.60'))
        self.VKAPI = VKAPI
        self.web_view.loadFinished.connect(self.loaded)

    def loaded(self):
        if '#code=' in self.web_view.url().toString():
            code = self.web_view.url().toString()[self.web_view.url().toString().index("code=")+5:]
            self.web_view.setUrl(QUrl('https://oauth.vk.com/access_token?client_id=' + self.VKAPI.app_id + '&client_secret=aW4JW9GEqR997m3O0rDW&redirect_uri=http://vk.com&code=' + code))
        elif 'access_token' in self.web_view.page().mainFrame().toPlainText():
            access_token = (json.loads(self.web_view.page().mainFrame().toPlainText().replace("'","\""))["access_token"])
            self.web_view.hide()
            self.VKAPI.login(access_token)
            self.success_login.emit()

