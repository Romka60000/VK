from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtWidgets import QLabel
import http.client
from vk import *
import requests
import time
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

    def getNewMessages(self):
        self.__longPollDict = self.__API.messages.getLongPollServer()

        # self.__messages = self.__API.messages.getHistory(v='5.60', count='2', peer_id=2000000000 + 47)
        # for i in self.__messages['items']:
        #     print(json.dumps(i, indent=4))
        # for i in self.__messages['items']:
        #     print (i['body'] + " " + str(i['out']) + " " + str(i['fwd_messages']) + str(i['attachments']))

        self.__response = requests.get('http://' + self.__longPollDict['server'] + '?act=a_check&key=' +
                                     self.__longPollDict['key'] + '&ts=' + str(self.__longPollDict['ts']) +
                                     '&wait=25&mode=32&version=1 ')
        self.__ts = json.loads(self.__response.text.replace("'","\""))['ts']
        self.__pts = json.loads(self.__response.text.replace("'","\""))['pts']

    @property
    def app_id(self):
        return self.__app_id

    @property
    def API(self):
        return self.__API
