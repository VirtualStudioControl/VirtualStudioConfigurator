from typing import Any, Callable, Dict, List, Union

from PyQt5.QtCore import QDateTime, Qt, QDate, QTime
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import *

from virtualstudio.common.logging import logengine
from virtualstudio.configurator.ui.widgets.general.color_selection_button import ColorSelectionButton
from virtualstudio.configurator.ui.widgets.general.file_selection_button import FileSelectionButton

logger = logengine.getLogger()

PRIMITIVES = Union[bool, float, int, str]
PRIMITIVE_LISTS = Union[bool, float, int, str, List[PRIMITIVES]]

#region Tools


def __hasArrtibType(object, methodName, type):
    if hasattr(object, methodName):
        if isinstance(getattr(object, methodName), type):
            return True
    return False


def __hasMethod(object, methodName):
    if hasattr(object, methodName):
        if callable(getattr(object, methodName)):
            return True
    return False


def __toPrimitive(object: Any):

    if isinstance(object, (bool, float, int, str, list)):
        return object

    if type(object) in DICT_TYPECAST_OBJTOPRIM:
        return DICT_TYPECAST_OBJTOPRIM[type(object)](object)

    return None


def __fromPrimitive(type, object):
    if type is None:
        return object

    if type in (bool, float, int, str, list):
        return object

    if type in DICT_TYPECAST_OBJTOPRIM:
        return DICT_TYPECAST_OBJTOPRIM[type](object)

    return None


def __addParamToDict(widget: QWidget, dict: Dict[str, PRIMITIVE_LISTS], functionName, paramName, args=None) -> Dict[str, PRIMITIVE_LISTS]:
    if args is None:
        args = []
    if hasattr(widget, functionName):
        value = widget.__getattribute__(functionName)(*args)
        dict[paramName] = __toPrimitive(value)

    return dict


def __applyParamToWidget(widget: QWidget, dict: Dict[str, PRIMITIVE_LISTS], functionName,
                         paramName, paramType: type = None,
                         args=None) -> None:
    if paramName not in dict or dict[paramName] is None:
        return
    if args is None:
        args = []
    if __hasMethod(widget, functionName):
        widget.__getattribute__(functionName)(__fromPrimitive(paramType, dict[paramName]), *args)


def __applyParamToWidgetNullable(widget: QWidget, dict: Dict[str, PRIMITIVE_LISTS], functionName,
                                 functionNameNullable,
                                 paramName, paramType: type = None,
                                 args=None) -> None:
    if args is None:
        args = []
    if paramName not in dict or dict[paramName] is None:
        if __hasMethod(widget, functionNameNullable):
            widget.__getattribute__(functionNameNullable)()
    elif __hasMethod(widget, functionName):
        widget.__getattribute__(functionName)(__fromPrimitive(paramType, dict[paramName]), *args)

#endregion

#region Type Specific functions

#region SetValue
def __setValueButton(widget: QWidget, value: Any) -> bool:
    if not __hasMethod(widget, "setChecked") or not isinstance(value, bool):
        return False
    widget.setChecked(value)
    return True


def __setValueInt(widget: QWidget, value: Any) -> bool:
    if not __hasMethod(widget, "setValue") or not isinstance(value, int):
        return False
    widget.setValue(value)
    return True


def __setValueFloat(widget: QWidget, value: Any) -> bool:
    if not __hasMethod(widget, "setValue") or not isinstance(value, float):
        return False
    widget.setValue(value)
    return True


def __setValueCombobox(widget: QWidget, value: Any) -> bool:
    if isinstance(value, str):
        if not __hasMethod(widget, "setCurrentText"):
            return False
        widget.setCurrentText(value)
        return True
    elif isinstance(value, int):
        if not __hasMethod(widget, "setCurrentIndex"):
            return False
        widget.setCurrentIndex(value)
        return True
    elif isinstance(value, QFont):
        if not __hasMethod(widget, "setCurrentFont"):
            return False
        widget.setCurrentFont(value)
        return True
    elif isinstance(value, list):
        if not __hasMethod(widget, "addItems") and not __hasMethod(widget, "clear"):
            return False
        widget.clear()
        widget.addItems(value)
        return True
    return False


