from typing import Optional

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from ...profilemanager import profileset_manager as ProfilesetManager
from ...devicemanager import devicemanager

from ..tools.widgettools import setComboTextSilent, setComboIndexSilent

from ..widgets.actions.model.actionmodel import ActionModel
from ..widgets.actions.editor.actionwidget import ActionWidget
from ..widgets.docks.closeabledock import CloseableDock
from ..widgets.hardwareview import HardwareViewWidget
from ..widgets.hardware.hardwaregraphic import *
from ..widgets.actionparameterwidgets.imagebutton_image_preview_widget import ImageButtonImagePreviewWidget
from ..widgets.actionparameterwidgets.state_display_widget import StateDisplayWidget

from ...data import constants

from virtualstudio.common.io.configtools import *
from virtualstudio.common.structs.action.abstract_action import *
from ...history.actions.abstract_history_action import AbstractHistoryAction
from ...history.actions.action_value_changed import ActionValueChanged

DEVICES = {
    "Elgato Stream Deck Mini": createElgatoStreamdeckMini(),
    "Elgato Stream Deck Original": createElgatoStreamdeck(),
    "Elgato Stream Deck Original (V2)": createElgatoStreamdeck(),
    "Elgato Stream Deck XL": createElgatoStreamdeckXL(),
    "Behringer X-Touch Compact": createXTouchCompact(),
    "Behringer X-Touch Mini": createXTouchMini(),
}

DEVICE_DATA_ROLE = Qt.UserRole

