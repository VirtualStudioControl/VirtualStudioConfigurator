from typing import Union

from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QPalette
from PyQt5.QtWidgets import QTreeView, QStyleOptionViewItem

from ..model.actionmodel import DATA_ROLE_ACTION_DATA, DATA_ROLE_CATEGORY_DATA

class ActionView(QTreeView):

    def __init__(self, parent=None):
        super().__init__(parent)
        print("Init Action View")

    def startDrag(self, supportedActions: Union[Qt.DropActions, Qt.DropAction]) -> None:
        super().startDrag(Qt.DropAction.CopyAction)

    def dragEnterEvent(self, event):
        event.ignore()

    def dragMoveEvent(self, event):
        event.ignore()

    def dropEvent(self, event):
        event.ignore()

    def drawRow(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        actionData = index.data(role=DATA_ROLE_ACTION_DATA)
        if actionData is not None:
            option.features = option.features & ~ option.Alternate
        else:
            option.features = option.features | option.Alternate

        # Set Selection color to transparent
        option.palette.setColor(QPalette.Highlight, QColor("#00000000"))

        super(ActionView, self).drawRow(painter, option, index)