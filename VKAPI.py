from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtWidgets import QLabel
import http.client
from vk import *
import requests
from vk.exceptions import VkAuthError, VkAPIError
import json


class VKAPI(QObject):

    def __init__(self, app_id):
        super(VKAPI, self).__init__()
        self.__app_id = app_id
        self.__session = None
        self.__API = None

    def login(self, access_token):
        self.__session = Session(access_token)
        self.__API = API(self.__session)

    def getMessagesList(self):
        self.__dialogList = self.__API.messages.getDialogs(v='5.60',count='20')
        self.__msgs_list = []
        self.__ids = []

        for i in self.__dialogList['items']:
            self.__ids.append(i['message']['user_id'])

        users = self.__API.users.get(user_ids=self.__ids)
        counter = 0

        for i in self.__dialogList['items']:
            msg = QLabel()
            if i['message']['title'] == ' ... ':
                msg.setText('<b>' + users[counter]['first_name'] + ' ' + users[counter]['last_name'] + '</b>' +
                            '<br>' + i['message']['body'])
                counter += 1

            else:
                msg.setText('<b>' + i['message']['title'] + '</b>' +
                            '<br>' + i['message']['body'])
            self.__msgs_list.append(msg)

        return self.__msgs_list

    @property
    def app_id(self):
        return self.__app_id

    @property
    def API(self):
        return self.__API
