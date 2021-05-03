import json
import traceback
from typing import Callable, Dict, Any

from virtualstudio.common.net.tcp_client import TCPClient
from virtualstudio.common.net.protocols.virtualstudiocom.constants import *

class ComClient(TCPClient):

    def __init__(self, listenAddress="127.0.0.1", port=4233):
        super().__init__(listenAddress, port)
        self.messageCallbacks: Dict[str, Callable[[Any], None]] = {}

    def loadRequestHandlers(self):
        pass

    def addMessageCallback(self, messageID, handler):
        self.messageCallbacks[messageID] = handler

    def onMessageRecv(self, message: bytes):
        msg = json.loads(message.decode("utf-8"))
        if msg[INTERN_MESSAGE_ID] in self.messageCallbacks.keys():
            cb = self.messageCallbacks[msg[INTERN_MESSAGE_ID]]
            del self.messageCallbacks[msg[INTERN_MESSAGE_ID]]
            try:
                cb(msg)
            except Exception as ex:
                print("Exception occured during Event Handling:", ex)
                traceback.print_exc()
            pass

    def sendMessageJSON(self, message: dict, callback: Callable=None):
        if callback is not None:
            self.addMessageCallback(message[INTERN_MESSAGE_ID], callback)
        content = json.dumps(message)
        self.sendMessage(content.encode("utf-8"))
