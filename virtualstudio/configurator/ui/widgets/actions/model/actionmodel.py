from typing import Dict, List, Tuple, Any

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QMimeData, QModelIndex
from PyQt5.QtGui import QStandardItemModel, QStandardItem

from .....structs.action import Action
from virtualstudio.configurator.data.mimetypes import MIME_TYPE_ACTIONID, MIME_TYPE_NULL

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
                    catItem.setSelectable(False)
                    parent.appendRow([catItem])
                cats, parent = cats[cat]
                cname += "."
            item = QStandardItem(actionObj.name)
            item.setData(actionObj, role=DATA_ROLE_ACTION_DATA)
            parent.appendRow([item])

    def mimeData(self, indexes: List[QModelIndex]):
        action: Action = indexes[0].data(role=DATA_ROLE_ACTION_DATA)
        mimedata = QMimeData()

        if action is not None:
            mimedata.setData(MIME_TYPE_ACTIONID, action.ident.encode("utf-8"))
        else:
            mimedata.setData(MIME_TYPE_NULL, b'')

        return mimedata

    def supportedDropActions(self):
        return QtCore.Qt.MoveAction

    def canDropMimeData(self, data, action, row, column, parent):
        print('can drop called on')
        print(parent.data())
        return True

    def dropMimeData(self, data, action, row, column, parent):
        parent_name = parent.data()
        node_name = data.text()
        print("Dropped {} onto {}".format(node_name, parent_name))
        return True