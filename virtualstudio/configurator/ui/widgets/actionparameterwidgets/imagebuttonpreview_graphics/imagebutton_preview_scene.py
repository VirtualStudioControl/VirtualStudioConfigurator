from typing import Optional, Tuple

from PyQt5.QtCore import Qt, QObject, QRectF, QBuffer
from PyQt5.QtGui import QBrush, QImage, QColor, QFont, QPainter, QPen
from PyQt5.QtWidgets import QGraphicsScene

from virtualstudio.common.io import filewriter
from virtualstudio.common.io.filewriter import readFileBinary
from virtualstudio.common.logging import logengine

from virtualstudio.common.tools import actiondatatools as actionTools, actiondatatools
from virtualstudio.common.tools import icontools
from virtualstudio.configurator.data import constants, default_values
from virtualstudio.configurator.devicemanager import devicemanager
from virtualstudio.configurator.ui.widgets.hardware.controls.abstractcontrolgraphic import AbstractControlGraphic

TEXT_ALIGN_V = {
    0: Qt.AlignTop,
    1: Qt.AlignVCenter,
    2: Qt.AlignBottom
}

TEXT_ALIGN_H = {
    0: Qt.AlignLeft,
    1: Qt.AlignHCenter,
    2: Qt.AlignRight
}