def __setValueDateTimeEdit(widget: QWidget, value: Any) -> bool:
    if isinstance(value, str):
        if not __hasMethod(widget, "setDateTime"):
            return False
        datetime = QDateTime()
        datetime.fromString(value, Qt.ISODateWithMs)
        widget.setDateTime(datetime)
        return True
    elif isinstance(value, int):
        if not __hasMethod(widget, "setDateTime"):
            return False
        datetime = QDateTime()
        datetime.fromMSecsSinceEpoch(value)
        widget.setDateTime(datetime)
        return True
    elif isinstance(value, float):
        if not __hasMethod(widget, "setDateTime"):
            return False
        datetime = QDateTime()
        datetime.fromSecsSinceEpoch(value)
        widget.setDateTime(datetime)
        return True
    elif isinstance(value, QDateTime):
        if not __hasMethod(widget, "setDateTime"):
            return False
        widget.setDateTime(value)
        return True
    return False


def __setValueLCDNumber(widget: QWidget, value: Any) -> bool:
    if isinstance(value, str):
        if not __hasMethod(widget, "display"):
            return False
        widget.display(value)
        return True
    elif isinstance(value, int):
        if not __hasMethod(widget, "display"):
            return False
        widget.display(value)
        return True
    elif isinstance(value, float):
        if not __hasMethod(widget, "display"):
            return False
        widget.display(value)
        return True
    return False


def __setValueTabWidget(widget: QWidget, value: Any) -> bool:
    if isinstance(value, int):
        if not __hasMethod(widget, "setCurrentIndex"):
            return False
        widget.setCurrentIndex(value)
        return True
    return False
#endregion

#region SetText
def __setText(widget: QWidget, value: Any) -> bool:
    if not __hasMethod(widget, "setText"):
        return False
    widget.setText(str(value))
    return True


def __setTextCombobox(widget: QWidget, value: Any) -> bool:
    if not __hasMethod(widget, "setCurrentText"):
        return False
    widget.setCurrentText(str(value))
    return True


def __setTextLCDNumber(widget: QWidget, value: Any) -> bool:
    if not __hasMethod(widget, "display"):
        return False
    widget.display(str(value))
    return True


def __setTextProgressBar(widget: QWidget, value: Any) -> bool:
    if not __hasMethod(widget, "setFormat") or not isinstance(value, str):
        return False
    widget.setFormat(value)
    return True
#endregion

#region Params

#region Casting


def __checkStateToInt(value) -> int:
    return int(value)


def __intToCheckState(value) -> Qt.CheckState:
    if value == Qt.CheckState.Unchecked:
        return Qt.CheckState.Unchecked
    elif value == Qt.CheckState.Checked:
        return Qt.CheckState.Checked
    else:
        return Qt.CheckState.PartiallyChecked


def __fontToStr(value: QFont) -> str:
    if __hasMethod(value, "family"):
        return value.family()
    return ""


def __strToFont(value: str) -> QFont:
    return QFont(value)


def __dateToStr(value: QDate) -> str:
    return value.toString(Qt.ISODateWithMs)


def __strToDate(value: str) -> QDate:
    ret = QDate()
    ret.fromString(value, Qt.ISODateWithMs)
    return ret


def __dateTimeToStr(value: QDateTime) -> str:
    return value.toString(Qt.ISODateWithMs)


def __strToDateTime(value: str) -> QDateTime:
    ret = QDateTime()
    ret.fromString(value, Qt.ISODateWithMs)
    return ret


def __timeToStr(value: QTime) -> str:
    return value.toString(Qt.ISODateWithMs)


def __strToTime(value: str) -> QTime:
    ret = QTime()
    ret.fromString(value, Qt.ISODateWithMs)
    return ret


DICT_TYPECAST_OBJTOPRIM: Dict[type, Callable[[Any], PRIMITIVE_LISTS]] = {
    Qt.CheckState: __checkStateToInt,
    QDate: __dateToStr,
    QDateTime: __dateTimeToStr,
    QFont: __fontToStr,
    QTime: __timeToStr
}


DICT_TYPECAST_PRIMTOOBJ: Dict[type, Callable[[PRIMITIVE_LISTS], Any]] = {
    Qt.CheckState: __intToCheckState,
    QDate: __strToDate,
    QDateTime: __strToDateTime,
    QFont: __strToFont,
    QTime: __strToTime,
}

