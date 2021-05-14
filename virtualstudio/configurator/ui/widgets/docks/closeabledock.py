from typing import Callable, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QDockWidget


class CloseableDock(QDockWidget):
    
    def __init__(self, parent=None, flags=Qt.WindowFlags()):
        super(CloseableDock, self).__init__(parent, flags)

        self.onClose: Optional[Callable[[], None]] = None

    def setOnClose(self, onClose: Optional[Callable[[], None]] = None):
        self.onClose = onClose

    def closeEvent(self, event: QCloseEvent):
        if self.onClose is not None:
            self.onClose()
        super(CloseableDock, self).closeEvent(event)