class ImagebuttonPreviewScene(QGraphicsScene):

    def __init__(self, parent: QObject = None):
        super().__init__(parent)
        self.logger = logengine.getLogger()

        self.setBackgroundBrush(Qt.black)

        self.currentState = 0

        self.currentImage: Optional[QImage] = None
        self.iconImage: QImage = QImage(64, 64, QImage.Format_RGB32)
        self.iconFormat: str = ""
        self.iconFlip: Tuple[bool, bool] = (False, False)
        self.showText: bool = True
        self.currentText: str = ""
        self.currentFont: Optional[QFont] = None
        self.textAlignment: Tuple[int, int] = (1,1)
        self.textForegroundColor: QColor= QColor("#ffffff")
        self.backgroundColor: QColor = QColor("#000000")

    def setState(self, state: int):
        self.currentState = state
        self.updateImageFromAction()

    def onDeviceChanged(self):
        device = devicemanager.getDevice(constants.CURRENT_DEVICE)

        if devicemanager.hasParameters(device):

            iconResolution = devicemanager.getParameterIconResolution(device, default=(64, 64))
            self.iconFormat = devicemanager.getParameterIconFormat(device, default="JPEG")
            self.iconFlip = devicemanager.getParameterIconFlip(device, default=(False, False))

            try:
                self.iconImage = QImage(*iconResolution, QImage.Format_RGB32)
            except Exception as ex:
                self.logger.exception(ex)


    def updateImageFromAction(self):
        self.redrawImage()

    def loadImage(self):
        dataString = actionTools.getValue(data=constants.SELECTED_CONTROL.action.actionParams,
                                    key=actionTools.KEY_STATE_IMAGEBUTTON_IMAGE_BASE,
                                    state=self.currentState)

        if dataString is not None or "":
            data = icontools.decodeIconData(dataString)
        else:
            path = actionTools.getValue(data=constants.SELECTED_CONTROL.action.actionParams,
                                        key=actionTools.KEY_STATE_IMAGEBUTTON_IMAGE_SRC,
                                        state=self.currentState)

            if path is not None and path != "":
                data = self.loadImageFromPath(path)
            else:
                data = bytes()

        image = QImage()
        image.loadFromData(data)

        return image

    def loadImageFromPath(self, path: str):
        data = readFileBinary(path)
        encoded = icontools.encodeIconData(data)
        actionTools.setValue(data=constants.SELECTED_CONTROL.action.actionParams,
                             key=actionTools.KEY_STATE_IMAGEBUTTON_IMAGE_BASE,
                             value=encoded,
                             state=self.currentState)
        return data

    def __updateText(self):
        self.showText = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_SHOW,
                                              self.currentState,
                                              default_values.IMAGEBUTTON_TEXT_SHOW)

        self.currentText = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_TEXT,
                                              self.currentState,
                                              default_values.IMAGEBUTTON_TEXT_TEXT)

        fontFamily = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                                    actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_FONT,
                                                    self.currentState,
                                                    default_values.IMAGEBUTTON_TEXT_FONT)
        pointSize = actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_FONTSIZE,
                                              self.currentState,
                                              default_values.IMAGEBUTTON_TEXT_FONTSIZE)

        self.currentFont = QFont(fontFamily, int(pointSize))

        self.currentFont.setBold(actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_BOLD,
                                              self.currentState,
                                              default_values.IMAGEBUTTON_TEXT_BOLD))
        self.currentFont.setItalic(actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ITALICS,
                                              self.currentState,
                                              default_values.IMAGEBUTTON_TEXT_ITALICS))
        self.currentFont.setUnderline(actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_UNDERLINE,
                                              self.currentState,
                                              default_values.IMAGEBUTTON_TEXT_UNDERLINE))
        self.currentFont.setStrikeOut(actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_STRIKETHROUGH,
                                              self.currentState,
                                              default_values.IMAGEBUTTON_TEXT_STRIKETHROUGH))

        self.textAlignment = (actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ALIGNV,
                                              self.currentState,
                                              default_values.IMAGEBUTTON_TEXT_ALIGNV),
                              actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                              actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_ALIGNH,
                                              self.currentState,
                                              default_values.IMAGEBUTTON_TEXT_ALIGNH))

        self.textForegroundColor = QColor(actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                                     actiondatatools.KEY_STATE_IMAGEBUTTON_TEXT_COLOR_FG,
                                                     self.currentState,
                                                     default_values.IMAGEBUTTON_TEXT_COLOR_FG))

        self.backgroundColor = QColor(actiondatatools.getValueOrDefault(constants.SELECTED_CONTROL.action.actionParams,
                                                                        actiondatatools.KEY_STATE_IMAGEBUTTON_COLOR_BACKGROUND,
                                                                        self.currentState,
                                                                        default_values.IMAGEBUTTON_COLOR_BACKGROUND))

    def redrawImage(self):
        self.currentImage = self.loadImage()
        self.__updateText()

        self.drawIcon()

        self.update()

    def computeTextAlignmentFlags(self):
        flags = 0

        flags = flags | TEXT_ALIGN_V[self.textAlignment[0]]
        flags = flags | TEXT_ALIGN_H[self.textAlignment[1]]

        return flags

    def drawIcon(self) -> None:
        if self.iconFormat == "":
            self.onDeviceChanged()
        painter = QPainter()

        painter.begin(self.iconImage)
        painter.setPen(QPen(self.backgroundColor))
        painter.setBrush(QBrush(self.backgroundColor))
        painter.drawRect(0, 0, self.iconImage.width(), self.iconImage.height())

        painter.drawImage(0, 0,
                          self.currentImage.scaled(self.iconImage.width(), self.iconImage.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation),
                          0, 0, self.iconImage.width(), self.iconImage.height())

        if self.showText:
            painter.setFont(self.currentFont)
            painter.setPen(QPen(self.textForegroundColor))
            painter.drawText(QRectF(0, 0, self.iconImage.width(), self.iconImage.height()),
                             self.computeTextAlignmentFlags(), self.currentText)

        painter.end()

        iconBuffer = QBuffer()

        mirrored = self.iconImage.mirrored(*self.iconFlip)
        mirrored.save(iconBuffer, self.iconFormat)

        actionTools.setValue(data=constants.SELECTED_CONTROL.action.actionParams,
                             key=actionTools.KEY_STATE_IMAGEBUTTON_IMAGE,
                             value=icontools.encodeIconData(iconBuffer.data()),
                             state=self.currentState)

        self.updateControl()


    def updateControl (self):
        control: Optional[AbstractControlGraphic] = constants.SELECTED_CONTROL
        if control is None:
            return

        control.setIconImage(QImage(self.iconImage))


    def drawForeground(self, painter: QPainter, rect: QRectF) -> None:
        try:
            painter.drawImage(rect,
                          self.iconImage.scaled(int(rect.width()), int(rect.height()), Qt.KeepAspectRatio,
                                                   Qt.SmoothTransformation))
        except Exception as ex:
            self.logger.exception(ex)
