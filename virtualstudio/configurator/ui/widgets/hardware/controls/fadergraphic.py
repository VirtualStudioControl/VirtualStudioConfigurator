from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .abstractcontrolgraphic import *


class FaderGraphic(AbstractControlGraphic):

    def __init__(self, ident, position, size, knob_size, knob_value, line_offset, text: str = None, parent: QWidget = None):
        super().__init__(ident, position, size, text, parent)
        self.knob_size = knob_size
        self.knob_value = knob_value
        self.line_offset = line_offset

        self.brush_knob = QBrush(QColor("#FF888888"), Qt.Dense6Pattern)

    def getType(self):
        return CONTROL_TYPE_FADER

    def toDict(self):
        dict = super().toDict()
        dict["knob_size"] = self.knob_size
        dict["knob_value"] = self.knob_value
        dict["line_offset"] = self.line_offset

        return dict

    def paint(self, painter : QPainter, style: QStyleOptionGraphicsItem, widget=None):
        # outline
        path_outline = QPainterPath()
        path_inner = QPainterPath()
        path_line = QPainterPath()
        rounding = min(self.size[0]/10.0, self.size[1]/10.0)
        path_outline.addRoundedRect(0, 0, self.size[0], self.size[1], rounding, rounding)

        path_inner.setFillRule(Qt.WindingFill)
        path_line.moveTo(self.size[0] / 2.0, self.line_offset + self.knob_size[1]/2)
        path_line.lineTo(self.size[0] / 2.0, self.size[1] - self.line_offset - self.knob_size[1]/2)
        path_inner.addRoundedRect((self.size[0] - self.knob_size[0]) / 2, self.line_offset + (
                    (1 - self.knob_value) * (self.size[1] - (2 * self.line_offset + self.knob_size[1]))),
                                  self.knob_size[0], self.knob_size[1], self.knob_size[0] / 10.0,
                                  self.knob_size[1] / 10.0)

        painter.setPen(self.pen_outline)
        painter.setBrush(self.brushBackground)
        painter.drawPath(path_outline)

        if self.isSelected():
            painter.setBrush(self.brushSelected)
            painter.drawPath(path_outline.simplified())

        painter.drawPath(path_line)
        painter.setBrush(self.brushBackground)
        painter.drawPath(path_inner)
        painter.setBrush(self.brush_knob)
        painter.drawPath(path_inner)