CONTROL_WIDGET_TYPES = {
    CONTROL_TYPE_NONE: 0,
    CONTROL_TYPE_ANY: 0,
    CONTROL_TYPE_BUTTON: 1,
    CONTROL_TYPE_IMAGE_BUTTON: 2,
    CONTROL_TYPE_FADER: 3,
    CONTROL_TYPE_ROTARY_ENCODER: 4
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
        self.button_addprofile: Optional[QToolButton] = None

        self.device_param_widget: Optional[QStackedWidget] = None

        self.actionSettingsRootWidget: Optional[QStackedWidget] = None
        self.controlConfigurationRoot: Optional[QStackedWidget] = None

        self.state_display_widget: Optional[StateDisplayWidget] = None

        self.label_control_button_identifier: Optional[QLabel] = None

        self.label_control_imagebutton_identifier: Optional[QLabel] = None
        self.action_imagebutton_image_preview: Optional[ImageButtonImagePreviewWidget] = None

        self.label_control_fader_identifier: Optional[QLabel] = None
        self.label_control_rotaryencoder_identifier: Optional[QLabel] = None

        self.actionSettingWidget: Optional[QWidget] = None
        self.action_list_widget: Optional[QTreeView] = None


        uic.loadUi('GUI/windows/mainwindow.ui', self)

        for device in DEVICES:
            writeJSON("config/devices/" + device.replace(" ", "_") + ".device.json", DEVICES[device].toDict())

        self.deviceView.setHardwareOptionWidget(self.device_param_widget)

        self.setupDocks()
        self.setupUIActions()
        self.setupInteractiveWidgets()

        self.setupDebugActions()

    #region Debugging

    def setupDebugActions(self):
        self.actionDebugLogHistory.triggered.connect(self.onLogHistory)

    def onLogHistory(self, triggered=False):
        print("Current History:")
        index = 0
        for item in constants.HISTORY.getAllItems():
            print('\t', str(index), ":", item)
            index += 1
        print("      Position:", constants.HISTORY.getPosition())
        print("Undo Available:", constants.HISTORY.undoActionsAvailable())
        print("Redo Available:", constants.HISTORY.redoActionsAvailable())

    #endregion

    #region Docks

    def setupDocks(self):
        self.setCorner(Qt.Corner.BottomRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)
        self.setCorner(Qt.Corner.TopRightCorner, Qt.DockWidgetArea.RightDockWidgetArea)

    #endregion

    #region UI Actions
    def setupUIActions(self):
        self.actionUndo.triggered.connect(self.onUndo)
        self.actionRedo.triggered.connect(self.onRedo)

        self.actionFullscreen.toggled.connect(self.setFullscreen)

        self.bindActionToDock(self.actionDockActions, self.actionDock)
        self.bindActionToDock(self.actionDockActionSettings, self.actionSettingsDock)

    #region generators

    def bindActionToDock(self, action: QAction, dock: CloseableDock):
        def setDock(value):
            """
            :param value: if True, shows the ToolDock, else, closes the Tooldock
            """
            if value:
                dock.show()
            else:
                dock.close()

        def updateAction():
            action.setChecked(False)

        action.toggled.connect(setDock)
        dock.setOnClose(updateAction)

    #endregion

    #region Implementations

    def onUndo(self, triggered=False):
        """
        Action to Undo
        :param triggered:
        :return: None
        """

        action: AbstractHistoryAction = constants.HISTORY.undo()
        if action is not None:
            action.undoAction()

    def onRedo(self, triggered=False):
        """
        Action to Redo
        :param triggered:
        :return: None
        """
        action: AbstractHistoryAction = constants.HISTORY.redo()
        if action is not None:
            action.redoAction()

    def setFullscreen(self, triggered=False):
        """
        Sets the Window State of this Window

        :param value: if True, sets WindowState to FullScreen, else, sets WindowState to NoState
        """
        if triggered:
            self.setWindowState(Qt.WindowFullScreen)
        else:
            self.setWindowState(Qt.WindowNoState)

    #endregion

    #endregion

    #region Interactive Widgets
    def setupInteractiveWidgets(self):
        self.button_addprofile.clicked.connect(self._onAddProfileClicked)

        self.combo_profile.currentTextChanged.connect(self._onProfileChanged)

        self.actionSettingsRootWidget.setCurrentIndex(0)
        self.deviceView.setSelectionChangeHandler(self.__onActionItemSelectionChanged)

        constants.DATA_PROVIDER.listDevices(self._setupDevices)
        constants.DATA_PROVIDER.listActions(self._setupActions)

    #region Actions
    def _setupActions(self, actions_loaded: bool, actions: list, categoryIcons: list):
        if not actions_loaded:
            return

        model = ActionModel(0, 1, self)

        model.addActions(actions)

        self.action_list_widget.setModel(model)
        self.action_list_widget.setUniformRowHeights(True)
        self.action_list_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        self.action_list_widget.setItemDelegateForColumn(0, ActionWidget(self.action_list_widget, categoryIcons))

    def __onActionItemSelectionChanged(self, control: AbstractControlGraphic):
        if control is not None and control.action is not None:
            self.controlConfigurationRoot.setCurrentIndex(CONTROL_WIDGET_TYPES[control.getType()])
            self.updateControlWidgets(control)
            self.actionSettingsRootWidget.setCurrentIndex(1)
        else:
            self.actionSettingsRootWidget.setCurrentIndex(0)

    def updateControlWidgets(self, control: AbstractControlGraphic):

        #region General
        self.state_display_widget.updateWidget(control.action)
        #endregion

        #region BUTTON
        self.label_control_button_identifier.setText(str(control.ident))
        #endregion

        # region ImageButton
        self.label_control_imagebutton_identifier.setText(str(control.ident))
        #endregion

        # region Fader
        self.label_control_fader_identifier.setText(str(control.ident))
        #endregion

        # region Rotary Encoder
        self.label_control_rotaryencoder_identifier.setText(str(control.ident))
        #endregion

    #endregion

    #region Devices
    def _setupDevices(self, devices_loaded: bool, devices: list):
        if not devices_loaded:
            return

        for d in devices:
            devicemanager.appendDevice(d)
            self.combo_device.addItem("{} {}".format(d['manufacturer'], d['name']), userData=d["identifier"])
        self.combo_device.update()

        self.combo_device.currentTextChanged.connect(self.__setHardwareOnce)
        self.combo_device.setCurrentIndex(0)
        self.combo_device.currentTextChanged.connect(self.onHardwareChanged)

        self.combo_device_prev_value = self.combo_device.currentText()

    def onHardwareChanged(self, text=""):
        try:
            constants.HISTORY.addItem(ActionValueChanged(func=self.__setHardwareSilent,
                                                         old=self.combo_device_prev_value, new=text))
        except Exception as ex:
            print(ex)

        self.combo_device_prev_value = text
        self.__setHardware(text)

    def __setHardwareSilent(self, text: str):
        setComboTextSilent(self.combo_device, text)
        self.__setHardware(text)

    def __setHardwareOnce(self, text=""):
        self.combo_device.currentTextChanged.disconnect(self.__setHardwareOnce)
        self.__setHardware(text)

    def __setHardware(self, text: str):
        device = self.combo_device.currentData(DEVICE_DATA_ROLE)
        constants.CURRENT_DEVICE = device
        ProfilesetManager.expectNewProfileSet()
        #ProfilesetManager.setCurrentProfile(device["currentProfile"])
        constants.DATA_PROVIDER.getProfileSet(device, self.onProfileSetUpdate)
        self.deviceView.setHardware(DEVICES[text], devicemanager.getDevice(device))

    #endregion
    #region Profiles

    def _onProfileChanged(self, text):
        previousProfileName = ProfilesetManager.getCurrentProfileName()
        try:
            constants.HISTORY.addItem(ActionValueChanged(func=self.__changeProfile,
                                                         old=previousProfileName, new=text))
        except Exception as ex:
            print(ex)
        self.__profileChanged(text)

    def __profileChanged(self, profileName):
        def __profileChangedCB(success):
            pass
        constants.DATA_PROVIDER.setCurrentProfile(constants.CURRENT_DEVICE, profileName,
                                                  __profileChangedCB)
        ProfilesetManager.setCurrentProfile(profileName)
        data = self.combo_device.currentData(DEVICE_DATA_ROLE)
        devicemanager.setCurrentProfile(devicemanager.getDevice(data), profileName)
        self.deviceView.updateProfile()

    def __changeProfile(self, profileName):
        setComboTextSilent(self.combo_profile, profileName)
        self.__profileChanged(profileName)

    def onProfileSetUpdate(self, profileset: dict):

        ProfilesetManager.loadProfileSetFromDict(profileset)
        self.__setProfileCombobox(profileset["profiles"])
        ProfilesetManager.setCurrentProfile(devicemanager.getDevice(constants.CURRENT_DEVICE)["currentProfile"])
        self.__changeProfile(devicemanager.getDevice(constants.CURRENT_DEVICE)["currentProfile"])

    def __setProfileCombobox(self, profiles: list):
        self.combo_profile.clear()
        self.combo_profile.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically)

        def __sort(e):
            return e["name"]

        profiles.sort(key=__sort)

        for profile in profiles:
            self.combo_profile.addItem("{}".format(profile['name']), userData=profile)

        currentProfile = ProfilesetManager.getCurrentProfileName()
        setComboIndexSilent(self.combo_profile, max(0, self.combo_profile.findText(currentProfile)))

    def _onAddProfileClicked(self, checked=False):
        name, doProceed = QInputDialog.getText(self, "Add Profile", "Name", flags=Qt.Popup)

        if not doProceed:
            return

        device = devicemanager.getDevice(self.combo_device.currentData(DEVICE_DATA_ROLE))
        family = "{} {}".format(device["manufacturer"], device["name"])
        profile = Profile(hardwareFamily=family, name=name)
        constants.DATA_PROVIDER.addProfile(device["identifier"], profile, self.__onProfileAdded)

    def __onProfileAdded(self, profileset: dict, success: bool):
        if success:
            self.onProfileSetUpdate(profileset)
    #endregion
    #endregion