from PyQt5.QtCore import QObject
from Dialog import Dialog
from Message import Message
from MessageLabel import MessageLabel
from MessageContainer import MessageContainer
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
        self.__msgs = MessageContainer()

    def login(self, access_token):
        self.__session = Session(access_token)
        self.__API = API(self.__session)

    def getDialogsList(self):
        dialogList = self.__API.messages.getDialogs(v='5.60',count='20')

        dlg_list = []
        ids = []
        for i in dialogList["items"]:
            msg = i["message"]
            if msg["user_id"] > 0:
                ids.append(msg["user_id"])
            if msg.get("chat_id") is not None:
                ids.extend(msg["chat_active"])
        users = self.__API.users.get(user_ids=ids)
        self.__users.update({i["uid"]: i for i in users})
        for i in dialogList['items']:
            msg = Message(i["message"], self)
            # dlg_list.append(MessageLabel(msg.getShortText(), False))
            dlg_list.append(msg)
            self.__msgs.addMessages(msg)
        return dlg_list

        # for i in dialogList['items']:
        #     dlg = Dialog()
        #     m = i["message"]
        #     if m.get("attachments") is not None:
        #         m["body"] += ("" if m["body"] == "" else "<br>") + m["attachments"][0]["type"]
        #     if m.get("fwd_messages") is not None:
        #         m["body"] += ("" if m["body"] == "" else "<br>") + 'Forwarded messages'
        #     if m["out"]:
        #         m["body"] = "<i>Вы: </i>" + m["body"]
        #     if m.get('chat_id') is not None:
        #         ids.append(m.get('chat_active'))
        #
        #         dlg.setText('<b>' + m["title"] + ': ' + self.getUser(m["user_id"])['first_name'] + ' ' +
        #                     self.getUser(m["user_id"])['last_name'] + "</b>" + '<br>' + m['body'])
        #         dlg.peer_id = (2000000000 + m['chat_id'])
        #
        #     elif i['message']['user_id'] < 0:
        #         dlg.setText('<b>' + self.getGroup(abs(i['message']['user_id']))['name'] + '</b>' + '<br>'
        #                     + i['message']['body'])
        #         dlg.peer_id = i['message']['user_id']
        #
        #     else:
        #         dlg.setText('<b>' + self.getUser(m["user_id"])['first_name'] + ' ' +
        #                     self.getUser(m["user_id"])['last_name'] + '</b>' +
        #                     '<br>' + i['message']['body'])
        #         dlg.peer_id = m['user_id']
        #
        #     dlg_list.append(dlg)
        # self.__users.update({i["uid"]: i for i in users})
        # return dlg_list

    def getMessagesList(self, peer_id):
        messages_list = self.__API.messages.getHistory(v='5.60', peer_id=peer_id, count=10)
        for i in messages_list['items']:
            if i not in self.__msgs.getDialog(peer_id):
                self.__msgs.addMessages(Message(i, self))
        return self.__msgs.getDialog(peer_id)




        # msgs = []
        # history = self.__API.messages.getHistory(v='5.60', peer_id=peer_id, count=50)
        # for i in (history['items']):
        #     if i.get('attachments') is not None:
        #         self.getAttachments(i)
        #
        #     if i.get('fwd_messages'):
        #         i['body'] += '<br><i>Forwarded messages:</i><br>' + self.getMessage(i['fwd_messages'])
        #
        #     msg = MessageLabel("")
        #     if i['from_id'] > 0:
        #         msg.setText('<br><b>' + self.getUser(i['from_id'])['first_name'] + ' ' +
        #                     self.getUser(i['from_id'])['last_name'] + '</b><br>' + i['body'] + '<br>')
        #     else:
        #         msg.setText('<b>' + self.getGroup(abs(i['from_id']))['name'] + '</b><br>' + i['body'] + '<br>')
        #
        #     msgs.append(msg)
        # return msgs

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

    def getAttachments(self, msg):
        if msg['body'] != '':
            msg['body'] += '<br>'
        for k in msg.get('attachments'):
            if k['type'] == 'photo':
                msg['body'] += '<a href=' + self.getPhoto(k) + '>Photo</a><br>'
            elif k['type'] == 'doc':
                msg['body'] += '<a href=' + k['doc']['url'] + '>Document: ' + k['doc']['title'] + '</a><br>'
            else:
                msg['body'] += '' + str(k['type']).capitalize() + '<br>'

    def getMessage(self, msgs):
        body = '-------------------------------------------------------<br>'
        for i in msgs:
            if i.get('attachments') is not None:
                self.getAttachments(i)

            if i['user_id'] > 0:
                body += ('<br><b>' + self.getUser(i['user_id'])['first_name'] + ' ' +
                            self.getUser(i['user_id'])['last_name'] + '</b><br>' + i['body'] + '<br>')
            else:
                body += ('<b>' + self.getGroup(abs(i['user_id']))['name'] + '</b><br>' + i['body'] + '<br>')
            if i.get('fwd_messages') is not None:
                body += self.getMessage(i.get('fwd_messages'))
        body += '-------------------------------------------------------'
        return body

    def getPhoto(self, msg):
        photo = msg.get('photo')
        return photo["photo_" + str(max(map(lambda x: int(x[6:]),
                                            [i for i in photo.keys() if i.startswith("photo_")])))]
