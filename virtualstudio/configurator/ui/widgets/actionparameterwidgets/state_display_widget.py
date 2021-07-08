from typing import List, Optional, Callable

from PyQt5.QtCore import QMargins, pyqtSignal
from PyQt5.QtWidgets import *

from virtualstudio.common.structs.action.action_info import ActionInfo
from ...tools.widgettools import setValueQRadioButtonSilent, setValueQRadioButton
from ....data import constants
from ....history.actions.action_value_changed import ActionValueChanged


class StateDisplayWidget(QWidget):

    __updateRadioButtons = pyqtSignal(int)

    def __init__(self, parent=None):
        super(StateDisplayWidget, self).__init__(parent)

        self.stateChangedCallback: Optional[Callable[[int], None]] = None
        self.currentState = 0
        self.currentStateCount = 0

        self.__updateRadioButtons.connect(self.__updateRadioBtns)

        self.radioButtons: List[QRadioButton] = []
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.insertStretch(-1, 2**16)
        self.layout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(self.layout)

    def createStateRadios(self, stateCount: int):
        for i in range(stateCount - len(self.radioButtons)):
            radioButton = QRadioButton()
            self.layout.insertWidget(0, radioButton)
            self.radioButtons.insert(0, radioButton)

            radioButton.toggled.connect(self.__createToggle(radioButton))

        self.setLayout(self.layout)

    def __createToggle(self, radioButton):
        def __onToggle(checked):
            index = self.radioButtons.index(radioButton)
            if checked:
                constants.HISTORY.addItem(ActionValueChanged(func=self.__setStateSilent, old=self.currentState, new=index))
                self.__changeState(index)

        return __onToggle

    def setStateChangedCallback(self, callback: Optional[Callable[[int], None]]):
        self.stateChangedCallback = callback

    def setState(self, state):
        setValueQRadioButton(self.radioButtons[state], True)

    def __setStateSilent(self, state):
        setValueQRadioButtonSilent(self.radioButtons[state], True)
        self.__changeState(state)

    def __changeState(self, state: int):
        self.currentState = state
        if self.stateChangedCallback is not None:
            self.stateChangedCallback(self.currentState)

    def updateWidget(self, action: ActionInfo):
        constants.DATA_PROVIDER.getActionStates(action, self.__changeStateCount)

    def __changeStateCount(self, statecount: int, success: bool):
        if not success:
            print("Statecount request Failed !")
            return

        self.currentStateCount = statecount
        self.__updateRadioButtons.emit(statecount)

    def __updateRadioBtns(self, statecount: int):
        if statecount <= 1:
            statecount = 0
        if statecount >= len(self.radioButtons):
            self.createStateRadios(statecount)

        if len(self.radioButtons) > 0:
            setValueQRadioButtonSilent(self.radioButtons[0], True)

        for i in range(len(self.radioButtons)):
            if i < statecount:
                self.radioButtons[i].show()
            else:
                self.radioButtons[i].hide()

        self.update()
