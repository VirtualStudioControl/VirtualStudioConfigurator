from typing import Optional, Callable

from virtualstudio.common.profile_manager.profileset import ProfileSet
from .abstract_history_action import *
from ...structs.action import Action

from typing import TypeVar


ACTION_TYPE_PROFILE_ACTION = getUniqueActionUUID()

T = TypeVar('T')

PROFILE_ADDED = 0x01
PROFILE_REMOVED = 0x02


class ActionProfileAction (AbstractHistoryAction):

    def __init__(self, profileset: ProfileSet, profilename: str):
        super(ActionProfileAction, self).__init__()

        self.profileset = profileset
        self.profilename = profilename

    def __str__(self):
        return "Value Changed, profileset='" + self.profileset.hardwareFamily + " profilename=" + self.profilename

    def action_type(self) -> int:
        return ACTION_TYPE_PROFILE_ACTION

    def undoAction(self):
        pass
        #self.__func(self.__old)

    def redoAction(self):
        pass
        #self.__func(self.__new)