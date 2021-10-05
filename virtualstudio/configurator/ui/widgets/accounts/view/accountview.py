from typing import Union

from PyQt5.QtCore import Qt, QModelIndex, QVariant
from PyQt5.QtGui import QPainter, QPalette, QColor, QDropEvent
from PyQt5.QtWidgets import QTreeView, QStyleOptionViewItem

from virtualstudio.common.account_manager.account_info import AccountInfo
from virtualstudio.configurator.ui.widgets.accounts.model.accountmodel import DATA_ROLE_ACCOUNT_DATA


class AccountView(QTreeView):

    def __init__(self, parent=None):
        super().__init__(parent)

    def drawRow(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        accountData = index.data(role=DATA_ROLE_ACCOUNT_DATA)
        if accountData is not None:
            option.features = option.features & ~ option.Alternate
        else:
            option.features = option.features | option.Alternate
            option.palette.setBrush(QPalette.AlternateBase, option.palette.window())

        # Set Selection color to transparent
        option.palette.setColor(QPalette.Highlight, QColor("#00000000"))

        super(AccountView, self).drawRow(painter, option, index)

