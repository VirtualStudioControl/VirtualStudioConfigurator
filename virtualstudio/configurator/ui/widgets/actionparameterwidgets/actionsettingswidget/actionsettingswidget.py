from typing import Any, Optional

from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget

from virtualstudio.common.structs.action.action_info import ActionInfo
from virtualstudio.common.structs.action.action_launcher import UI_TYPE_QTUI, UI_TYPE_INVALID, logengine
from virtualstudio.common.tools import icontools, actiondatatools
from virtualstudio.configurator.data import constants
from virtualstudio.configurator.ui.tools.autom import widgetctrl
from virtualstudio.configurator.ui.widgets.actionparameterwidgets.actionsettingswidget.ramfile import RamFile


class ActionSettingsWidget(QWidget):

    __loadNewUI = pyqtSignal(str, str)
    action: Optional[ActionInfo] = None
    logger = logengine.getLogger()

    def __init__(self, parent=None):
        self.action: Optional[ActionInfo] = None
        super(ActionSettingsWidget, self).__init__(parent=parent)

        self.__loadNewUI.connect(self.loadUI)

    def clearWidgets(self):
        for c in self.children():
            c.deleteLater()

        self.__dict__.clear()

    def setAction(self, action: Optional[ActionInfo]):
        self.clearWidgets()

        if self.action is not None:
            self.action.setDataChangedCallback(None)

        self.action = action

        def __callback(data: Any, type: str, success: bool):
            if not success:
                return
            self.__loadNewUI.emit(data, type)

        if action is None:
            return
        constants.DATA_PROVIDER.getActionWidget(action, __callback)
        self.action.setDataChangedCallback(self.loadUIValues)

    def loadUI(self, data: Any, type: str):
        if type == UI_TYPE_INVALID:
            return

        if type == UI_TYPE_QTUI:
            self.logger.info("Loading QTUI")
            self.loadQTUI(icontools.decodeIconData(data))
            self.connectCallbacks()

        if self.action is not None:
            try:
                self.loadUIValues()
            except Exception as ex:
                self.logger.exception(ex)

    def loadQTUI(self, data: bytes):
        buffer = RamFile(data)
        try:
            uic.loadUi(buffer, self)
            self.update()
        except Exception as ex:
            self.logger.exception(ex)

    def loadUIValues(self):
        if self.action is None:
            self.logger.info("Action is None")
            return

        gui_values = actiondatatools.getValue(self.action.actionParams, actiondatatools.KEY_GUI)

        if gui_values is None:
            self.logger.info("GUI Values is None")
            return

        for name in gui_values:
            try:
                if name in self.__dict__:
                    widget = self.__dict__[name]
                    self.logger.debug("Processing Widget: " + name)
                    if widget is not None:
                        widgetctrl.setParamsSilent(widget, gui_values[name])
                    else:
                        self.logger.info("GUI Widget is None")
            except Exception as ex:
                self.logger.exception(ex)

    def __createCallback(self, name, action: Optional[ActionInfo]):
        def __cb():
            def __setDataCB(success: bool):
                pass
            if self.action is None:
                return
            widget = self.__dict__[name]

            params = widgetctrl.getParams(widget)
            data = {}
            actiondatatools.updateValue(data, actiondatatools.KEY_GUI, {name: params})
            constants.DATA_PROVIDER.setActionData(action, data, __setDataCB)
            actiondatatools.merge(action.actionParams, data)

        return __cb

    def connectCallbacks(self):
        for var in self.__dict__:
            widgetctrl.setCallback(self.__dict__[var], self.__createCallback(var, self.action))