#endregion

PARAMETER_ENABLED = "enabled"
PARAMETER_VISIBLE = "visible"
PARAMETER_STYLESHEET = "styleSheet"

PARAMETER_CHECKABLE = "checkable"
PARAMETER_CHECKED = "checked"
PARAMETER_TEXT = "text"

PARAMETER_MINIMUM = "minimum"
PARAMETER_MAXIMUM = "maximum"
PARAMETER_PAGESTEP = "pageStep"
PARAMETER_SINGLESTEP = "singleStep"

PARAMETER_VALUE = "value"

PARAMETER_CHECKSTATE = "checkState"
PARAMETER_TRISTATE = "tristate"

PARAMETER_CURRENT_INDEX = "currentIndex"
PARAMETER_CURRENT_TEXT = "currentText"
PARAMETER_CURRENT_FONT = "currentFont"

PARAMETER_EDITABLE = "editable"
PARAMETER_DUPLICATES_ENABLED = "duplicatesEnabled"
PARAMETER_PLACEHOLDER_TEXT = "palceholderText"

PARAMETER_DESCRIPTION = "description"

PARAMETER_CALENDAR_POPUP = "calendarPopup"
PARAMETER_DATE = "date"
PARAMETER_DATETIME = "dateTime"
PARAMETER_TIME = "time"

PARAMETER_MAXIMUM_DATE = "maximumDate"
PARAMETER_MAXIMUM_DATETIME = "maximumDateTime"
PARAMETER_MAXIMUM_TIME = "maximumTime"

PARAMETER_MINIMUM_DATE = "minimumDate"
PARAMETER_MINIMUM_DATETIME = "minimumDateTime"
PARAMETER_MINIMUM_TIME = "minimumTime"

PARAMETER_PREFIX = "prefix"
PARAMETER_SUFFIX = "suffix"
PARAMETER_DECIMALS = "decimals"
PARAMETER_DIGIT_COUNT = "digitCount"
PARAMETER_READONLY = "readonly"

PARAMETER_TEXT_VISIBLE = "textVisible"
PARAMETER_FORMAT = "format"
PARAMETER_DISPALY_INTEGER_BASE = "displayIntegerBase"

PARAMETER_ITEM_TEXTS = "itemTexts"

PARAMETER_CURRENT_FILE = "currentFile"
PARAMETER_FILE_CONTENT = "fileContent"
PARAMETER_FILE_FILTER = "fileFilter"

PARAMETER_COLOR = "color"

#region GetParams

def __putItems(widget: QWidget, dict:Dict[str, PRIMITIVE_LISTS], parameterName: str):
    if __hasMethod(widget, "count") and __hasMethod(widget, "itemText"):
        itemTexts: List[str] = []

        for i in range(widget.count()):
            itemTexts.append(widget.itemText(i))
        dict[parameterName] = itemTexts

    return dict


