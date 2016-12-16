from PyQt5.QtCore import QObject, QUrl
from PyQt5.QtWidgets import QLabel
from Dialog import Dialog
from Message import Message
import time
from vk import *


class VKAPI(QObject):

    def __init__(self, app_id):
        super(VKAPI, self).__init__()
        self.__app_id = app_id
        self.__session = None
        self.__API = None
        self.__users = {}
        self.__groups = {}

    def login(self, access_token):
        self.__session = Session(access_token)
        self.__API = API(self.__session)

    def getDialogsList(self):
        dialogList = self.__API.messages.getDialogs(v='5.60',count='20')
        msgs_list = []
        ids = []

        for i in dialogList['items']:
            if i['message'].get('chat_id') is None:
                ids.append(i['message']['user_id'])

        users = self.__API.users.get(user_ids=ids)
        self.__users.update({i["uid"]: i for i in users})

        for i in dialogList['items']:
            msg = Dialog()
            m = i["message"]
            if m.get("attachments") is not None:
                m["body"] += ("" if m["body"] == "" else"<br>") + m["attachments"][0]["type"]
            if m["out"]:
                m["body"] = "<i>Вы: </i>" + m["body"]
            if m.get('chat_id') is not None:
                users = self.__API.users.get(v='5.60', user_ids=m.get('chat_active'))
                self.__users.update({i['id']: i for i in users})

                msg.setText('<b>' + m["title"] + ': ' + self.getUser(m["user_id"])['first_name'] + ' ' +
                            self.getUser(m["user_id"])['last_name'] + "</b>" + '<br>' + m['body'])
                msg.peer_id = (2000000000 + m['chat_id'])

            elif i['message']['user_id'] < 0:
                msg.setText('<b>' + self.getGroup(abs(i['message']['user_id']))['name'] + '</b>' + '<br>'
                            + i['message']['body'])
                msg.peer_id = i['message']['user_id']

            else:
                msg.setText('<b>' + self.getUser(m["user_id"])['first_name'] + ' ' +
                            self.getUser(m["user_id"])['last_name'] + '</b>' +
                            '<br>' + i['message']['body'])
                msg.peer_id = m['user_id']

            msgs_list.append(msg)

        return msgs_list

    def getMessagesList(self, peer_id):
        msgs = []
        for i in (self.__API.messages.getHistory(v='5.60', peer_id=peer_id, count=50)['items']):
            msg = Message()
            if i['from_id'] > 0:
                msg.setText('<b>' + self.getUser(i['from_id'])['first_name'] + ' ' +
                            self.getUser(i['from_id'])['last_name'] + '</b><br>' + i['body'] + '<br>')

            else:
                msg.setText('<b>' + self.getGroup(abs(i['from_id']))['name'] + '</b><br>' + i['body'] + '<br>')

            msgs.append(msg)
        return msgs

    def sendMessage(self, peer_id, message):
        try:
            self.__API.messages.send(v='5.60', peer_id=peer_id, message=message)
        except:
            pass

    @property
    def app_id(self):
        return self.__app_id

    @property
    def API(self):
        return self.__API

    def getUser(self, *ids):
        l = []
        for i in ids:
            if i not in self.__users.keys():
                l.append(i)
        if len(l) != 0:
            users = self.__API.users.get(v="5.60", user_ids=l)
            self.__users.update({i["id"]: i for i in users})
        if len(ids) == 1:
            return self.__users[ids[0]]
        return {k: v for k, v in self.__users if k in ids }

    def getGroup(self, *ids):
        l = []
        for i in ids:
            if i not in self.__groups.keys():
                l.append(i)
        if len(l) != 0:
            groups = self.__API.groups.getById(v="5.60", group_ids=l)
            self.__groups.update({i["id"]: i for i in groups})
        if len(ids) == 1:
            return self.__groups[ids[0]]
        return {k: v for k, v in self.__groups if k in ids }