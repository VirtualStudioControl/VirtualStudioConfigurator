from typing import Dict

from virtualstudio.common.net.protocols.virtualstudiocom import constants as consts
from virtualstudio.common.structs.action.action_info import ActionInfo
from virtualstudio.common.structs.action.action_info import fromDict as actionInfoFromDict
from virtualstudio.configurator.profilemanager import profileset_manager


def paramUpdateHandler(params: Dict):
    onParamUpdate(actionInfoFromDict(params[consts.EVT_UPDATE_PARAMS_PARAM_ACTION]))

def onParamUpdate (action: ActionInfo):
    profileset_manager.updateActionData(action)