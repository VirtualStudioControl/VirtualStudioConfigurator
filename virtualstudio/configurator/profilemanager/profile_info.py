from typing import Dict

from virtualstudio.common.structs.action.action_info import ActionInfo
from virtualstudio.common.structs.profile.profile import Profile

from virtualstudio.common.structs.action.action_info import fromDict as actionInfoFromDict

class ProfileInfo(Profile):

    def __init__(self, hardwareFamily: str, name: str, category=None):
        super().__init__(hardwareFamily, name, category)

        self.actions: Dict[int, ActionInfo] = {}

    def setAction(self, controlID: int, action: ActionInfo):
        self.actions[controlID] = action

    def removeAction(self, controlID: int):
        if controlID in self.actions:
            del self.actions[controlID]

    def update(self, other):
        self.hardwareFamily = other.hardwareFamily
        if isinstance(other, ProfileInfo):
            self.actions = other.actions
            return

        self.actions: Dict[int, ActionInfo] = {}

        for actionID in other.actions:
            self.actions[actionID] = other.actions[actionID].getActionInfo()


    def toDict(self):
        result = {
            "hardwareFamily": self.hardwareFamily,
            "name": self.name,
            "category": self.category,
        }

        actionList = []

        for action in self.actions:
            actionList.append(self.actions[action].toDict())

        result["actions"] = actionList

        return result

def fromDict(values: dict):
    profile = ProfileInfo(hardwareFamily=values["hardwareFamily"], name=values["name"],
                      category=values["category"])
    for actionDict in values["actions"]:
        info = actionInfoFromDict(actionDict)
        profile.setAction(controlID=info.control, action=info)

    return profile