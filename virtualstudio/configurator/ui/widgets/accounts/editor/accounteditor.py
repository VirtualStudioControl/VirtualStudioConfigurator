import base64
from typing import Dict

from PyQt5.QtCore import QModelIndex, QAbstractItemModel, QSize, Qt
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPen, QFont
from PyQt5.QtWidgets import QStyledItemDelegate, QTreeView, QStyleOptionViewItem, QWidget, QStyle

from virtualstudio.common.account_manager.account_info import AccountInfo
from virtualstudio.configurator.ui.widgets.accounts.model.accountmodel import DATA_ROLE_ACCOUNT_DATA, \
    DATA_ROLE_CATEGORY_DATA


class AccountEditor(QStyledItemDelegate):

    def __init__(self, view: QTreeView, accountTypeIcons: Dict[str, str], categoryIcons: Dict[str, str], parent=None):
        super(AccountEditor, self).__init__(parent)
        self.view: QTreeView = view

        #self.categoryIcons = {}
        self.accountTypeIcons = {}
        for k in accountTypeIcons:
            self.accountTypeIcons[k] = self.decodeIcon(accountTypeIcons[k])

        self.brushCathegoryBg = QBrush(QColor(53, 53, 53, 75))
        self.brushActionBg = QBrush(QColor(25, 25, 25, 127))

    def decodeIcon(self, data):
        rawIcon = base64.b64decode(data.encode("utf-8"))
        iconImage = QImage()
        iconImage.loadFromData(rawIcon)
        return iconImage

    def initStyleOption(self, option: QStyleOptionViewItem, index: QModelIndex):
        accountData: AccountInfo = index.data(role=DATA_ROLE_ACCOUNT_DATA)
        if accountData is None:
            option.text = index.data()
        else:
            option.text = "{}@{}.{}".format(accountData.username, accountData.server, accountData.port)
        option.displayAlignment = Qt.AlignVCenter | Qt.AlignLeft

    def sizeHint(self, option: QStyleOptionViewItem, modelIndex: QModelIndex):
        size: QSize = super(AccountEditor, self).sizeHint(option, modelIndex)
        size.setHeight(50)
        return size

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        actionData = index.data(role=DATA_ROLE_ACCOUNT_DATA)
        if actionData is not None:
            self.paintAction(painter, option, index, actionData)
        else:
            self.paintCategory(painter, option, index, index.data())

    def paintAction(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex, account: AccountInfo):
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
        #painter.drawImage(x + icon_offset, y + icon_offset, account.iconImage, 0, 0, 32, 32)
        if account.accountType in self.accountTypeIcons:
        #    pass
            painter.drawImage(x + icon_offset, y + icon_offset, self.accountTypeIcons[account.accountType], 0, 0, 32, 32)
        else:
            print(account.accountType, "not in", self.accountTypeIcons.keys())
            painter.setPen(QPen(Qt.white))
            painter.drawRect(x + icon_offset, y + icon_offset, 32, 32)

        font: QFont = painter.font()

        if int(option.state & QStyle.State_Selected) > 0:
            painter.setPen(QPen(QColor("#FF00AAFF")))

            font.setBold(True)
        else:
            painter.setPen(QPen(Qt.white))

            font.setBold(False)
        font.setItalic(False)

        painter.setFont(font)

        text_offset = ((h / 2)) // 2

        painter.drawText(x + 32 + (icon_offset * 2), y + text_offset, w - (x + 32 + (icon_offset * 3)), 20, 0,
                         account.accountTitle)
        painter.setPen(QPen(Qt.gray))
        font.setItalic(True)
        painter.setFont(font)
        painter.drawText(x + 32 + (icon_offset * 2), y + 15 + text_offset, w - (x + 32 + (icon_offset * 3)), 20, 0,
                         "{}@{}:{}".format(account.username, account.server, account.port))
        font.setItalic(False)
        painter.setFont(font)

    def paintCategory(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex, category: str):
        categoryData = index.data(role=DATA_ROLE_CATEGORY_DATA)
        x = option.rect.x()
        y = option.rect.y()
        w = option.rect.width()
        h = option.rect.height()

        # painter.setBrush(self.brushCathegoryBg)
        painter.setPen(Qt.NoPen)
        # painter.drawRect(x, y, w, h)

        icon_offset = (h - 32) // 2

        painter.setBrush(Qt.NoBrush)

        #if categoryData["name"] in self.categoryIcons:
        #    pass
            #painter.drawImage(x + icon_offset, y + icon_offset, self.categoryIcons[categoryData["name"]], 0, 0, 32, 32)
        #else:
        painter.setPen(QPen(Qt.white))
        painter.drawRect(x + icon_offset, y + icon_offset, 32, 32)

        painter.setPen(QPen(Qt.white))
        font: QFont = painter.font()
        font.setBold(True)
        painter.setFont(font)
        text_offset = (h - 12) // 2

        painter.drawText(x + 32 + (icon_offset * 2), y + text_offset, w - (x + 32 + (icon_offset * 3)), 20, 0, category)
        font.setBold(False)
        painter.setFont(font)

    def createEditor(self, widget, style, index):
        return None

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        pass
