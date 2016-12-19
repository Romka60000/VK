from Message import Message


class MessageContainer:
    def __init__(self):
        self.__msgs = {}

    def addMessages(self, *msgs):
        for i in msgs:
            if isinstance(i, Message):
                self.__msgs[i.id] = i

    def getDialog(self, peer_id):
        return sorted([m for m in self.__msgs.values() if m.peer_id == peer_id], key=lambda x: x.id)
