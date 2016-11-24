from PyQt5.QtCore import QObject
from vk import *
from vk.exceptions import VkAuthError, VkAPIError
from vk.mixins import *

class VKAPI(QObject):

    def __init__(self, app_id):
        super(VKAPI, self).__init__()
        self.__app_id = app_id
        self.__session = None
        self.__API = None

    def login(self, access_token):
        self.__session = Session(access_token)
        self.__API = API(self.__session)

    @property
    def app_id(self):
        return self.__app_id

    @property
    def API(self):
        return self.__API
