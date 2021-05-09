from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .abstractcontrolgraphic import *


class ButtonGraphic(AbstractControlGraphic):

    def __init__(self, ident, position, size, text: str = None, parent: QWidget = None):
        super().__init__(ident, position, size, text, parent)

        self.isActive = False
        self.brushActive = QBrush(QColor("#FFFFAA00"), Qt.Dense3Pattern)

    def getType(self):
        return CONTROL_TYPE_BUTTON

    def toDict(self):
        dict = super(ButtonGraphic, self).toDict()
        dict["active"] = self.isActive
        return dict

    def paint(self, painter, style: QStyleOptionGraphicsItem, widget=None):
        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.size[0], self.size[1], self.size[0]/10.0, self.size[1]/10.0)

        painter.setBrush(self.brushBackground)
        painter.setPen(self.pen_outline)
        painter.drawPath(path_outline.simplified())

        if self.action is not None:
            painter.setBrush(self.brushAction)
            painter.drawPath(path_outline.simplified())

        if self.isActive:
            painter.setBrush(self.brushActive)
            painter.drawPath(path_outline.simplified())

        if self.isSelected():
            painter.setBrush(self.brushSelected)
            painter.drawPath(path_outline.simplified())
