from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .abstractcontrolgraphic import *


class RotaryEncoderGraphic(AbstractControlGraphic):

    def __init__(self, ident: int, position, size, inner_pos, inner_size, text: str = None, parent: QWidget = None):
        super().__init__(ident, position, size, text, parent)
        self.inner_size = inner_size
        self.inner_pos = inner_pos

        self.brush_knob = QBrush(QColor("#FF888888"), Qt.Dense6Pattern)

    def getType(self):
        return CONTROL_TYPE_ROTARY_ENCODER

    def toDict(self):
        dict = super().toDict()
        dict["inner_size"] = self.inner_size
        dict["inner_pos"] = self.inner_pos

        return dict

    def paint(self, painter, style: QStyleOptionGraphicsItem, widget=None):
        # outline
        path_outline = QPainterPath()
        path_outline.addEllipse(0, 0, self.size[0], self.size[1])

        path_outline.setFillRule(Qt.WindingFill)

        path_inner = QPainterPath()
        path_inner.addEllipse(self.inner_pos[0], self.inner_pos[1], self.inner_size[0], self.inner_size[1])

        painter.setBrush(Qt.NoBrush)
        painter.setBrush(self.brushBackground)
        painter.setPen(self.pen_outline)
        painter.drawPath(path_outline)

        if self.isSelected:
            painter.setBrush(Qt.NoBrush)
            painter.setPen(self.pen_selected)
            painter.drawPath(path_outline.simplified())

        painter.setPen(self.pen_outline)
        painter.setBrush(self.brush_knob)
        painter.drawPath(path_inner)
