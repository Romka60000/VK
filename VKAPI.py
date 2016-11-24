from PyQt5.QtCore import QObject
from vk import *
from vk.exceptions import VkAuthError, VkAPIError
from vk.mixins import *

class VKAPI(QObject):

    def __init__(self, app_id):
        super(VKAPI, self).__init__()
        self.app_id = app_id
        self.session = None
        self.API = None

    def login(self, access_token):

        self.session = Session(access_token)
        self.API = API(self.session)
