from typing import Optional

from PyQt5.QtCore import Qt, QObject
from PyQt5.QtGui import QGradient, QBrush, QImage
from PyQt5.QtWidgets import QGraphicsScene

from virtualstudio.common.structs.action.action_info import ActionInfo

from virtualstudio.common.tools import actiondatatools as actionTools
from virtualstudio.common.tools import icontools

class ImagebuttonPreviewScene(QGraphicsScene):

    def __init__(self, parent: QObject = None):
        super().__init__(parent)

        self.setBackgroundBrush(Qt.black)

        self.borderOffset = 5

        self.isMoveEvent = False
        self.isMouseTranslateStart = False

        self.action: Optional[ActionInfo] = None
        self.currentState = 0
        self.currentImage = QImage()

    def setAction(self, action: ActionInfo):
        self.action = action
        self.currentState = 0
        self.updateImageFromAction()

    def setState(self, state: int):
        self.currentState = state
        self.updateImageFromAction()

    def updateImageFromAction(self):
        image = actionTools.getValue(data=self.action.actionParams, key=actionTools.KEY_STATE_IMAGEBUTTON_IMAGE,
                                     state=self.currentState)
        if image is not None:
            imageData = icontools.decodeIconData(image)
            self.currentImage.loadFromData(imageData)