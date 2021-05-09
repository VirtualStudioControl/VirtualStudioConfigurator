from typing import Dict, Any

__ACTION_DICT: Dict[str, Any] = {}


def registerAction(action):
    if action.ident not in __ACTION_DICT:
        __ACTION_DICT[action.ident] = action


def getActionByID(actionID: str):
    if actionID in __ACTION_DICT:
        return __ACTION_DICT[actionID]
    return None
