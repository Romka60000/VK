from PyQt5.QtCore import QObject
from Message import Message
from MessageContainer import MessageContainer
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
        dialogList = self.__API.messages.getDialogs(v='5.60',count='30')

        dlg_list = []
        ids = []
        for i in dialogList["items"]:
            dlg = i["message"]
            if dlg["user_id"] > 0:
                ids.append(dlg["user_id"])
            if dlg.get("chat_id") is not None:
                ids.extend(dlg["chat_active"])
        users = self.__API.users.get(user_ids=ids)
        self.__users.update({i["uid"]: i for i in users})
        for i in dialogList['items']:
            dlg = Message(i["message"], self)
            dlg_list.append(dlg)
            self.__msgs.addMessages(dlg)
        return dlg_list

    def getMessagesList(self, peer_id):
        messages_list = self.__API.messages.getHistory(v='5.60', peer_id=peer_id, count=50)
        for i in messages_list['items']:
            if i not in self.__msgs.getDialog(peer_id):
                self.__msgs.addMessages(Message(i, self))
        return self.__msgs.getDialog(peer_id)

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