def __getParams(widget: QWidget) -> Dict[str, PRIMITIVE_LISTS]:
    ret: Dict[str, PRIMITIVE_LISTS] = {}

    # QWidget
    __addParamToDict(widget, ret, "isEnabled", PARAMETER_ENABLED)
    __addParamToDict(widget, ret, "isVisible", PARAMETER_VISIBLE)
    __addParamToDict(widget, ret, "styleSheet", PARAMETER_STYLESHEET)

    # Children
    __addParamToDict(widget, ret, "isCheckable", PARAMETER_CHECKABLE)
    __addParamToDict(widget, ret, "isChecked", PARAMETER_CHECKED)
    __addParamToDict(widget, ret, "text", PARAMETER_TEXT)

    __addParamToDict(widget, ret, "minimum", PARAMETER_MINIMUM)
    __addParamToDict(widget, ret, "maximum", PARAMETER_MAXIMUM)
    __addParamToDict(widget, ret, "pageStep", PARAMETER_PAGESTEP)
    __addParamToDict(widget, ret, "singleStep", PARAMETER_SINGLESTEP)

    __addParamToDict(widget, ret, "value", PARAMETER_VALUE)

    __addParamToDict(widget, ret, "checkState", PARAMETER_CHECKSTATE)
    __addParamToDict(widget, ret, "isTristate", PARAMETER_TRISTATE)

    __addParamToDict(widget, ret, "currentIndex", PARAMETER_CURRENT_INDEX)
    __addParamToDict(widget, ret, "currentText", PARAMETER_CURRENT_TEXT)
    __addParamToDict(widget, ret, "currentFont", PARAMETER_CURRENT_FONT)

    __addParamToDict(widget, ret, "isEditable", PARAMETER_EDITABLE)
    __addParamToDict(widget, ret, "duplicatesEnabled", PARAMETER_DUPLICATES_ENABLED)
    __addParamToDict(widget, ret, "placeholderText", PARAMETER_PLACEHOLDER_TEXT)

    __addParamToDict(widget, ret, "description", PARAMETER_DESCRIPTION)

    __addParamToDict(widget, ret, "calendarPopup", PARAMETER_CALENDAR_POPUP)
    __addParamToDict(widget, ret, "date", PARAMETER_DATE)
    __addParamToDict(widget, ret, "dateTime", PARAMETER_DATETIME)
    __addParamToDict(widget, ret, "time", PARAMETER_TIME)

    __addParamToDict(widget, ret, "maximumDate", PARAMETER_MAXIMUM_DATE)
    __addParamToDict(widget, ret, "maximumDateTime", PARAMETER_MAXIMUM_DATETIME)
    __addParamToDict(widget, ret, "maximumTime", PARAMETER_MAXIMUM_TIME)

    __addParamToDict(widget, ret, "minimumDate", PARAMETER_MINIMUM_DATE)
    __addParamToDict(widget, ret, "minimumDateTime", PARAMETER_MINIMUM_DATETIME)
    __addParamToDict(widget, ret, "minimumTime", PARAMETER_MINIMUM_TIME)

    __addParamToDict(widget, ret, "prefix", PARAMETER_PREFIX)
    __addParamToDict(widget, ret, "suffix", PARAMETER_SUFFIX)

    __addParamToDict(widget, ret, "decimals", PARAMETER_DECIMALS)
    __addParamToDict(widget, ret, "isReadOnly", PARAMETER_READONLY)
    __addParamToDict(widget, ret, "digitCount", PARAMETER_DIGIT_COUNT)

    __addParamToDict(widget, ret, "isTextVisible", PARAMETER_TEXT_VISIBLE)
    __addParamToDict(widget, ret, "format", PARAMETER_FORMAT)

    __addParamToDict(widget, ret, "displayIntegerBase", PARAMETER_DISPALY_INTEGER_BASE)

    __addParamToDict(widget, ret, "displayIntegerBase", PARAMETER_DISPALY_INTEGER_BASE)

    __addParamToDict(widget, ret, "currentFile", PARAMETER_CURRENT_FILE)
    __addParamToDict(widget, ret, "fileContent", PARAMETER_FILE_CONTENT)
    __addParamToDict(widget, ret, "filenameFilter", PARAMETER_FILE_FILTER)

    __addParamToDict(widget, ret, "color", PARAMETER_COLOR)

    __putItems(widget, ret, PARAMETER_ITEM_TEXTS)

    return ret
#endregion

#region SetParams

