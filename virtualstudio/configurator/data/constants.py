from typing import Optional

from .provider.abstract_data_provider import AbstractDataProvider
from ..history.history import History

#region General
from ..ui.widgets.hardware.controls.abstractcontrolgraphic import AbstractControlGraphic

from virtualstudio.common.account_manager.account_info import AccountInfo

DATA_PROVIDER: Optional[AbstractDataProvider] = None

HISTORY: Optional[History] = None

CURRENT_DEVICE = None

SELECTED_CONTROL: Optional[AbstractControlGraphic] = None

CURRENT_ACCOUNT: Optional[AccountInfo] = None

#endregion


#region Image Dialog

IMAGEDIALOG_LAST_PATH = ""

FILTER_FILEDIALOG_IMAGEFILES = "Image Files (*.png *.jpg *.jpeg *.bmp);; " \
                               "PNG (*.png);; " \
                               "JPEG (*.jpg *.jpeg);; " \
                               "Bitmap (*.bmp)"

#endregion