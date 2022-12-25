import base64

from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont, QImage
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from PyQt5.QtWidgets import QStyleOptionViewItem

from .....structs.action import Action
from ..model.actionmodel import DATA_ROLE_ACTION_DATA, DATA_ROLE_CATEGORY_DATA

from virtualstudio.common.logging import logengine

class ActionWidget(QStyledItemDelegate):
    
    def __init__(self, view: QTreeView, categoryIcons: list, parent=None):
        super(ActionWidget, self).__init__(parent)
        self.view: QTreeView = view

        self.categoryIcons = {}

        for k in categoryIcons:
            self.categoryIcons[k['name']] = self.decodeIcon(k['icon'])

        self.brushCathegoryBg = QBrush(QColor(53, 53, 53, 75))
        self.brushActionBg = QBrush(QColor(25, 25, 25, 127))

        self.logger = logengine.getLogger()

    def decodeIcon(self, data):
        rawIcon = base64.b64decode(data.encode("utf-8"))
        iconImage = QImage()
        iconImage.loadFromData(rawIcon)
        return iconImage

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        actionData = index.data(role=DATA_ROLE_ACTION_DATA)
        if actionData is None:
            option.text = index.data()
        else:
            option.text = actionData.name + "  " + "{}.{}.{}".format(*actionData.version)
        option.displayAlignment = Qt.AlignVCenter | Qt.AlignLeft

    def sizeHint(self, option: QStyleOptionViewItem, modelIndex: QModelIndex):
        size: QSize = super(ActionWidget, self).sizeHint(option, modelIndex)
        size.setHeight(50)
        return size

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        actionData = index.data(role=DATA_ROLE_ACTION_DATA)
        try:
            if actionData is not None:
                self.paintAction(painter, option, index, actionData)
            else:
                self.paintCategory(painter, option, index, index.data())
        except Exception as ex:
            self.logger.exception(ex)

    def paintAction(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex, action: Action):
        x = option.rect.x()
        y = option.rect.y()
        w = option.rect.width()
        h = option.rect.height()

        # Required to draw background on Drag & Drop
        painter.setBrush(self.brushActionBg)
        painter.setPen(Qt.NoPen)
        painter.drawRect(x, y, w, h)

        icon_offset = (h - 32) // 2

        painter.setBrush(Qt.NoBrush)
        painter.drawImage(x + icon_offset, y + icon_offset, action.iconImage, 0, 0, 32, 32)

        painter.setPen(QPen(Qt.white))
        font: QFont = painter.font()
        font.setBold(False)
        font.setItalic(False)

        painter.setFont(font)

        text_offset = int(((h/2)) // 2)

        painter.drawText(x + 32 + (icon_offset * 2), y + text_offset, w - (x + 32 + (icon_offset * 3)), 20, 0, action.name)
        painter.setPen(QPen(Qt.gray))
        font.setItalic(True)
        painter.setFont(font)
        painter.drawText(x + 32 + (icon_offset * 2), y + 15 + text_offset, w - (x + 32 + (icon_offset * 3)), 20, 0,
                         "{} - v{}.{}.{}".format(action.author, *action.version))
        font.setItalic(False)
        painter.setFont(font)

    def paintCategory(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex, category: str):
        categoryData = index.data(role=DATA_ROLE_CATEGORY_DATA)
        x = option.rect.x()
        y = option.rect.y()
        w = option.rect.width()
        h = option.rect.height()

        #painter.setBrush(self.brushCathegoryBg)
        painter.setPen(Qt.NoPen)
        #painter.drawRect(x, y, w, h)

        icon_offset = (h - 32) // 2

        painter.setBrush(Qt.NoBrush)

        if categoryData["name"] in self.categoryIcons:
            painter.drawImage(x + icon_offset, y + icon_offset, self.categoryIcons[categoryData["name"]], 0, 0, 32, 32)
        else:
            painter.setPen(QPen(Qt.white))
            painter.drawRect(x + icon_offset, y + icon_offset, 32, 32)

        painter.setPen(QPen(Qt.white))
        font: QFont = painter.font()
        font.setBold(True)
        painter.setFont(font)
        text_offset = (h - 12) // 2

        painter.drawText(x + 32 + (icon_offset*2), y + text_offset, w - (x + 32 + (icon_offset*3)), 20, 0, category)
        font.setBold(False)
        painter.setFont(font)

    def createEditor(self, widget, style, index):
        return None

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        pass
