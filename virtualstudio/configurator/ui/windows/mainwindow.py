from typing import Tuple

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QColor
from PyQt5 import uic

from virtualstudio.common.tools import actiondatatools
from virtualstudio.configurator.ui.widgets.actionparameterwidgets.actionsettingswidget.actionsettingswidget import ActionSettingsWidget
from ..widgets.general.color_selection_button import ColorSelectionButton
from ...profilemanager import profileset_manager as ProfilesetManager
from ...devicemanager import devicemanager

from ..tools.widgettools import *

from ..widgets.actions.model.actionmodel import ActionModel
from ..widgets.actions.editor.actionwidget import ActionWidget
from ..widgets.docks.closeabledock import CloseableDock
from ..widgets.hardwareview import HardwareViewWidget
from ..widgets.hardware.hardwaregraphic import *
from ..widgets.actionparameterwidgets.imagebutton_image_preview_widget import ImageButtonImagePreviewWidget
from ..widgets.actionparameterwidgets.state_display_widget import StateDisplayWidget

from ...data import constants, default_values

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

        self.label_control_imagebutton_choose_image: Optional[QToolButton] = None
        self.label_control_imagebutton_showtext: Optional[QToolButton] = None

        self.label_control_imagebutton_text: Optional[QPlainTextEdit] = None
        self.label_control_imagebutton_font: Optional[QFontComboBox] = None

        self.label_control_imagebutton_font_bold: Optional[QToolButton] = None
        self.label_control_imagebutton_font_italic: Optional[QToolButton] = None
        self.label_control_imagebutton_font_underline: Optional[QToolButton] = None
        self.label_control_imagebutton_font_strikeout: Optional[QToolButton] = None
        self.label_control_imagebutton_font_size: Optional[QSpinBox] = None

        self.label_control_imagebutton_font_align_v: Optional[QComboBox] = None
        self.label_control_imagebutton_font_align_h: Optional[QComboBox] = None

        self.label_control_imagebutton_font_foreground: Optional[ColorSelectionButton] = None
        self.label_control_imagebutton_font_outline: Optional[ColorSelectionButton] = None

        self.label_control_fader_identifier: Optional[QLabel] = None
        self.label_control_rotaryencoder_identifier: Optional[QLabel] = None

        self.actionSettingWidget: Optional[ActionSettingsWidget] = None
        self.action_list_widget: Optional[QTreeView] = None

        uic.loadUi('GUI/windows/mainwindow.ui', self)

        for device in DEVICES:
            writeJSON("config/devices/" + device.replace(" ", "_") + ".device.json", DEVICES[device].toDict())

        self.deviceView.setHardwareOptionWidget(self.device_param_widget)

        constants.DATA_PROVIDER.setupEvents()

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

        self.actionDeleteAction.triggered.connect(self.deleteSelectedAction)

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

    def deleteSelectedAction(self, triggered=False):
        """
        Deletes the action of the current

        :return: None
        """
        constants.SELECTED_CONTROL.setAction(None)


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

        self.setupControlWigets()

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

        constants.SELECTED_CONTROL = control

        if control is not None and control.action is not None:
            self.controlConfigurationRoot.setCurrentIndex(CONTROL_WIDGET_TYPES[control.getType()])
            self.updateControlWidgets(control)
            self.actionSettingsRootWidget.setCurrentIndex(1)
        else:
            self.actionSettingsRootWidget.setCurrentIndex(0)
            self.actionSettingWidget.setAction(None)

    def __onStateChanged(self, state: int):
        try:
            self.updateControlWidgetState()
            self.action_imagebutton_image_preview.setState(state)
        except Exception as ex:
            import traceback
            traceback.print_exc()
            print(ex)

    #region Parameter Editor
    def setupControlWigets(self):

        self.combo_control_button_ledstate.currentIndexChanged.connect(self.onLedButtonLEDStateChanged)

        self.label_control_imagebutton_choose_image.clicked.connect(self.onChooseImagebuttonImage)
        self.label_control_imagebutton_showtext.clicked.connect(self.onShowImagebuttonText)

        self.label_control_imagebutton_text.textChanged.connect(self.onUpdateImagebuttonTextContent)
        self.label_control_imagebutton_font.currentFontChanged.connect(self.onImagebuttonFontChanged)

        self.label_control_imagebutton_font_bold.clicked.connect(self.onImagebuttonFontStyleChanged)
        self.label_control_imagebutton_font_italic.clicked.connect(self.onImagebuttonFontStyleChanged)
        self.label_control_imagebutton_font_underline.clicked.connect(self.onImagebuttonFontStyleChanged)
        self.label_control_imagebutton_font_strikeout.clicked.connect(self.onImagebuttonFontStyleChanged)
        self.label_control_imagebutton_font_size.valueChanged.connect(self.onImagebuttonFontSizeChanged)

        self.label_control_imagebutton_font_align_v.currentIndexChanged.connect(self.onImagebuttonTextAlignVChanged)
        self.label_control_imagebutton_font_align_h.currentIndexChanged.connect(self.onImagebuttonTextAlignHChanged)

        self.label_control_imagebutton_font_foreground.colorChanged.connect(self.onImagebuttonFontForegroundChanged)
        self.label_control_imagebutton_font_outline.colorChanged.connect(self.onImagebuttonFontOutlineChanged)

        self.combo_control_rotary_ringmode.currentIndexChanged.connect(self.onRotaryEncoderRingModeChanged)

        self.state_display_widget.setStateChangedCallback(self.__onStateChanged)

    def sendActionStateData(self, action: ActionInfo):
        def __setDataCB(success: bool):
            pass
        constants.DATA_PROVIDER.setActionData(action, {'states': action.actionParams['states']}, __setDataCB)

    #region LED Button Control Handlers
    def onLedButtonLEDStateChanged(self, index):
        def __set(index: int):
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_BUTTON_LEDSTATE,
                                     index,
                                     self.state_display_widget.currentState)
            self.sendActionStateData(constants.SELECTED_CONTROL.action)

        def __history(index: int):
            setComboIndexSilent(self.combo_control_button_ledstate, index)
            __set(index)

        prevVal = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_BUTTON_LEDSTATE,
                                           self.state_display_widget.currentState,
                                           default_values.BUTTON_LED_STATE)
        constants.HISTORY.addItem(ActionValueChanged(func=__history,
                                                     old=prevVal,
                                                     new=index))

        __set(index)
    #endregion

    #region Rotary Encoder Control Handlers
    def onRotaryEncoderRingModeChanged(self, index):
        def __set(index: int):
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_ROTARYENCODER_LEDRINGMODE,
                                     index,
                                     self.state_display_widget.currentState)
            self.sendActionStateData(constants.SELECTED_CONTROL.action)

        def __history(index: int):
            setComboIndexSilent(self.combo_control_rotary_ringmode, index)
            __set(index)

        prevVal = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_ROTARYENCODER_LEDRINGMODE,
                                           self.state_display_widget.currentState,
                                           default_values.ROTARY_LEDRING_MODE)
        constants.HISTORY.addItem(ActionValueChanged(func=__history,
                                                     old=prevVal,
                                                     new=index))

        __set(index)
    #endregion

    #region Imagebutton control Handlers
    def onChooseImagebuttonImage(self, checked=False):
        path = QFileDialog.getOpenFileName(self, "Select Image", constants.IMAGEDIALOG_LAST_PATH, constants.FILTER_FILEDIALOG_IMAGEFILES)[0]
        if path == "":
            return # Canceled Loading

        def __set(path: str):
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_IMAGE_BASE,
                                     None,
                                     self.state_display_widget.currentState)

            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_IMAGE_SRC,
                                     path,
                                     self.state_display_widget.currentState)
            self.action_imagebutton_image_preview.updateImage()

            self.sendActionStateData(constants.SELECTED_CONTROL.action)



        #TODO: Use better (per State) History Setter
        constants.HISTORY.addItem(ActionValueChanged(func=__set,
                                                     old=constants.IMAGEDIALOG_LAST_PATH,
                                                     new=path))
        constants.IMAGEDIALOG_LAST_PATH = path
        __set(path)

    def onShowImagebuttonText(self, checked=False):
        def __set(value: bool):
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                 actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_SHOW,
                                 value,
                                 self.state_display_widget.currentState)
            self.action_imagebutton_image_preview.updateImage()
            self.sendActionStateData(constants.SELECTED_CONTROL.action)

        def __history(value: bool):
            setButtonCheckedSilent(self.label_control_imagebutton_showtext, value)
            __set(value)

        prevVal = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_SHOW,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_SHOW)
        constants.HISTORY.addItem(ActionValueChanged(func=__history,
                                                     old=prevVal,
                                                     new=checked))
        __set(checked)

    def onUpdateImagebuttonTextContent(self):
        def __set(text: str):
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_TEXT,
                                     text,
                                     self.state_display_widget.currentState)
            self.action_imagebutton_image_preview.updateImage()
            self.sendActionStateData(constants.SELECTED_CONTROL.action)

        def __history(text: str):
            setPlainTextEditSilent(self.label_control_imagebutton_text, text)
            __set(text)

        text = self.label_control_imagebutton_text.toPlainText()

        prevVal = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_TEXT,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_TEXT)

        if prevVal != text:
            #TODO: Use PlainTextEdit's builtin Undo / Redo
            constants.HISTORY.addItem(ActionValueChanged(func=__history,
                                                         old=prevVal,
                                                         new=text))
        __set(text)

    def onImagebuttonFontChanged(self, font: QFont):
        def __set(font: QFont):
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_FONT,
                                     font.family(),
                                     self.state_display_widget.currentState)
            self.action_imagebutton_image_preview.updateImage()
            self.sendActionStateData(constants.SELECTED_CONTROL.action)

        def __history(font: QFont):
            setComboFontSilent(self.label_control_imagebutton_font, font)
            __set(font)

        prevVal = QFont(actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_FONT,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_FONT), self.font().pointSizeF())

        constants.HISTORY.addItem(ActionValueChanged(func=__history,
                                                     old=prevVal,
                                                     new=font))
        __set(font)

    def onImagebuttonFontStyleChanged (self, checked=False):
        def __set(states: Tuple[bool, bool, bool, bool]):
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_BOLD,
                                     states[0],
                                     self.state_display_widget.currentState)
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ITALICS,
                                     states[1],
                                     self.state_display_widget.currentState)
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_UNDERLINE,
                                     states[2],
                                     self.state_display_widget.currentState)
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_STRIKETHROUGH,
                                     states[3],
                                     self.state_display_widget.currentState)
            self.action_imagebutton_image_preview.updateImage()
            self.sendActionStateData(constants.SELECTED_CONTROL.action)


        def __history(states: Tuple[bool, bool, bool, bool]):
            setButtonCheckedSilent(self.label_control_imagebutton_font_bold, states[0])
            setButtonCheckedSilent(self.label_control_imagebutton_font_italic, states[1])
            setButtonCheckedSilent(self.label_control_imagebutton_font_underline, states[2])
            setButtonCheckedSilent(self.label_control_imagebutton_font_strikeout, states[3])

            __set(states)

        flags = (self.label_control_imagebutton_font_bold.isChecked(),
                 self.label_control_imagebutton_font_italic.isChecked(),
                 self.label_control_imagebutton_font_underline.isChecked(),
                 self.label_control_imagebutton_font_strikeout.isChecked())

        prevVal = (actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                 actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_BOLD,
                                 self.state_display_widget.currentState,
                                 default_values.IMAGEBUTTON_TEXT_BOLD),
        actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                 actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ITALICS,
                                 self.state_display_widget.currentState,
                                 default_values.IMAGEBUTTON_TEXT_ITALICS),
        actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                 actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_UNDERLINE,
                                 self.state_display_widget.currentState,
                                 default_values.IMAGEBUTTON_TEXT_UNDERLINE),
        actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                 actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_STRIKETHROUGH,
                                 self.state_display_widget.currentState,
                                 default_values.IMAGEBUTTON_TEXT_STRIKETHROUGH))

        constants.HISTORY.addItem(ActionValueChanged(func=__history,
                                                     old=prevVal,
                                                     new=flags))
        __set(flags)

    def onImagebuttonFontSizeChanged (self, value):
        def __set(value: int):
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_FONTSIZE,
                                     value,
                                     self.state_display_widget.currentState)
            self.action_imagebutton_image_preview.updateImage()
            self.sendActionStateData(constants.SELECTED_CONTROL.action)

        def __history(value: int):
            setValueQSpinSilent(self.label_control_imagebutton_font_size, value)
            __set(value)

        prevVal = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_FONTSIZE,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_FONTSIZE)

        if prevVal != value:
            constants.HISTORY.addItem(ActionValueChanged(func=__history,
                                                         old=prevVal,
                                                         new=value))

        __set(value)

    def onImagebuttonTextAlignVChanged(self, index):
        def __set(index: int):
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ALIGNV,
                                     index,
                                     self.state_display_widget.currentState)
            self.action_imagebutton_image_preview.updateImage()
            self.sendActionStateData(constants.SELECTED_CONTROL.action)

        def __history(index: int):
            setComboIndexSilent(self.label_control_imagebutton_font_align_v, index)
            __set(index)

        prevVal = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ALIGNV,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_ALIGNV)
        constants.HISTORY.addItem(ActionValueChanged(func=__history,
                                                     old=prevVal,
                                                     new=index))

        __set(index)

    def onImagebuttonTextAlignHChanged(self, index):
        def __set(index: int):
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ALIGNH,
                                     index,
                                     self.state_display_widget.currentState)
            self.action_imagebutton_image_preview.updateImage()
            self.sendActionStateData(constants.SELECTED_CONTROL.action)

        def __history(index: int):
            setComboIndexSilent(self.label_control_imagebutton_font_align_h, index)
            __set(index)

        prevVal = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ALIGNH,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_ALIGNH)
        constants.HISTORY.addItem(ActionValueChanged(func=__history,
                                                     old=prevVal,
                                                     new=index))
        __set(index)

    def onImagebuttonFontForegroundChanged(self, color: QColor):
        def __set(color: QColor):
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_COLOR_FG,
                                     color.name(),
                                     self.state_display_widget.currentState)
            self.action_imagebutton_image_preview.updateImage()
            self.sendActionStateData(constants.SELECTED_CONTROL.action)

        def __history(color: str):
            col = QColor(color)
            self.label_control_imagebutton_font_foreground.setColor(col)
            __set(col)

        prevVal = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_COLOR_FG,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_COLOR_FG)
        constants.HISTORY.addItem(ActionValueChanged(func=__history,
                                                     old=prevVal,
                                                     new=color.name()))

        __set(color)

    def onImagebuttonFontOutlineChanged(self, color: QColor):
        def __set(color: QColor):
            actiondatatools.setValue(constants.SELECTED_CONTROL.action.actionParams,
                                     actiondatatools.KEY_STATE_IMAGEBUTTON_COLOR_BACKGROUND,
                                     color.name(),
                                     self.state_display_widget.currentState)
            self.action_imagebutton_image_preview.updateImage()
            self.sendActionStateData(constants.SELECTED_CONTROL.action)

        def __history(color: str):
            col = QColor(color)
            self.label_control_imagebutton_font_outline.setColor(col)
            __set(col)

        prevVal = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                                    actiondatatools.KEY_STATE_IMAGEBUTTON_COLOR_BACKGROUND,
                                                    self.state_display_widget.currentState,
                                                    default_values.IMAGEBUTTON_COLOR_BACKGROUND)
        constants.HISTORY.addItem(ActionValueChanged(func=__history,
                                                     old=prevVal,
                                                     new=color.name()))

        __set(color)

    #endregion

    def updateControlWidgets(self, control: AbstractControlGraphic):

        #region General
        self.state_display_widget.updateWidget(control.action)
        self.actionSettingWidget.setAction(control.action)
        #endregion

        #region BUTTON
        self.label_control_button_identifier.setText(str(control.ident))
        #endregion

        # region ImageButton
        self.label_control_imagebutton_identifier.setText(str(control.ident))
        self.action_imagebutton_image_preview.setState(0)
        #endregion

        # region Fader
        self.label_control_fader_identifier.setText(str(control.ident))
        #endregion

        # region Rotary Encoder
        self.label_control_rotaryencoder_identifier.setText(str(control.ident))
        #endregion

        self.updateControlWidgetState()
        self.action_imagebutton_image_preview.updateImage()

    def updateControlWidgetState(self):

        # region Ensure Default Values
        #region Button
        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_BUTTON_LEDSTATE,
                                           self.state_display_widget.currentState,
                                           default_values.BUTTON_LED_STATE)
        #endregion

        # region ImageButton
        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_SHOW,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_SHOW)

        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_TEXT,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_TEXT)

        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_FONT,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_FONT)

        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_BOLD,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_BOLD)

        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ITALICS,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_ITALICS)

        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_UNDERLINE,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_UNDERLINE)

        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_STRIKETHROUGH,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_STRIKETHROUGH)

        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_FONTSIZE,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_FONTSIZE)

        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ALIGNV,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_ALIGNV)

        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ALIGNH,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_ALIGNH)

        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_COLOR_FG,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_TEXT_COLOR_FG)

        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_IMAGEBUTTON_COLOR_BACKGROUND,
                                           self.state_display_widget.currentState,
                                           default_values.IMAGEBUTTON_COLOR_BACKGROUND)
        # endregion

        #region Rotary Encoder
        actiondatatools.ensureDefaultValue(constants.SELECTED_CONTROL.action.actionParams,
                                           actiondatatools.KEY_STATE_ROTARYENCODER_LEDRINGMODE,
                                           self.state_display_widget.currentState,
                                           default_values.ROTARY_LEDRING_MODE)
        #endregion

        # endregion

        #region Button
        setComboIndexSilent(self.combo_control_button_ledstate,
                            actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                                              actiondatatools.KEY_STATE_BUTTON_LEDSTATE,
                                                              self.state_display_widget.currentState,
                                                              default_values.BUTTON_LED_STATE))
        #endregion

        #region ImageButton
        setButtonCheckedSilent(self.label_control_imagebutton_showtext, actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_SHOW,
                                              self.state_display_widget.currentState,
                                              default_values.IMAGEBUTTON_TEXT_SHOW))

        setPlainTextEditSilent(self.label_control_imagebutton_text, actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_TEXT,
                                              self.state_display_widget.currentState,
                                              default_values.IMAGEBUTTON_TEXT_TEXT))

        setComboFontSilent(self.label_control_imagebutton_font, QFont(actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_FONT,
                                              self.state_display_widget.currentState,
                                              default_values.IMAGEBUTTON_TEXT_FONT), self.font().pointSizeF()))

        setButtonCheckedSilent(self.label_control_imagebutton_font_bold, actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_BOLD,
                                              self.state_display_widget.currentState,
                                              default_values.IMAGEBUTTON_TEXT_BOLD))

        setButtonCheckedSilent(self.label_control_imagebutton_font_italic, actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ITALICS,
                                              self.state_display_widget.currentState,
                                              default_values.IMAGEBUTTON_TEXT_ITALICS))

        setButtonCheckedSilent(self.label_control_imagebutton_font_underline, actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_UNDERLINE,
                                              self.state_display_widget.currentState,
                                              default_values.IMAGEBUTTON_TEXT_UNDERLINE))

        setButtonCheckedSilent(self.label_control_imagebutton_font_strikeout, actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_STRIKETHROUGH,
                                              self.state_display_widget.currentState,
                                              default_values.IMAGEBUTTON_TEXT_STRIKETHROUGH))

        setValueQSpinSilent(self.label_control_imagebutton_font_size, actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_FONTSIZE,
                                              self.state_display_widget.currentState,
                                              default_values.IMAGEBUTTON_TEXT_FONTSIZE))

        setComboIndexSilent(self.label_control_imagebutton_font_align_v, actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ALIGNV,
                                              self.state_display_widget.currentState,
                                              default_values.IMAGEBUTTON_TEXT_ALIGNV))

        setComboIndexSilent(self.label_control_imagebutton_font_align_h, actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ALIGNH,
                                              self.state_display_widget.currentState,
                                              default_values.IMAGEBUTTON_TEXT_ALIGNH))

        self.label_control_imagebutton_font_foreground.setColor(
            QColor(actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                                     actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_COLOR_FG,
                                                     self.state_display_widget.currentState,
                                                     default_values.IMAGEBUTTON_TEXT_COLOR_FG)))
        self.label_control_imagebutton_font_outline.setColor(
            QColor(actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                                     actiondatatools.KEY_STATE_IMAGEBUTTON_COLOR_BACKGROUND,
                                                     self.state_display_widget.currentState,
                                                     default_values.IMAGEBUTTON_COLOR_BACKGROUND)))
        #endregion

        #region Rotary Encoder
        setComboIndexSilent(self.combo_control_rotary_ringmode,
                            actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                                              actiondatatools.KEY_STATE_ROTARYENCODER_LEDRINGMODE,
                                                              self.state_display_widget.currentState,
                                                              default_values.ROTARY_LEDRING_MODE))
        #endregion

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

        self.action_imagebutton_image_preview.onDeviceChanged()

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