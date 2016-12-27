from PyQt5.QtCore import QObject

class Message(QObject):
    def __init__(self, dct, api):
        self.__msg = dct
        self.__api = api
        self.__msg["peer_id"] = self.getPeerId()

    def __getattr__(self, item):
        return self.__msg.get(item)

    def getPeerId(self):
        if self.chat_id is not None:
            return 2000000000 + self.chat_id
        return self.user_id

    def getTitle(self, chat_title):
        idx = self.from_id if self.from_id is not None else self.user_id
        if idx < 0:
            sender = self.__api.getGroup(-idx)["name"]
        else:
            user = self.__api.getUser(idx)
            sender = user["first_name"] + " " + user["last_name"]
        s = "<b>" + (self.title + ": " if self.chat_id is not None and chat_title else "") + sender + "</b><br>"
        body = self.body
        if self.out and chat_title:
            body = '<i>Вы: </i>' + body
        s += body + ("<br>" if self.body != "" else "")
        return s

    def getShortText(self):
        s = self.getTitle(True)
        if self.attachments is not None:
            s += self.attachments[0]['type'].capitalize() + '<br>'
        if self.fwd_messages is not None:
            s += 'Forwarded messages<br>'
        return s

    def getFullText(self):
        s = self.getTitle(False)
        if self.attachments is not None:
            for i in self.attachments:
                if i['type'] == 'photo':
                    s += '<a href= ' + self.__api.getPhoto(i) +'>Photo</a><br>'
                elif i['type'] == 'doc':
                    s += '<a href= ' + i['doc']['url'] + 'Document: ' + i['doc']['title'] + '</a><br>'
                else:
                    s += i['type'].capitalize() + '<br>'
        if self.fwd_messages is not None:
            s += "<i>Forwarded messages:</i><br>"
            s += self.__api.getMessage(self.fwd_messages)
        return s
