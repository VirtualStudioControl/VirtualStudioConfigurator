from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .buttongraphic import *

class ImageButtonGraphic(ButtonGraphic):

    def __init__(self, ident: int, position, size, text: str = None, parent: QWidget = None):
        super().__init__(ident, position, size, text, parent)

    def getType(self):
        return CONTROL_TYPE_IMAGE_BUTTON

    def paint(self, painter, style: QStyleOptionGraphicsItem, widget=None):
        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.size[0], self.size[1], self.size[0]/10.0, self.size[1]/10.0)

        painter.setBrush(self.brushBackground)
        painter.setPen(self.pen_outline)
        painter.drawPath(path_outline.simplified())

        if self.isSelected:
            painter.setBrush(self.brushSelected)
            painter.drawPath(path_outline.simplified())