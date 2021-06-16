from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

#region TOOLS
def _silence(method, widget, value):
    """
    Execute the supplied method without triggering any Signals on the given Widget

    :param method: Method with signature f(w : widget, v : value)
    :param widget: QWidget used as first Argument for method
    :param value: Value used as second argument for method
    :return: None
    """
    widget.blockSignals(True)
    method(widget, value)
    widget.blockSignals(False)
#endregion

#region Widget Tools

def setValueQRadioButton(widget: QRadioButton, value: bool):
    """
    Sets the Value of the given QRadioButton

    :param widget: QRadioButton to set the value of
    :param value: Value to set
    :return: None
    """
    widget.setChecked(value)


def setValueQRadioButtonSilent(widget: QRadioButton, value: bool):
    """
    Sets the Value of the given QRadioButton

    :param widget: QRadioButton to set the value of
    :param value: Value to set
    :return: None
    """
    _silence(setValueQRadioButton, widget, value)


def setValueQSpin(widget, value):
    """
    Sets the Value of the given QSpin

    :param widget: QSpin to set the value of
    :param value: Value to set
    :return: None
    """
    widget.setValue(value)

def setValueQSpinSilent (widget, value):
    """
    Sets the Value of the given QSpin without triggering signals

    :param widget: QSpin to set the value of
    :param value: Value to set
    :return: None
    """
    _silence(setValueQSpin, widget, value)

def setValueQSlider(widget, value):
    """
    Sets the Value of the given QSlider Widget

    :param widget: QSlider to set the value of
    :param value: Value to set
    :return: None
    """
    widget.setValue(value)

def setValueQSliderSilent (widget, value):
    """
    Sets the Value of the given QSlider Widget without triggering signals

    :param widget: QSlider to set the value of
    :param value: Value to set
    :return: None
    """
    _silence(setValueQSpin, widget, value)

def setValueQLineEdit(widget, value):
    """
    Sets the Value of the given QLineEdit Widget

    :param widget: QLineEdit to set the value of
    :param value: Value to set
    :return: None
    """
    widget.setText(value)

def setValueQLineEditSilent(widget, value):
    """
    Sets the Value of the given QLineEdit Widget without triggering signals

    :param widget: QLineEdit to set the value of
    :param value: Value to set
    :return: None
    """
    _silence(setValueQLineEdit, widget, value)

def setComboIndex(widget, value):
    """
    Sets the active index of the given QComboBox Widget

    :param widget: QComboBox to set the index of
    :param value: Index to set
    :return: None
    """
    widget.setCurrentIndex(value)

def setComboIndexSilent(widget, value):
    """
    Sets the active index of the given QComboBox Widget without triggering signals

    :param widget: QComboBox to set the index of
    :param value: Index to set
    :return: None
    """
    _silence(setComboIndex, widget, value)

def setComboText(widget, value, dict=None):
    """
    Sets the text of the given QComboBox Widget

    :param widget: QComboBox to set the text of
    :param value: text to set
    :param dict: Lookup for text translation, if None, value is used directly, otherwise the element with the key value
    is used. Default: None
    :return: None
    """
    if dict is None:
        widget.setCurrentText(value)
        return
    widget.setCurrentText(dict[value])

def setComboTextSilent(widget, value):
    """
    Sets the text of the given QComboBox Widget

    :param widget: QComboBox to set the text of
    :param value: text to set
    :return: None
    """
    _silence(setComboText, widget, value)

def setPlainTextEdit(widget : QPlainTextEdit, value):
    """
    Sets the content of the given QPlainTextEdit Widget

    :param widget: QPlainTextEdit to set the content of
    :param value: content to set
    :return: None
    """
    widget.setPlainText(value)

def setPlainTextEditSilent(widget, value):
    """
    Sets the content of the given QPlainTextEdit Widget

    :param widget: QPlainTextEdit to set the content of
    :param value: content to set
    :return: None
    """
    _silence(setPlainTextEdit, widget, value)

def setKeySequenceEdit (widget : QKeySequenceEdit, value : QKeySequence):
    """
    Set the QKeySequence of the given QKeySequenceEdit widget
    :param widget: QKeySequenceEdit to set the Key sequence of
    :param value: QKeySequence to set
    :return: None
    """
    widget.setKeySequence(value)

#region Widget Setup

def setComboboxListValuesFromDict(widget, values):
    """
    Set the Values of a QCombobox from a Dict

    :param widget: QCombobox to set the values
    :param values: Dict containing the values to set
    :return: None
    """
    widget.addItems(list(values.keys()))

#endregion

#endregion