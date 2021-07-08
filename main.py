from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys
import traceback

from virtualstudio.configurator.data import constants
from virtualstudio.configurator.data.provider.com_data_provider import ComDataProvider
from virtualstudio.configurator.history.history import History
from virtualstudio.configurator.ui.windows.mainwindow import MainWindow

def dark ():
    """
    Sets the UI Colorsheme to Dark

    :return: None
    """
    dark_palette = QPalette(QColor(53, 53, 53))
    qApp.setPalette(dark_palette)


if __name__ == "__main__":
    try:
        constants.DATA_PROVIDER = ComDataProvider()
        constants.HISTORY = History()
        try:
            app = QApplication(sys.argv)
            window = MainWindow()
            dark()
            app.setStyle('Fusion')

            window.show()
            app.exec_()
        finally:
            constants.DATA_PROVIDER.close()

    except Exception as ex:
        print("UNHANDLED Exception Occured !")
        traceback.print_exc()
#endregion