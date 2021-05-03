import base64

from PyQt5.QtGui import QImage


class Action:
    def __init__(self, values: dict):
        self.name = values['name']
        self.category = values['category']
        self.author = values['author']
        self.version = values['version']
        self.ident = values['id']
        self.allowedControls = values['id']

        print(values)

        self.rawIcon = base64.b64decode(values["icon"].encode("utf-8"))
        self.iconImage = QImage()
        self.iconImage.loadFromData(self.rawIcon)