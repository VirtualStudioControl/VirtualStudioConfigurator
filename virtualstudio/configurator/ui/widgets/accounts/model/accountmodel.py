from typing import List, Dict, Any, Tuple

from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QMimeData, Qt, QVariant, QDataStream
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeWidgetItem

from virtualstudio.common.account_manager.account_info import AccountInfo, fromDict
from virtualstudio.configurator.data.mimetypes import MIME_TYPE_NULL, MIME_TYPE_ACCOUNT

DATA_ROLE_ACCOUNT_DATA = Qt.UserRole + 1
DATA_ROLE_CATEGORY_DATA = Qt.UserRole + 2



class AccountModel(QStandardItemModel):

    def __init__(self, rows, columns, parent=None):
        super(AccountModel, self).__init__(rows, columns, parent)
        self.categorys: Dict[str, Tuple[dict, QStandardItem]] = {}

    def addAccounts(self, accounts: List[Dict[str, Any]]):
        root = self.invisibleRootItem()

        for account in accounts:
            actionObj: AccountInfo = fromDict(account)
            parent = root
            cats = self.categorys
            cname = ""
            for cat in actionObj.account_category:
                cname += cat
                if cat not in cats:
                    catItem = QStandardItem(cat)
                    cats[cat] = ({}, catItem)
                    catItem.setData({'name': cname}, role=DATA_ROLE_CATEGORY_DATA)
                    catItem.setSelectable(False)
                    parent.appendRow([catItem])
                cats, parent = cats[cat]
                cname += "."
            item = QStandardItem(actionObj.accountTitle)
            item.setData(actionObj, role=DATA_ROLE_ACCOUNT_DATA)
            parent.appendRow([item])
            #self.rowsInserted(parent, parent.rowCount()-1, parent.rowCount())

    def addAccount(self, account: AccountInfo):
        parent = self.invisibleRootItem()
        cats = self.categorys
        cname = ""

        for cat in account.account_category:
            cname += cat
            if cat not in cats:
                catItem = QStandardItem(cat)
                cats[cat] = ({}, catItem)
                catItem.setData({'name': cname}, role=DATA_ROLE_CATEGORY_DATA)
                catItem.setSelectable(False)
                parent.appendRow([catItem])
            cats, parent = cats[cat]
            cname += "."
        item = QStandardItem(account.accountTitle)
        item.setData(account, role=DATA_ROLE_ACCOUNT_DATA)
        parent.appendRow([item])
        #self.reset()

    def canDropMimeData(self, data, action, row, column, parent):
        if parent.data(role=DATA_ROLE_ACCOUNT_DATA) is None:
            return True
        return False

    def reset(self):
        self.sort(0)

    def decodeMime(self, input_data):
        data = []
        item = {}
        ds = QDataStream(input_data)
        while not ds.atEnd():
            ds.readInt32()
            ds.readInt32()
            map_items = ds.readInt32()
            for i in range(map_items):
                key = ds.readInt32()
                value = QVariant()
                ds >> value
                item[Qt.ItemDataRole(key)] = value
            data.append(item)
        return data

    def dropMimeData(self, data: QMimeData, action: Qt.DropAction, row: int, column: int, parent: QModelIndex):
        if super(AccountModel, self).dropMimeData(data, action, row, column, parent):
            data_items = self.decodeMime(data.data('application/x-qabstractitemmodeldatalist'))
            it = QStandardItem()
            for data in data_items:
                for r, v in data.items():
                    it.setData(v.value(), r)
            account: AccountInfo = it.data(role=DATA_ROLE_ACCOUNT_DATA)

            self.updateCategory(account, parent)

            return True
        return False

    def updateCategory(self, account: AccountInfo, parent: QModelIndex):
        category = []
        p = parent
        while p.isValid():
            category.insert(0, p.data())
            p = p.parent()
        account.account_category = category
