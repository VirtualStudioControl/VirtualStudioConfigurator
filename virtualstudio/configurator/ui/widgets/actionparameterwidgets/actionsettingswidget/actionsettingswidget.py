from typing import Any, Optional

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from virtualstudio.common.structs.action.action_info import ActionInfo
from virtualstudio.common.structs.action.action_launcher import UI_TYPE_QTUI, UI_TYPE_INVALID
from virtualstudio.common.tools import icontools, actiondatatools
from virtualstudio.configurator.data import constants
from virtualstudio.configurator.ui.tools.autom import widgetctrl
from virtualstudio.configurator.ui.widgets.actionparameterwidgets.actionsettingswidget.ramfile import RamFile


class ActionSettingsWidget(QWidget):

    __loadNewUI = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(ActionSettingsWidget, self).__init__(parent=parent)

        self.action = None

        self.__loadNewUI.connect(self.loadUI)

        print(self.__dict__)

    def clearWidgets(self):
        for c in self.children():
            c.deleteLater()

        self.__dict__.clear()

    def setAction(self, action: Optional[ActionInfo]):
        self.clearWidgets()

        self.action = action

        def __callback(data: Any, type: str, success: bool):
            if not success:
                return
            self.__loadNewUI.emit(data, type)

        if action is None:
            return
        constants.DATA_PROVIDER.getActionWidget(action, __callback)

    def loadUI(self, data: Any, type: str):
        if type == UI_TYPE_INVALID:
            return

        if type == UI_TYPE_QTUI:
            self.loadQTUI(icontools.decodeIconData(data))
            self.connectCallbacks()
            return

    def loadQTUI(self, data: bytes):
        buffer = RamFile(data)
        uic.loadUi(buffer, self)
        self.update()

    def __createCallback(self, name, action: Optional[ActionInfo]):
        def __cb():
            def __setDataCB(success: bool):
                pass
            if self.action is None:
                return
            widget = self.__dict__[name]
            try:
                params = widgetctrl.getParams(widget)
                print(name, params)
                data = {}
                actiondatatools.updateValue(data, actiondatatools.KEY_GUI, {name: params})
                constants.DATA_PROVIDER.setActionData(action, data, __setDataCB)
                actiondatatools.merge(action.actionParams, data)
            except Exception as ex:
                print(ex)
                import traceback
                traceback.print_exc()

        return __cb

    def connectCallbacks(self):
        for var in self.__dict__:
            widgetctrl.setCallback(self.__dict__[var], self.__createCallback(var, self.action))
