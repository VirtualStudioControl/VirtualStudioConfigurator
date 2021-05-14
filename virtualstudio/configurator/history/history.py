from typing import List, Optional

from .actions.abstract_history_action import AbstractHistoryAction


class History:

    def __init__(self):
        self.history: List[AbstractHistoryAction] = []
        self.stackpos = 0
        self.max_history_steps = 0

    def undo(self) -> Optional[AbstractHistoryAction]:
        """
        :return: the next undo action, or None, if not available
        """
        if not self.canUndo():
            return None
        self.stackpos -= 1
        item = self.history[self.stackpos]
        return item

    def redo(self) -> Optional[AbstractHistoryAction]:
        """

        :return: the next redo action, or None if not available
        """
        if not self.canRedo():
            return None
        item = self.history[self.stackpos]
        self.stackpos += 1
        return item

    def addItem(self, action: AbstractHistoryAction) -> bool:
        """
        Adds the given Action to the History, all redo actions after the current position are discarded
        :param action: Action to add
        :return: True if successfull
        """
        self.cutHistory()
        self.history.append(action)
        self.cullHistory()
        self.stackpos += 1
        return True

    def undoActionsAvailable(self) -> int:
        """

        :return: Number of Undo Actions available
        """
        return max(0, self.stackpos)

    def canUndo(self) -> bool:
        """

        :return: True if undo actions are available, False otherwise
        """
        return self.stackpos > 0

    def redoActionsAvailable(self) -> int:
        """

        :return: Number of Redo Actions available
        """
        return max(0, len(self.history) - self.stackpos)

    def canRedo(self) -> bool:
        """

        :return: True if Redo actions are available, False otherwise
        """
        return self.stackpos < len(self.history)

    def getAllItems(self) -> List[AbstractHistoryAction]:
        """

        :return: all History Actions
        """
        return self.history

    def getPosition(self):
        """

        :return: the current Position in the History Stack
        """
        return self.stackpos

    def setMaxHistoryItems(self, steps):
        """
        Sets the maximum number of History Items allowed. Number of Items is Best Effort. (No Gurantees)

        :param steps - Maximum number of actions allowed
        :return: None
        """
        self.max_history_steps = steps

    def clearHistory(self):
        """
        Clear all History Actiosn
        :return: None
        """
        self.history: List[AbstractHistoryAction] = []
        self.stackpos = 0

    def cutHistory(self):
        """
        Remove all Redo Actions
        :return: None
        """
        self.history = self.history[0 : self.stackpos]

    def cullHistory(self):
        """
        Remove Undo Actions, if more Undo actions are available than requested
        :return: None
        """
        if self.max_history_steps <= 0:
            return
        actualSteps = max(self.max_history_steps, len(self.history) - self.stackpos)
        self.history = self.history[actualSteps:]
