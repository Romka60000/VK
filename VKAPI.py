from PyQt5.QtCore import QObject, QUrl
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
        self.__dialogList = self.__API.messages.getDialogs(count='200')
        for i in self.__dialogList:
            print (i)

    def getMessagesHistory(self):
        self.__longPollDict = self.__API.messages.getLongPollServer()

       #  self.__connection = http.client.HTTPConnection(self.__longPollDict['server'] + '?act=a_check&key=' +
       #                              self.__longPollDict['key'] + '&ts=' + str(self.__longPollDict['ts']) +
       #                              '&wait=25&mode=2&version=1 ')
       #  self.__connection.request("GET", "")
       #  print (self.__connection.getresponse().readall())
        print(self.__longPollDict['ts'])


        # self.__messages = self.__API.messages.getHistory(v='5.60', count='2', peer_id=2000000000 + 47)
        # for i in self.__messages['items']:
        #     print(json.dumps(i, indent=4))
        # for i in self.__messages['items']:
        #     print (i['body'] + " " + str(i['out']) + " " + str(i['fwd_messages']) + str(i['attachments']))

        self.__response = requests.get('http://' +self.__longPollDict['server'] + '?act=a_check&key=' +
                                     self.__longPollDict['key'] + '&ts=' + str(self.__longPollDict['ts']) +
                                     '&wait=25&mode=2&version=1 ')
        self.__ts = json.loads(self.__response.text.replace("'","\""))['ts']
        print(self.__ts)

    @property
    def app_id(self):
        return self.__app_id

    @property
    def API(self):
        return self.__API
