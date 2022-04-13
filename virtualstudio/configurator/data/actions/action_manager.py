from typing import Dict, Optional

__ACTION_DICT: Dict[str, 'Action'] = {}


def registerAction(action: 'Action'):
    if action.ident not in __ACTION_DICT:
        __ACTION_DICT[action.ident] = action


def getActionByID(actionID: str) -> Optional['Action']:
    if actionID in __ACTION_DICT:
        return __ACTION_DICT[actionID]
    return None
