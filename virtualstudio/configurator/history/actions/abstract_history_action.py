NEXT_UUID = 0x00

def getUniqueActionUUID():
    """

    :return: the next action type UUID
    """
    global NEXT_UUID
    uuid = NEXT_UUID
    NEXT_UUID += 1
    return uuid


ACTION_TYPE_ABSTRACT = getUniqueActionUUID()


class AbstractHistoryAction:
    def __init__(self):
        pass

    def __str__(self):
        return "AbstractHistoryAction"

    def action_type(self) -> int:
        return ACTION_TYPE_ABSTRACT

    def undoAction(self):
        pass

    def redoAction(self):
        pass
