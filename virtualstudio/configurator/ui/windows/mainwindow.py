from typing import Optional

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from ..widgets.hardwareview import HardwareViewWidget
from ..widgets.hardware.hardwaregraphic import *

from virutalstudio.common.io.configtools import *

DEVICES = {
    "StreamDeck": createElgatoStreamdeck(),
    "StreamDeck XL": createElgatoStreamdeckXL(),
    "StreamDeck Mini": createElgatoStreamdeckMini(),
    "Behringer X Touch Compact": createXTouchCompact(),
    "Behringer X Touch Mini": createXTouchMini(),
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

        uic.loadUi('GUI/windows/mainwindow.ui', self)

        for device in DEVICES:
            writeJSON("config/devices/" + device.replace(" ", "_") + ".device.json", DEVICES[device].toDict())

        self.deviceView.setHardwareOptionWidget(self.device_param_widget)

        self.setupInteractiveWidgets()

    def setupInteractiveWidgets(self):
        for d in DEVICES:
            self.combo_device.addItem(d)

        self.combo_device.currentTextChanged.connect(self.onHardwareChanged)

        self.deviceView.setHardware(DEVICES[self.combo_device.currentText()])

    def onHardwareChanged(self, text=""):
        self.deviceView.setHardware(DEVICES[text])
