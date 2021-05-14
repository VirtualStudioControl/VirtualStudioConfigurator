from typing import List, Callable


class AbstractDataProvider:

    def __init__(self):
        pass

    def getProfileSet(self, deviceID: str, callback: Callable):
        pass

    def listActions(self, callback: Callable[[bool, List, List], None]):
        pass

    def listDevices(self, callback: Callable[[bool, List], None]):
        pass
