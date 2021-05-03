from typing import List, Callable

from .abstract_data_provider import AbstractDataProvider
from ...net.com_client import ComClient

from virtualstudio.common.net.protocols.virtualstudiocom import client as req

class ComDataProvider(AbstractDataProvider):

    def __init__(self, coreAddress: str = "127.0.0.1", core_port: int = 4233):
        super().__init__()
        self.client = ComClient(coreAddress, core_port)
        self.client.start()

    def listActions(self, callback: Callable[[bool, List, List], None]):
        def __wrap(msg: dict):
            print(msg)
            callback(msg['actions_loaded'], msg['actions'], msg['categories'])

        self.client.sendMessageJSON(req.requestActionList(), __wrap)

    def listDevices(self, callback: Callable[[bool, List], None]):
        def __wrap(msg: dict):
            callback(msg['devices_loaded'], msg['devices'])

        self.client.sendMessageJSON(req.requestDeviceList(), __wrap)

    def close(self):
        try:
            self.client.requestStop()
            self.client.join(1)
        finally:
            self.client.closeConnection()
