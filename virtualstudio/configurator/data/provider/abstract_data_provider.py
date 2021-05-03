from typing import List, Callable


class AbstractDataProvider:

    def __init__(self):
        pass

    def listActions(self, callback: Callable):
        pass

    def getActionIcon(self, callback: Callable, identifier: str):
        pass

    def getCategoryIcon(self, callback: Callable, category: List[str]):
        pass

    def listDevices(self, callback: Callable):
        pass
