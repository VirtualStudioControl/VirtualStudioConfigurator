from typing import Optional, Callable

from .abstract_history_action import *
from ...structs.action import Action

from typing import TypeVar

ACTION_TYPE_VALUE_CHANGED = getUniqueActionUUID()

T = TypeVar('T')


class ActionValueChanged (AbstractHistoryAction):
    def __init__(self, func: Callable[[T], None], old: Optional[T], new: Optional[T]):
        super(ActionValueChanged, self).__init__()

        self.__func: Callable[[T], None] = func
        self.__old: Optional[T] = old
        self.__new: Optional[T] = new

    def __str__(self):
        return "Value Changed, func='" + str(self.__func) + "'; old=" + str(self.__old) + "; new=" + str(self.__new)

    def action_type(self) -> int:
        return ACTION_TYPE_VALUE_CHANGED

    def undoAction(self):
        self.__func(self.__old)

    def redoAction(self):
        self.__func(self.__new)
