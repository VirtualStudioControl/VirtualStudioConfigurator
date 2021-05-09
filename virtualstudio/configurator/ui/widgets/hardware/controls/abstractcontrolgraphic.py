from typing import Optional

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from virtualstudio.common.structs.action.abstract_action import *
from virtualstudio.configurator.data.mimetypes import MIME_TYPE_ACTIONID
from .....data.actions.action_manager import getActionByID
from .....structs.action import Action


class AbstractControlGraphic(QGraphicsItem):

    def __init__(self, ident, position, size, text: str = None, parent: QWidget = None):
        super().__init__(parent)
        self.ident = ident

        self.position = position
        self.size = size

        self.setPos(*position)

        self.text = text
        if self.text is None:
            self.text = str(ident)

        self.selectable = True

        self.pen_outline = QPen(Qt.black)
        self.brushBackground = QBrush(QColor("#FFFFFF"), Qt.SolidPattern)
        self.brushAction = QBrush(QColor("#8800FF00"), Qt.Dense3Pattern)
        self.brushSelected = QBrush(QColor("#8800AAFF"), Qt.Dense4Pattern)

        self.action: Optional[Action] = None

        self.setFlag(self.ItemIsSelectable, self.selectable)
        self.setFlag(self.ItemIsMovable, False)
        self.setAcceptDrops(self.selectable)

    def getType(self):
        return CONTROL_TYPE_NONE

    def toDict(self):
        r = {'ident': self.ident, 'type': self.getType(), 'position': self.position, 'size': self.size,
             'text': self.text, 'selectable': self.selectable}

        return r

    def setSelectable(self, value: bool):
        self.selectable = value
        self.setFlag(self.ItemIsSelectable, self.selectable)
        self.setAcceptDrops(self.selectable)

    def boundingRect(self) -> QRectF:
        """Defining Qt bounding rectangle"""
        return QRectF(
            0,
            0,
            self.size[0],
            self.size[1]
        ).normalized()

    def dragEnterEvent(self, event: QGraphicsSceneDragDropEvent):
        if not self.selectable:
            event.ignore()
            return
        if MIME_TYPE_ACTIONID in event.mimeData().formats():
            actionID = bytes(event.mimeData().data(MIME_TYPE_ACTIONID)).decode('utf-8')
            action: Action = getActionByID(actionID)
            if self.getType() in action.allowedControls:
                event.accept()
            else:
                event.ignore()

    def dragLeaveEvent(self, event: QGraphicsSceneDragDropEvent):
        pass

    def dropEvent(self, event: QGraphicsSceneDragDropEvent):
        if MIME_TYPE_ACTIONID in event.mimeData().formats():
            actionID = bytes(event.mimeData().data(MIME_TYPE_ACTIONID)).decode('utf-8')
            self.action = getActionByID(actionID)
            self.update()
            event.accept()
            return
        event.ignore()
