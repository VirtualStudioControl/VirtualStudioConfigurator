from typing import Tuple

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from .buttongraphic import *

class ImageButtonGraphic(ButtonGraphic):

    def __init__(self, ident: int, position, size, text: str = None, parent: QWidget = None):
        super().__init__(ident, position, size, text, parent)

        self.iconImage = None
        self.iconFlip = (False, False)

    def getType(self):
        return CONTROL_TYPE_IMAGE_BUTTON

    def setIconImage(self, iconImage: Optional[QImage], iconFlip: Tuple[bool, bool] = (False, False)):
        self.iconImage = iconImage
        self.iconFlip = iconFlip
        self.update()

    def paint(self, painter, style: QStyleOptionGraphicsItem, widget=None):
        # outline
        try:
            path_outline = QPainterPath()
            path_outline.addRoundedRect(0, 0, self.size[0], self.size[1], self.size[0]/10.0, self.size[1]/10.0)

            painter.setBrush(self.brushBackground)
            painter.setPen(self.pen_outline)
            painter.drawPath(path_outline.simplified())

            if self.iconImage is not None:
                painter.setClipPath(path_outline.simplified(), Qt.ClipOperation.ReplaceClip)
                painter.drawImage(QRectF(0, 0, self.size[0], self.size[1]),
                              self.iconImage.mirrored(*self.iconFlip))
                painter.setClipPath(path_outline.simplified(), Qt.ClipOperation.NoClip)
                painter.setBrush(Qt.NoBrush)

            painter.drawPath(path_outline.simplified())

            if self.isSelected:
                #painter.setBrush(self.brushSelected)
                painter.setPen(self.pen_selected)
                painter.drawPath(path_outline.simplified())
        except Exception as ex:
            print(ex)