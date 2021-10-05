from typing import List, Callable, Dict, Any

from virtualstudio.common.account_manager.account_info import AccountInfo
from virtualstudio.common.structs.action.action_info import ActionInfo
from virtualstudio.common.structs.profile.profile import Profile


class AbstractDataProvider:

    def __init__(self):
        pass

    #region Messages

    #region Accounts

    def listAccounts(self, callback: Callable[[bool, List, Dict, Dict], None]):
        pass

    def setAccountData(self, account: AccountInfo, callback: Callable[[bool, str], None]):
        pass
    #endregion

    #region Actions

    def listActions(self, callback: Callable[[bool, List, List], None]):
        pass

    def getActionStates(self, action: ActionInfo, callback: Callable[[int, bool], None]):
        pass

    def getActionWidget(self, action: ActionInfo, callback: Callable[[Any, str, bool], None]):
        pass

    def setActionData(self, action: ActionInfo, data: dict, callback: Callable[[bool], None]):
        pass

    #endregion

    #region Device
    def listDevices(self, callback: Callable[[bool, List], None]):
        pass
    #endregion

    #region Profiles

    def getProfileSet(self, deviceID: str, callback: Callable[[Dict], None]):
        pass

    def setCurrentProfile(self, deviceID: str, profileName: str, callback: Callable[[bool], None]):
        pass

    def addProfile(self, deviceID: str, profile: Profile, callback: Callable[[Dict, bool], None]):
        pass

    def updateProfile(self, deviceID: str, profile: Profile, callback: Callable[[Dict, bool], None]):
        pass

    def removeProfile(self, deviceID: str, profileName: str, callback: Callable[[Dict, bool], None]):
        pass

    #endregion

    #endregion

    #region Events

    def setupEvents(self):
        pass

    #endregion