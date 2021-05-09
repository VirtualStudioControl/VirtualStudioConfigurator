from typing import Optional

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from ..widgets.actions.model.actionmodel import ActionModel
from ..widgets.actions.editor.actionwidget import ActionWidget
from ..widgets.hardwareview import HardwareViewWidget, QStandardItemModel
from ..widgets.hardware.hardwaregraphic import *

from virtualstudio.configurator.data import constants

from virtualstudio.common.io.configtools import *

DEVICES = {
    "Elgato Stream Deck Mini": createElgatoStreamdeckMini(),
    "Elgato Stream Deck Original": createElgatoStreamdeck(),
    "Elgato Stream Deck Original (V2)": createElgatoStreamdeck(),
    "Elgato Stream Deck XL": createElgatoStreamdeckXL(),
    "Behringer X-Touch Compact": createXTouchCompact(),
    "Behringer X-Touch Mini": createXTouchMini(),
}

class MainWindow(QMainWindow):

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

        self.deviceView: Optional[HardwareViewWidget] = None
        self.combo_device: Optional[QComboBox] = None
        self.combo_profile: Optional[QComboBox] = None
        self.device_param_widget: Optional[QStackedWidget] = None
        self.actionSettingWidget: Optional[QWidget] = None
        self.action_list_widget: Optional[QTreeView] = None

        uic.loadUi('GUI/windows/mainwindow.ui', self)

        for device in DEVICES:
            writeJSON("config/devices/" + device.replace(" ", "_") + ".device.json", DEVICES[device].toDict())

        self.deviceView.setHardwareOptionWidget(self.device_param_widget)

        self.setupInteractiveWidgets()

    def setupInteractiveWidgets(self):
        constants.DATA_PROVIDER.listDevices(self._setupDevices)
        constants.DATA_PROVIDER.listActions(self._setupActions)

    def _setupActions(self, actions_loaded: bool, actions: list, categoryIcons: list):
        if not actions_loaded:
            return

        model = ActionModel(0, 1, self)

        model.addActions(actions)

        self.action_list_widget.setModel(model)
        self.action_list_widget.setUniformRowHeights(True)
        self.action_list_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        self.action_list_widget.setItemDelegateForColumn(0, ActionWidget(self.action_list_widget, categoryIcons))

    def _setupDevices(self, devices_loaded: bool, devices: list):
        if not devices_loaded:
            return

        for d in devices:
            self.combo_device.addItem("{} {}".format(d['manufacturer'], d['name']), "{} {}".format(d['manufacturer'],
                                                                                                   d['name']))

        self.combo_device.currentTextChanged.connect(self.onHardwareChanged)
        self.combo_device.update()
        self.combo_device.setCurrentIndex(0)

    def onHardwareChanged(self, text=""):
        self.deviceView.setHardware(DEVICES[text])
