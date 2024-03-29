from typing import List, Callable, Dict, Any

from virtualstudio.common.account_manager.account_info import AccountInfo
from virtualstudio.common.net.protocols.virtualstudiocom import constants as const
from virtualstudio.common.structs.action.action_info import ActionInfo
from virtualstudio.common.structs.profile.profile import Profile
from .abstract_data_provider import AbstractDataProvider
from ...eventhandler.eventhandler import paramUpdateHandler
from ...net.com_client import ComClient

from virtualstudio.common.net.protocols.virtualstudiocom import client as req


class ComDataProvider(AbstractDataProvider):

    def __init__(self, coreAddress: str = "127.0.0.1", core_port: int = 4233): #"192.168.114.105" "127.0.0.1" "172.24.2.159"
        super().__init__()
        self.client = ComClient(coreAddress, core_port)
        self.client.start()

    #region Messages

    #region Accounts

    def listAccounts(self, callback: Callable[[bool, List, Dict, Dict], None]):
        def __wrap(msg: dict):
            callback(msg['accounts_loaded'], msg['accounts'], msg['accountTypes'], msg['categories'])

        self.client.sendMessageJSON(req.requestAccountList(), __wrap)

    def setAccountData(self, account: AccountInfo, callback: Callable[[bool, str], None]):
        def __wrap(msg: dict):
            callback(msg['success'], msg['uuid'])
        self.client.sendMessageJSON(req.setAccountData(account), __wrap)

    #endregion

    #region Actions

    def listActions(self, callback: Callable[[bool, List, List], None]):
        def __wrap(msg: dict):
            callback(msg['actions_loaded'], msg['actions'], msg['categories'])

        self.client.sendMessageJSON(req.requestActionList(), __wrap)

    def getActionStates(self, action: ActionInfo, callback: Callable[[int, bool], None]):
        def __wrap(msg: dict):
            callback(msg['states'], msg['success'])

        self.client.sendMessageJSON(req.getActionStates(action), __wrap)

    def getActionWidget(self, action: ActionInfo, callback: Callable[[Any, str, bool], None]):
        def __wrap(msg: dict):
            callback(msg['widgetdata'], msg['widgetdatatype'], msg['success'])

        self.client.sendMessageJSON(req.getActionWidget(action), __wrap)

    def setActionData(self, action: ActionInfo, data: dict, callback: Callable[[bool], None]):
        def __wrap(msg: dict):
            callback(msg['success'])
        self.client.sendMessageJSON(req.setActionData(action, data), __wrap)

    #endregion

    #region Devices

    def listDevices(self, callback: Callable[[bool, List], None]):
        def __wrap(msg: dict):
            callback(msg['devices_loaded'], msg['devices'])

        self.client.sendMessageJSON(req.requestDeviceList(), __wrap)

    #endregion

    #region Profiles

    def getProfileSet(self, deviceID: str, callback: Callable[[Dict], None]):
        def __wrap(msg: dict):
            callback(msg['profileset'])

        self.client.sendMessageJSON(req.requestProfileSet(deviceID), __wrap)

    def setCurrentProfile(self, deviceID: str, profileName: str, callback: Callable[[bool], None]):
        def __wrap(msg: dict):
            callback(msg['success'])

        self.client.sendMessageJSON(req.requestSetCurrentProfile(deviceID, profileName), __wrap)

    def addProfile(self, deviceID: str, profile: Profile, callback: Callable[[Dict, bool], None]):
        def __wrap(msg: dict):
            callback(msg['profileset'], msg['success'])

        self.client.sendMessageJSON(req.requestAddProfile(deviceID, profile), __wrap)

    def updateProfile(self, deviceID: str, profile: Profile, callback: Callable[[Dict, bool], None]):
        def __wrap(msg: dict):
            callback(msg['profileset'], msg['success'])

        self.client.sendMessageJSON(req.requestUpdateProfile(deviceID, profile), __wrap)

    def removeProfile(self, deviceID: str, profileName: str, callback: Callable[[Dict, bool], None]):
        def __wrap(msg: dict):
            callback(msg['profileset'], msg['success'])

        self.client.sendMessageJSON(req.requestRemoveProfile(deviceID, profileName), __wrap)

    #endregion

    #endregion

    #region Events

    def setupEvents(self):
        self.client.addEventCallback(const.EVT_UPDATE_PARAMS, paramUpdateHandler)

    #endregion

    def close(self):
        try:
            self.client.requestStop()
            self.client.join(1)
        finally:
            self.client.closeConnection()
