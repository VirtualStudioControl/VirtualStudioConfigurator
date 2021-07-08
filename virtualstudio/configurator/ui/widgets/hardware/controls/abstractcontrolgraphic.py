from typing import Optional

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from virtualstudio.common.structs.action.abstract_action import *
from virtualstudio.common.structs.action.action_info import ActionInfo
from virtualstudio.common.tools import actiondatatools, icontools
from .....data.mimetypes import MIME_TYPE_ACTIONID
from .....data.actions.action_manager import getActionByID
from .....data import constants

from .....history.actions.action_value_changed import ActionValueChanged

from .....structs.action import Action

from virtualstudio.configurator.profilemanager import profileset_manager as profilemanager
from virtualstudio.configurator.data import constants
from virtualstudio.configurator.data.tools import datarequests


class AbstractControlGraphic(QGraphicsItem):

    def __init__(self, ident: int, position, size, text: str = None, parent: QWidget = None):
        super().__init__(parent)
        self.ident: int = ident

        self.position = position
        self.size = size

        self.setPos(*position)

        self.text = text
        if self.text is None:
            self.text = str(ident)

        self.selectable = True
        self.isSelected = False

        self.pen_outline = QPen(Qt.black)
        self.brushBackground = QBrush(QColor("#FFFFFF"), Qt.SolidPattern)
        self.brushAction = QBrush(QColor("#8800FF00"), Qt.Dense3Pattern)

        self.pen_selected = QPen(QColor("#FF00AAFF"))
        self.pen_selected.setWidth(3)
        self.brushSelected = QBrush(QColor("#8800AAFF"), Qt.Dense4Pattern)

        self.action: Optional[ActionInfo] = None

        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setAcceptDrops(self.selectable)

    def getType(self):
        return CONTROL_TYPE_NONE

    def toDict(self):
        r = {'ident': self.ident, 'type': self.getType(), 'position': self.position, 'size': self.size,
             'text': self.text, 'selectable': self.selectable}

        return r

    def setSelectable(self, value: bool):
        self.selectable = value
        self.setAcceptDrops(self.selectable)

    def boundingRect(self) -> QRectF:
        """Defining Qt bounding rectangle"""
        return QRectF(
            0,
            0,
            self.size[0],
            self.size[1]
        ).normalized()

    def setAction(self, action: ActionInfo):
        try:
            constants.HISTORY.addItem(ActionValueChanged(func=self._setAction, old=self.action, new=action))
        except Exception as ex:
            print(ex)

        self._setAction(action)

    def _setAction(self, action: Optional[ActionInfo]):
        self.action = action
        if self.action is not None:
            iconData = actiondatatools.getValueOrDefault(self.action.actionParams,
                                                                actiondatatools.KEY_STATE_IMAGEBUTTON_IMAGE,
                                                                0, None)
            if iconData is not None and iconData != "":
                decoded = icontools.decodeIconData(iconData)
                img = QImage()
                img.loadFromData(decoded)
                self.setIconImage(img)
            else:
                self.setIconImage(None)
        else:
            self.setIconImage(None)
        self.update()

    def setIconImage(self, iconImage: Optional[QImage]):
        pass

    #region Drag & Drop

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
            action = getActionByID(actionID)

            actionInfo = ActionInfo(action.ident, self.ident, self.getType())
            profileName = profilemanager.getCurrentProfileName()
            profile = profilemanager.getProfileByName(profileName)
            if action is not None:
                profile.setAction(self.ident, actionInfo)
            else:
                profile.removeAction(self.ident)

            datarequests.updateProfile(profile)

            self.setAction(actionInfo)

            event.accept()
            return
        event.ignore()

    #endregion
