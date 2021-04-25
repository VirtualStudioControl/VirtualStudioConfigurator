from typing import Optional

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .hardware.hardwarescene import HardwareScene
from .hardware.hardwaregraphic import HardwareGraphic

class HardwareViewWidget(QGraphicsView):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.initUI()

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 8
        self.zoomStep = 1
        self.zoomRange = [0, 16]

        self.hardware: Optional[HardwareGraphic] = None
        self.hardware_widget: Optional[QStackedWidget] = None

        self.devicePageDict = {}

        self.scene = HardwareScene()
        self.setScene(self.scene)

    def initUI(self):
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        # enable dropping
        self.setAcceptDrops(True)

    def setHardwareOptionWidget(self, widget : QWidget):
        self.hardware_widget = widget

    def setHardware(self, hardware: HardwareGraphic):
        self.hardware = hardware
        self.scene.setHardware(hardware)
        self.generateHardwareWidgetContent()

    def generateHardwareWidgetContent(self):
        if self.hardware.name in self.devicePageDict:
            self.hardware_widget.setCurrentIndex(self.devicePageDict[self.hardware.name])
            return

        widget = QWidget()
        layout: QGridLayout = QGridLayout()

        layout.addWidget(QWidget(), 0, 0)

        if self.hardware.layers > 1:
            layerLabel = QLabel()
            layerLabel.setText("Layer")
            layout.addWidget(layerLabel, 1, 0)

            layout_combo = QComboBox()

            for layer in range(self.hardware.layers):
                layout_combo.addItem(self.hardware.getNameOfLayer(layer))
            layout.addWidget(layout_combo, 1, 1)
            layout_combo.currentIndexChanged.connect(self.onLayerChanged)

        layout.setContentsMargins(0,0,0,0)

        widget.setLayout(layout)
        self.devicePageDict[self.hardware.name] = self.hardware_widget.insertWidget(len(self.devicePageDict), widget)
        self.hardware_widget.setCurrentIndex(self.devicePageDict[self.hardware.name])
        self.hardware_widget.update()

    def onLayerChanged(self, index):
        self.hardware.setActiveLayer(index)

    def wheelEvent(self, event:QWheelEvent):
        zoomOutFactor = 1 / self.zoomInFactor

        # calculate zoom
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep


        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        # set scene scale
        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)
