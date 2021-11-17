from typing import Optional, Callable

from PyQt5.QtCore import *
from PyQt5.QtGui import QPen, QBrush, QColor, QPainterPath, QKeyEvent, QTransform
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsSceneDragDropEvent, QGraphicsItem, QGraphicsSceneMouseEvent

from .hardwaregraphic import *
from .selectionmanager import SelectionManager


class HardwareScene(QGraphicsScene):

    def __init__(self, parent: QObject = None, selectionChangeEvent: Callable[[Optional[AbstractControlGraphic]], None] = None):
        super().__init__(parent)

        self.setBackgroundBrush(Qt.white)

        self.hardware: Optional[HardwareGraphic] = None

        self.pen_outline = QPen(Qt.black)
        self.brushDevice = QBrush(QColor("#444444"), Qt.BDiagPattern)

        self.borderOffset = 5

        self.isMoveEvent = False
        self.isMouseTranslateStart = False

        self.selectionManager = SelectionManager(self)
        self.selectionManager.setSelectionChangeHandler(selectionChangeEvent)
        self.selectionChanged.connect(self.onSelectionChanged)

    def setHardware(self, hardware: HardwareGraphic):
        for item in self.items():
            self.removeItem(item)

        if self.hardware is not None:
            self.hardware.setUpdateListener(None)

        for itm in hardware.getItems():
            self.addItem(itm)

        self.hardware = hardware
        self.hardware.setUpdateListener(self.updateItems)
        self.updateSceneRect()

    def updateItems(self):
        for item in self.items():
            self.removeItem(item)
        for itm in self.hardware.getItems():
            self.addItem(itm)

    def updateSceneRect(self):
        x, y, w, h = self.hardware.bb
        self.setSceneRect(x-self.borderOffset, y-self.borderOffset, w+self.borderOffset*2, h+self.borderOffset*2)

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            try:
                item = self.itemAt(event.scenePos(), QTransform())
                if isinstance(item, AbstractControlGraphic) or item is None:
                    self.selectionManager.setSelected(item)
                    self.update()
            except Exception as ex:
                print(ex)

    def onSelectionChanged(self) -> None:
        pass
#        if self.__ignoreSelectionEvents:
#            return
#        itemsSelected = self.selectedItems()
#
#        if len(itemsSelected) > 1:
#            self.__ignoreSelectionEvents = True
#            for i in range(0, len(itemsSelected)):
#                itemsSelected[i].setSelected(False)
#            self.selectionManager.selectedControl.setSelected(True)
#            self.__ignoreSelectionEvents = False
#            return
#
#        self.selectionManager.setSelected(itemsSelected[0])
#        print("selecionChanged", len(itemsSelected))
#
#        self.update()

    def canDropMimeData(self, data, action, row, column, parent):
        return True

    #region Rendering
    def drawBackground(self, painter, rect):
        """
        Draws the Background for this Scene

        :param painter: Painter to paint the background with
        :param rect: the Viewport for painting the background
        :return: None
        """
        super().drawBackground(painter, rect)

        if self.hardware is not None:
            path_outline = QPainterPath()
            path_outline.addRoundedRect(*self.hardware.bb, self.hardware.borderrounding, self.hardware.borderrounding)
            painter.setBrush(self.brushDevice)
            painter.setPen(self.pen_outline)
            painter.drawPath(path_outline.simplified())
    #endregion