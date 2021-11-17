from typing import Optional, Dict, Any, Callable

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from ..tools.widgettools import setComboIndexSilent

from .hardware.hardwarescene import HardwareScene, AbstractControlGraphic
from .hardware.hardwaregraphic import HardwareGraphic
from ...data import constants
from ...history.actions.action_value_changed import ActionValueChanged
from ...profilemanager import profileset_manager as profilemanager

SETTING_LAYER_INDEX = "layerIndex"

WIDGET_LAYER_COMBO = "layerCombo"

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
        self.hardwarePageDict = {}
        self.hardware_widget_dict: Dict[str, Dict[str, QWidget]] = {}

        self.device: Optional[Dict[str, Any]] = None
        self.deviceSettingsDict: Optional[Dict[str, Any]] = {}

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

    def canDropMimeData(self, data, action, row, column, parent):
        return True


    def updateProfile(self):
        currentProfile = profilemanager.getProfileByName(profilemanager.getCurrentProfileName())

        if self.hardware is not None:
            self.hardware.setProfile(currentProfile)

    def setHardwareOptionWidget(self, widget : QWidget):
        self.hardware_widget = widget

    def setSelectionChangeHandler(self, handler: Callable[[Optional[AbstractControlGraphic]], None]):
        self.scene.selectionManager.setSelectionChangeHandler(handler)

    def setHardware(self, hardware: HardwareGraphic, device: dict):
        self.hardware = hardware
        self.device = device
        self.scene.setHardware(hardware)
        self.scene.selectionManager.setDevice(device["identifier"])
        self.generateHardwareWidgetContent()

    def generateHardwareWidgetContent(self):
        if self.hardware.name in self.hardwarePageDict:
            self.hardware_widget.setCurrentIndex(self.hardwarePageDict[self.hardware.name])
            self.setDeviceSettings()
            return

        widget = QWidget()
        layout: QGridLayout = QGridLayout()

        layout.addWidget(QWidget(), 0, 0)
        settings = {}
        widgetdict: Dict[str, QWidget] = {}

        if self.hardware.layers > 1:
            layerLabel = QLabel()
            layerLabel.setText("Layer")
            layout.addWidget(layerLabel, 1, 0)

            layer_combo = QComboBox()

            for layer in range(self.hardware.layers):
                layer_combo.addItem(self.hardware.getNameOfLayer(layer))
            layout.addWidget(layer_combo, 1, 1)
            layer_combo.currentIndexChanged.connect(self.onLayerChanged)

            widgetdict[WIDGET_LAYER_COMBO] = layer_combo
            settings[SETTING_LAYER_INDEX] = 0

        layout.setContentsMargins(0,0,0,0)

        widget.setLayout(layout)

        self.deviceSettingsDict[self.device['identifier']] = settings
        self.hardware_widget_dict[self.hardware.name] = widgetdict
        self.hardwarePageDict[self.hardware.name] = self.hardware_widget.insertWidget(len(self.hardwarePageDict), widget)
        self.hardware_widget.setCurrentIndex(self.hardwarePageDict[self.hardware.name])
        self.hardware_widget.update()

    def setDeviceSettings(self):
        settings = self.deviceSettingsDict[self.device['identifier']]
        widgets = self.hardware_widget_dict[self.hardware.name]

        if SETTING_LAYER_INDEX in settings:
            self.__onLayerChangedSilent(settings[SETTING_LAYER_INDEX], widgets[WIDGET_LAYER_COMBO])

    def onLayerChanged(self, index):
        def __wrapAction(index: int):
            self.__onLayerChangedSilent(index, self.hardware_widget_dict[self.hardware.name][WIDGET_LAYER_COMBO])
        try:
            constants.HISTORY.addItem(
                ActionValueChanged(func=__wrapAction,
                                   old=self.deviceSettingsDict[self.device['identifier']][SETTING_LAYER_INDEX],
                                   new=index))
        except Exception as ex:
            print(ex)
        self.__onLayerChanged(index)

    def __onLayerChangedSilent(self, index, widget):
        setComboIndexSilent(widget, index)
        self.__onLayerChanged(index)

    def __onLayerChanged(self, index):
        self.deviceSettingsDict[self.device['identifier']][SETTING_LAYER_INDEX] = index
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