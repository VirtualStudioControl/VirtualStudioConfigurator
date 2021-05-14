from typing import Optional

from .provider.abstract_data_provider import AbstractDataProvider
from ..history.history import History

DATA_PROVIDER: Optional[AbstractDataProvider] = None

HISTORY: Optional[History] = None