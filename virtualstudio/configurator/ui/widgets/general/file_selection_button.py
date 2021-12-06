import base64

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QToolButton, QFileDialog

from virtualstudio.common.io import filewriter
from virtualstudio.common.logging import logengine

logger = logengine.getLogger()

class FileSelectionButton(QToolButton):

    fileselectorfilechanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._currentFile = ""
        self._text = ""
        self._file_content = None
        self._filename_filter = ""
        self.initCallbacks()

    def initCallbacks(self):
        self.clicked.connect(self.openFile)

    def text(self):
        return self._text

    def setText(self, text):
        self._text = text

    def currentFile(self):
        return self._currentFile

    def setCurrentFile(self, currentFile: str):
        self._currentFile = currentFile
        super().setText(self._currentFile)

    def fileContent(self):
        return self._file_content

    def filenameFilter(self):
        return self._filename_filter

    def setFilenameFilter(self, filenameFilter: str):
        self._filename_filter = filenameFilter

    def openFile(self, triggered=False):
        try:
            self._currentFile = QFileDialog.getOpenFileName(self, self._text, self._currentFile, self._filename_filter)[0]
            super().setText(self._currentFile)
            if self._currentFile == "":
                self._file_content = None
                return

            self._file_content = base64.b64encode(filewriter.readFileBinary(self._currentFile)).decode("utf-8")

            self.fileselectorfilechanged.emit()
        except Exception as ex:
            logger.debug("Error Opening file: {}".format(self._currentFile))
            logger.exception(ex)