def __setParams(widget: QWidget, params: Dict[str, PRIMITIVE_LISTS]) -> bool:

    __applyParamToWidget(widget, params, "setEnabled", PARAMETER_ENABLED)
    __applyParamToWidget(widget, params, "setVisible", PARAMETER_VISIBLE)
    __applyParamToWidget(widget, params, "setStyleSheet", PARAMETER_STYLESHEET)

    if __hasMethod(widget, "clear") and __hasMethod(widget, "addItems"):
        widget.clear()

    __applyParamToWidget(widget, params, "addItems", PARAMETER_ITEM_TEXTS)

    __applyParamToWidget(widget, params, "setCheckable", PARAMETER_CHECKABLE)
    __applyParamToWidget(widget, params, "setChecked", PARAMETER_CHECKED)

    __applyParamToWidget(widget, params, "setText", PARAMETER_TEXT)

    __applyParamToWidget(widget, params, "setMinimum", PARAMETER_MINIMUM)
    __applyParamToWidget(widget, params, "setMaximum", PARAMETER_MAXIMUM)
    __applyParamToWidget(widget, params, "setPageStep", PARAMETER_PAGESTEP)
    __applyParamToWidget(widget, params, "setSingleStep", PARAMETER_SINGLESTEP)
    __applyParamToWidget(widget, params, "setValue", PARAMETER_VALUE)
    __applyParamToWidget(widget, params, "setCheckState", PARAMETER_CHECKSTATE, Qt.CheckState)
    __applyParamToWidget(widget, params, "setTristate", PARAMETER_TRISTATE)

    __applyParamToWidget(widget, params, "setCurrentIndex", PARAMETER_CURRENT_INDEX)
    __applyParamToWidget(widget, params, "setCurrentText", PARAMETER_CURRENT_TEXT)
    __applyParamToWidget(widget, params, "setCurrentFont", PARAMETER_CURRENT_FONT, QFont)

    __applyParamToWidget(widget, params, "setEditable", PARAMETER_EDITABLE)
    __applyParamToWidget(widget, params, "setDuplicatesEnabled", PARAMETER_DUPLICATES_ENABLED)
    __applyParamToWidget(widget, params, "setPlaceholderText", PARAMETER_PLACEHOLDER_TEXT)
    __applyParamToWidget(widget, params, "setDescription", PARAMETER_DESCRIPTION)
    __applyParamToWidget(widget, params, "setCalendarPopup", PARAMETER_CALENDAR_POPUP)
    __applyParamToWidget(widget, params, "setDate", PARAMETER_DATE, QDate)
    __applyParamToWidget(widget, params, "setDateTime", PARAMETER_DATETIME, QDateTime)
    __applyParamToWidget(widget, params, "setTime", PARAMETER_TIME, QTime)

    __applyParamToWidgetNullable(widget, params, "setMaximumDate", "clearMaximumDate", PARAMETER_MAXIMUM_DATE, QDate)
    __applyParamToWidgetNullable(widget, params, "setMaximumDateTime", "clearMaximumDateTime", PARAMETER_MAXIMUM_DATETIME, QDateTime)
    __applyParamToWidgetNullable(widget, params, "setMaximumTime", "clearMaximumTime", PARAMETER_MAXIMUM_TIME, QTime)
    __applyParamToWidgetNullable(widget, params, "setMinimumDate", "clearMinimumDate", PARAMETER_MINIMUM_DATE, QDate)
    __applyParamToWidgetNullable(widget, params, "setMinimumDateTime", "clearMinimumDateTime", PARAMETER_MINIMUM_DATETIME, QDateTime)
    __applyParamToWidgetNullable(widget, params, "setMinimumTime", "clearMinimumTime", PARAMETER_MINIMUM_TIME, QTime)

    __applyParamToWidget(widget, params, "setPrefix", PARAMETER_PREFIX)
    __applyParamToWidget(widget, params, "setSuffix", PARAMETER_SUFFIX)

    __applyParamToWidget(widget, params, "setDecimals", PARAMETER_DECIMALS)
    __applyParamToWidget(widget, params, "setDigitCount", PARAMETER_DIGIT_COUNT)

    __applyParamToWidget(widget, params, "setReadOnly", PARAMETER_READONLY)

    __applyParamToWidget(widget, params, "setTextVisible", PARAMETER_TEXT_VISIBLE)
    __applyParamToWidget(widget, params, "setFormat", PARAMETER_FORMAT)

    __applyParamToWidget(widget, params, "setDisplayIntegerBase", PARAMETER_DISPALY_INTEGER_BASE)

    __applyParamToWidget(widget, params, "setCurrentFile", PARAMETER_CURRENT_FILE)
    __applyParamToWidget(widget, params, "setFilenameFilter", PARAMETER_FILE_FILTER)

    __applyParamToWidget(widget, params, "setColor", PARAMETER_COLOR)

    return True

#endregion
#endregion

#region Callbacks


def __bindClicked(widget: QWidget, callback: Callable[[], None]) -> bool:
    if not hasattr(widget, "clicked"):
        return False

    def __callback(checked: bool=True):
        callback()

    widget.clicked.connect(__callback)
    return True


def __bindCurrentIndexChanged(widget: QWidget, callback: Callable[[], None]) -> bool:
    if not hasattr(widget, "currentIndexChanged"):
        return False

    def __callback(index: int):
        callback()

    widget.currentIndexChanged.connect(__callback)
    return True


