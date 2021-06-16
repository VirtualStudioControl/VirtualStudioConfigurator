from typing import Callable, Optional, Dict

from PyQt5.QtWidgets import QGraphicsItem

from virtualstudio.configurator.history.actions.action_value_changed import ActionValueChanged
from virtualstudio.configurator.ui.widgets.hardware.controls.abstractcontrolgraphic import AbstractControlGraphic
from virtualstudio.configurator.data import constants


class SelectionManager:

    def __init__(self, scene):
        super(SelectionManager, self).__init__()
        self.scene = scene
        self.deviceID: Optional[str] = None
        self.selectedControl: Optional[Dict[str, AbstractControlGraphic]] = {}
        self.onSelectionChangeCB: Optional[Callable[[Optional[AbstractControlGraphic]], None]] = None

    def setDevice(self, deviceID: str):
        self.deviceID = deviceID
        if deviceID not in self.selectedControl:
            self.selectedControl[deviceID] = None
        self.onSelectionChange(self.selectedControl[self.deviceID])

    def setSelected(self, control: Optional[AbstractControlGraphic]):
        if self.deviceID is None or self.selectedControl[self.deviceID] == control:
            return

        constants.HISTORY.addItem(ActionValueChanged(func=self.__setSelected, old=self.selectedControl[self.deviceID],
                                                     new=control))

        self.__setSelected(control)

    def __setSelected(self, control: Optional[AbstractControlGraphic]):
        if self.deviceID is None or self.selectedControl[self.deviceID] == control:
            return

        if control is not None and not control.selectable:
            control = None

        if self.selectedControl[self.deviceID] is not None:
            self.selectedControl[self.deviceID].isSelected = False
        if control is not None:
            control.isSelected = True
        self.selectedControl[self.deviceID] = control
        self.scene.update()
        self.onSelectionChange(self.selectedControl[self.deviceID])

    def onSelectionChange(self, control: Optional[AbstractControlGraphic]):
        if self.onSelectionChangeCB is not None:
            self.onSelectionChangeCB(control)

    def setSelectionChangeHandler(self, handler: Callable[[Optional[AbstractControlGraphic]], None]):
        self.onSelectionChangeCB = handler
