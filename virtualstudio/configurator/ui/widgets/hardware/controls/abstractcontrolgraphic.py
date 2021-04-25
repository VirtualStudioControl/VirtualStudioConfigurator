from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

CONTROL_TYPE_ABSTRACT = "ABSTRACT"
CONTROL_TYPE_BUTTON = "BUTTON"
CONTROL_TYPE_IMAGEBUTTON = "IMAGEBUTTON"
CONTROL_TYPE_FADER = "FADER"
CONTROL_TYPE_ROTARYENCODER = "ROTARYENCODER"

class AbstractControlGraphic(QGraphicsItem):

    def __init__(self, ident, position, size, text: str = None, parent: QWidget = None):
        super().__init__(parent)
        self.ident = ident

        self.position = position
        self.size = size

        self.setPos(*position)

        self.text = text
        if self.text is None:
            self.text = str(ident)

        self.selectable = True

        self.pen_outline = QPen(Qt.black)
        self.brushBackground = QBrush(QColor("#FFFFFF"), Qt.SolidPattern)
        self.brushAction = QBrush(QColor("#00FF00"), Qt.DiagCrossPattern)
        self.brushSelected = QBrush(QColor("#8800AAFF"), Qt.Dense4Pattern)

        self.setFlag(self.ItemIsSelectable, self.selectable)
        self.setFlag(self.ItemIsMovable, False)

    def getType(self):
        return CONTROL_TYPE_ABSTRACT

    def toDict(self):
        r = {'ident': self.ident, 'type': self.getType(), 'position': self.position, 'size': self.size,
             'text': self.text, 'selectable': self.selectable}

        return r

    def setSelectable(self, value: bool):
        self.selectable = value
        self.setFlag(self.ItemIsSelectable, self.selectable)

    def boundingRect(self) -> QRectF:
        """Defining Qt' bounding rectangle"""
        return QRectF(
            0,
            0,
            self.size[0],
            self.size[1]
        ).normalized()