def __bindDateTimeChanged(widget: QWidget, callback: Callable[[], None]) -> bool:
    if not hasattr(widget, "dateTimeChanged"):
        return False

    def __callback(datetime: QDateTime):
        callback()

    widget.dateTimeChanged.connect(__callback)
    return True


def __bindValueChanged(widget: QWidget, callback: Callable[[], None]) -> bool:
    if not hasattr(widget, "valueChanged"):
        return False

    def __callback(value: Any):
        callback()

    widget.valueChanged.connect(__callback)
    return True


def __bindTextChanged(widget: QWidget, callback: Callable[[], None]) -> bool:
    if not hasattr(widget, "textChanged"):
        return False

    def __callback(value: Any):
        callback()

    widget.textChanged.connect(__callback)
    return True


def __bindCurrentChanged(widget: QWidget, callback: Callable[[], None]) -> bool:
    if not hasattr(widget, "currentChanged"):
        return False

    def __callback(value: int):
        callback()

    widget.currentChanged.connect(__callback)
    return True


def __bindFileselectorFileChanged(widget: QWidget, callback: Callable[[], None]) -> bool:
    if not hasattr(widget, "fileselectorfilechanged"):
        return False

    def __callback():
        callback()

    widget.fileselectorfilechanged.connect(__callback)
    return True

def __bindColorChanged(widget: QWidget, callback: Callable[[], None]):
    if not hasattr(widget, "colorChanged"):
        return False

    def __callback(color: QColor):
        callback()

    widget.colorChanged.connect(__callback)
    return True
#endregion

#endregion

#region Dictionaries


WIDGET_SET_VALUE: Dict[type, Callable[[QWidget, Any], bool]] = {
    QAbstractButton: __setValueButton,
    QAbstractSlider: __setValueInt,
    QCheckBox: __setValueButton,
    QComboBox: __setValueCombobox,
    QCommandLinkButton: __setValueButton,
    QDateTimeEdit: __setValueDateTimeEdit,
    QDateEdit: __setValueDateTimeEdit,
    QDial: __setValueInt,
    QDoubleSpinBox: __setValueFloat,
    QLabel: __setText,
    QLCDNumber: __setValueLCDNumber,
    QLineEdit: __setText,
    QProgressBar: __setValueInt,
    QPushButton: __setValueButton,
    QRadioButton: __setValueButton,
    QScrollBar: __setValueInt,
    QSlider: __setValueInt,
    QSpinBox: __setValueInt,
    QTabWidget: __setValueTabWidget,
    QTimeEdit: __setValueDateTimeEdit,
    QToolButton: __setValueButton,
}

WIDGET_SET_TEXT: Dict[type, Callable[[QWidget, Any], bool]] = {
    QAbstractButton: __setText,
    QCheckBox: __setText,
    QComboBox: __setTextCombobox,
    QCommandLinkButton: __setText,
    QLabel: __setText,
    QLCDNumber: __setTextLCDNumber,
    QLineEdit: __setText,
    QProgressBar: __setTextProgressBar,
    QPushButton: __setText,
    QRadioButton: __setText,
    QToolButton: __setText,
}

WIDGET_GET_PARAMS: Dict[type, Callable[[QWidget], Dict[str, PRIMITIVE_LISTS]]] = {
    QAbstractButton: __getParams,
    QAbstractSlider: __getParams,
    QCheckBox: __getParams,
    QComboBox: __getParams,
    QCommandLinkButton: __getParams,
    QDateTimeEdit: __getParams,
    QDateEdit: __getParams,
    QDial: __getParams,
    QDoubleSpinBox: __getParams,
    QFontComboBox: __getParams,
    QLabel: __getParams,
    QLCDNumber: __getParams,
    QLineEdit: __getParams,
    QProgressBar: __getParams,
    QPushButton: __getParams,
    QRadioButton: __getParams,
    QScrollBar: __getParams,
    QSlider: __getParams,
    QSpinBox: __getParams,
    QTabWidget: __getParams,
    QTimeEdit: __getParams,
    QToolButton: __getParams,

    FileSelectionButton: __getParams,
    ColorSelectionButton: __getParams,
}

