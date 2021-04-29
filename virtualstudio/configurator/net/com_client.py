import json

from virtualstudio.common.net.tcp_client import TCPClient
from virtualstudio.common.net.protocols.virtualstudiocom.constants import *

class ComClient(TCPClient):

    def __init__(self, listenAddress="127.0.0.1", port=4233):
        super().__init__(listenAddress, port)
        self.messageCallbacks = {}

    def loadRequestHandlers(self):
        pass

    def addMessageCallback(self, messageID, handler):
        self.messageCallbacks[messageID] = handler

    def onMessageRecv(self, message: bytes):
        msg = json.loads(message.decode("utf-8"))
        print(msg)
        if msg[INTERN_MESSAGE_ID] in self.messageCallbacks.keys():
            self.messageCallbacks[msg[INTERN_MESSAGE_ID]](msg)

    def sendMessageJSON(self, message: dict, callback=None):
        if callback is not None:
            self.addMessageCallback(message[INTERN_MESSAGE_ID], callback)
        content = json.dumps(message)
        self.sendMessage(content.encode("utf-8"))
