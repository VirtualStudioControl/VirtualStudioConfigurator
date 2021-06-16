from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *

from virtualstudio.common.structs.action.action_info import ActionInfo
from .imagebuttonpreview_graphics.imagebutton_preview_scene import ImagebuttonPreviewScene

class ImageButtonImagePreviewWidget(QGraphicsView):

    def __init__(self, parent=None):
        super(ImageButtonImagePreviewWidget, self).__init__(parent)

        self.scene = ImagebuttonPreviewScene()
        self.setSceneRect(-32, -32, 64, 64)
        self.setScene(self.scene)

        self.initUI()

    def initUI(self):
        self.setRenderHints(
            QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

        # enable dropping
        self.setAcceptDrops(True)

    def updateWidget(self, action: ActionInfo):
        self.scene.setAction(action)

    def setState(self, state: int):
        self.scene.setState(state)