WIDGET_SET_PARAMS: Dict[type, Callable[[QWidget, Dict[str, PRIMITIVE_LISTS]], bool]] = {
    QAbstractButton: __setParams,
    QAbstractSlider: __setParams,
    QCheckBox: __setParams,
    QComboBox: __setParams,
    QCommandLinkButton: __setParams,
    QDateTimeEdit: __setParams,
    QDateEdit: __setParams,
    QDial: __setParams,
    QDoubleSpinBox: __setParams,
    QFontComboBox: __setParams,
    QLabel: __setParams,
    QLCDNumber: __setParams,
    QLineEdit: __setParams,
    QProgressBar: __setParams,
    QPushButton: __setParams,
    QRadioButton: __setParams,
    QScrollBar: __setParams,
    QSlider: __setParams,
    QSpinBox: __setParams,
    QStackedWidget: __setParams,
    QTabWidget: __setParams,
    QTimeEdit: __setParams,
    QToolButton: __setParams,

    FileSelectionButton: __setParams,
    ColorSelectionButton: __setParams,
}

WIDGET_SET_CALLBACK: Dict[type, Callable[[QWidget, Callable[[], None]], bool]] = {
    QAbstractButton: __bindClicked,
    QAbstractSlider: __bindValueChanged,
    QCheckBox: __bindClicked,
    QComboBox: __bindCurrentIndexChanged,
    QFontComboBox: __bindCurrentIndexChanged,
    QCommandLinkButton: __bindClicked,
    QDateTimeEdit: __bindDateTimeChanged,
    QDateEdit: __bindDateTimeChanged,
    QDial: __bindValueChanged,
    QDoubleSpinBox: __bindValueChanged,
    QLineEdit: __bindTextChanged,
    QProgressBar: __bindValueChanged,
    QPushButton: __bindClicked,
    QRadioButton: __bindClicked,
    QScrollBar: __bindValueChanged,
    QSlider: __bindValueChanged,
    QSpinBox: __bindValueChanged,
    QTabWidget: __bindCurrentChanged,
    QTimeEdit: __bindDateTimeChanged,
    QToolButton: __bindClicked,

    FileSelectionButton: __bindFileselectorFileChanged,
    ColorSelectionButton: __bindColorChanged
}

#endregion

#region General Setters


def setValue(widget: QWidget, value: Any) -> bool:
    if type(widget) not in WIDGET_SET_VALUE:
        return False
    return WIDGET_SET_VALUE[type(widget)](widget, value)


def setValueSilent(widget: QWidget, value: Any) -> bool:
    widget.blockSignals(True)
    res = setValue(widget, value)
    widget.blockSignals(False)
    return res


def setText(widget: QWidget, value: str) -> bool:
    if type(widget) not in WIDGET_SET_VALUE:
        return False
    return WIDGET_SET_TEXT[type(widget)](widget, value)


def setTextSilent(widget: QWidget, value: str) -> bool:
    widget.blockSignals(True)
    res = setText(widget, value)
    widget.blockSignals(False)
    return res


def getParams(widget: QWidget) -> Dict[str, PRIMITIVE_LISTS]:
    try:
        if type(widget) not in WIDGET_GET_PARAMS:
            return {"error": "404 - KEY NOT FOUND"}
        return WIDGET_GET_PARAMS[type(widget)](widget)
    except Exception as ex:
        logger.exception(ex)


def setParams(widget: QWidget, value: Dict[str, PRIMITIVE_LISTS]) -> bool:
    try:
        if type(widget) not in WIDGET_SET_PARAMS:
            return False
        return WIDGET_SET_PARAMS[type(widget)](widget, value)
    except Exception as ex:
        logger.exception(ex)


def setParamsSilent(widget: QWidget, value: Dict[str, PRIMITIVE_LISTS]) -> bool:
    try:
        widget.blockSignals(True)
        res = setParams(widget, value)
        widget.blockSignals(False)
        return res
    except Exception as ex:
        logger.exception(ex)


def setCallback(widget: QWidget, callback: Callable[[], None]):
    if type(widget) not in WIDGET_SET_CALLBACK:
        return False
    return WIDGET_SET_CALLBACK[type(widget)](widget, callback)

#endregion