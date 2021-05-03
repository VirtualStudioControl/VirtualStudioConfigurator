from typing import Dict, List, Tuple, Any

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from .....structs.action import Action

DATA_ROLE_ACTION_DATA = Qt.UserRole + 1
DATA_ROLE_CATEGORY_DATA = Qt.UserRole + 2

class ActionModel(QStandardItemModel):

    def __init__(self, rows, columns, parent=None):
        super(ActionModel, self).__init__(rows, columns, parent)

    def addActions(self, actions: List[Dict[str, Any]]):
        categorys: Dict[str, Tuple[dict, QStandardItem]] = {}
        root = self.invisibleRootItem()

        for action in actions:
            actionObj: Action = Action(action)
            parent = root
            cats = categorys
            cname = ""
            for cat in actionObj.category:
                cname += cat
                if cat not in cats:
                    catItem = QStandardItem(cat)
                    cats[cat] = ({}, catItem)
                    catItem.setData({'name': cname}, role=DATA_ROLE_CATEGORY_DATA)
                    parent.appendRow([catItem])
                cats, parent = cats[cat]
                cname += "."
            item = QStandardItem(actionObj.name)
            item.setData(actionObj, role=DATA_ROLE_ACTION_DATA)
            parent.appendRow([item])
