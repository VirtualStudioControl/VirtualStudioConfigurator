from typing import Tuple

from .abstract_history_action import *

ACTION_TYPE_MULTIACTION = getUniqueActionUUID()


class ActionMultiAction (AbstractHistoryAction):
    def __init__(self, *actions: AbstractHistoryAction):
        super(ActionMultiAction, self).__init__()
        self.__actions: Tuple[AbstractHistoryAction] = actions

    def __str__(self):
        return "MultiAction, actions='" + str(self.__actions)

    def action_type(self) -> int:
        return ACTION_TYPE_MULTIACTION

    def undoAction(self):
        for a in self.__actions:
            a.undoAction()

    def redoAction(self):
        for a in self.__actions:
            a.redoAction()
