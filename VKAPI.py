from PyQt5.QtCore import QObject
from vk import *

class VKAPI(QObject):

    def __init__(self, app_id):
        super(VKAPI, self).__init__()
        self.app_id = app_id
        self.session = None
        self.API = None

    def login(self, username, password):
        self.session = AuthSession(app_id = self.app_id, user_login = username, user_password = password)
        print(self.session.access_token)
        print(self.session)