from typing import Dict, Any, Optional, List

from virtualstudio.common.logging import logengine
from virtualstudio.common.structs.profile.profile import Profile
from .controls.abstractcontrolgraphic import AbstractControlGraphic
from .controls.buttongraphic import ButtonGraphic
from .controls.imagebuttongraphic import ImageButtonGraphic
from .controls.rotaryencodergraphic import RotaryEncoderGraphic
from .controls.fadergraphic import FaderGraphic

logger = logengine.getLogger()


class HardwareGraphic:

    def __init__(self, name: str, bezel: float = 0.0, borderrounding: float = 0.0, layers: int = 1, layerNames: Optional[List[str]] = None):
        self.name = name

        self.items: List[Dict[Any, AbstractControlGraphic]] = []
        self.bezel = bezel
        self.borderrounding = borderrounding

        self.layers = layers
        for _ in range(layers):
            self.items.append({})

        self.layerNames = layerNames
        if self.layerNames is None:
            self.layerNames = []

        self.activeLayer = 0

        self.updated = None

        self.bb = (0, 0, 1, 1)

    def toDict(self):
        r = {}
        r['name'] = self.name
        r['bezel'] = self.bezel
        r['borderrounding'] = self.borderrounding
        r['activeLayer'] = self.activeLayer
        r['layerCount'] = self.layers
        r['layerNames'] = self.layerNames

        layers = []
        for i in range(self.layers):
            layers.append([])
            for item in self.getItems(i):
                layers[i].append(item.toDict())
        r['layers'] = layers
        return r

    def onUpdate(self):
        if self.updated is not None:
            self.updated()

    def setUpdateListener(self, updateFunc=None):
        self.updated = updateFunc

    def setBezel(self, bezel):
        self.bezel = bezel
        self.onUpdate()

    def setActiveLayer(self, layer):
        self.activeLayer = layer
        self.onUpdate()

    def getNameOfLayer(self, layer):
        if layer < len(self.layerNames):
            return self.layerNames[layer]
        return "Layer {}".format(layer)

    def getItems(self, layer=None):
        if layer is None:
            layer = self.activeLayer
        return self.items[layer].values()

    def getItem(self, ident: int, layer=None):
        if layer is not None:
            return self.items[layer][ident]
        for lay in range(self.layers):
            if ident in self.items[lay]:
                return self.items[lay][ident]
        return None

    def addItem(self, item: AbstractControlGraphic, layer=None):
        if layer is None:
            layer = self.activeLayer
        self.items[layer][item.ident] = item
        self.onUpdate()

    def setProfile(self, profile: Profile):
        if profile is None:
            logger.fatal("Got Profile which is None !")
            return

        for item in self.getItems():
            if item.ident in profile.actions:
                item._setAction(profile.actions[item.ident])
            else:
                item._setAction(None)

    def computeBB(self):
        x, y, w, h = (0, 0, 0, 0)

        for layer in range(self.layers):
            for k in self.items[layer]:
                x = min(x, self.items[layer][k].position[0])
                y = min(y, self.items[layer][k].position[1])
                w = max(w, self.items[layer][k].position[0] + self.items[layer][k].size[0])
                h = max(h, self.items[layer][k].position[1] + self.items[layer][k].size[1])

        self.bb = (x - self.bezel, y - self.bezel, (w-x) + self.bezel*2, (h-x) + self.bezel*2)

        self.onUpdate()


def createElgatoStreamdeck():
    streamDeck = HardwareGraphic(name="Elgato StreamDeck", bezel=40, borderrounding=20)

    for i in range(3):
        for j in range(5):
            streamDeck.addItem(ImageButtonGraphic(i*5+j, (45*j, 45*i), (40, 40), "({} , {})".format(j, i)))

    streamDeck.computeBB()
    return streamDeck


def createElgatoStreamdeckMini():
    streamDeck = HardwareGraphic(name="Elgato StreamDeck Mini", bezel=40, borderrounding=20)

    for i in range(2):
        for j in range(3):
            streamDeck.addItem(ImageButtonGraphic(i*3+j, (45*j, 45*i), (40, 40), "({} , {})".format(j, i)))

    streamDeck.computeBB()
    return streamDeck


def createElgatoStreamdeckXL():
    streamDeck = HardwareGraphic(name="Elgato StreamDeck XL", bezel=40, borderrounding=20)

    for i in range(4):
        for j in range(8):
            streamDeck.addItem(ImageButtonGraphic(i*8+j, (45*j, 45*i), (40, 40), "({} , {})".format(j, i)))

    streamDeck.computeBB()
    return streamDeck


def createXTouchCompact():
    xtouch = HardwareGraphic(name="Behringer X Touch Compact", bezel=20, borderrounding=20, layers=2, layerNames=['A', 'B'])

    controls = 0

    for i in range(3):
        for j in range(8):
            xtouch.addItem(ButtonGraphic(controls, (15 + 65 * j, 80 + 40 * i), (30, 20), "{}".format(controls)), layer=0)
            controls += 1

    for i in range(8):
        xtouch.addItem(ButtonGraphic(controls, (15 + 65 * i, 520), (30, 20), "{}".format(controls)), layer=0)
        controls += 1

    xtouch.addItem(ButtonGraphic(controls, (545, 520), (30, 20), "{}".format(controls)), layer=0)
    controls += 1

    for i in range(3):
        for j in range(2):
            xtouch.addItem(ButtonGraphic(controls, (620 + 65 * j, 310 + 70 * i), (30, 20), "{}".format(controls)), layer=0)
            controls += 1

    isActive = True
    for i in range(2):
        btn = ButtonGraphic(997 + i, (620 + 65 * i, 520), (30, 20), "{}".format(controls))
        btn.isActive = isActive
        btn.setSelectable(False)
        isActive = not isActive
        xtouch.addItem(btn, layer=0)
        #controls += 1

    for i in range(8):
        xtouch.addItem(FaderGraphic(controls, (65 * i, 200), (60, 300), (30, 60), 0, 10, "{}".format(controls)), layer=0)
        controls += 1

    xtouch.addItem(FaderGraphic(controls, (530, 200), (60, 300), (30, 60), 0, 10, "{}".format(controls)), layer=0)
    controls += 1

    for i in range(8):
        xtouch.addItem(RotaryEncoderGraphic(controls, (i*65, 0), (60, 60), (15, 15), (30, 30), "{}".format(controls)), layer=0)
        controls += 1

    for i in range(4):
        for j in range(2):
            xtouch.addItem(RotaryEncoderGraphic(controls, (605 + 65 * j, 70 * i), (60, 60), (15, 15), (30, 30), "{}".format(controls)), layer=0)
            controls += 1

    # Layer B

    for i in range(3):
        for j in range(8):
            xtouch.addItem(ButtonGraphic(controls, (15 + 65 * j, 80 + 40 * i), (30, 20), "{}".format(controls)), layer=1)
            controls += 1

    for i in range(8):
        xtouch.addItem(ButtonGraphic(controls, (15 + 65 * i, 520), (30, 20), "{}".format(controls)), layer=1)
        controls += 1

    xtouch.addItem(ButtonGraphic(controls, (545, 520), (30, 20), "{}".format(controls)), layer=1)
    controls += 1

    for i in range(3):
        for j in range(2):
            xtouch.addItem(ButtonGraphic(controls, (620 + 65 * j, 310 + 70 * i), (30, 20), "{}".format(controls)), layer=1)
            controls += 1

    isActive = False
    for i in range(2):
        btn = ButtonGraphic(999 + i, (620 + 65 * i, 520), (30, 20), "{}".format(controls))
        btn.isActive = isActive
        btn.setSelectable(False)
        isActive = not isActive
        xtouch.addItem(btn, layer=1)
        #controls += 1

    xtouch.computeBB()

    for i in range(8):
        xtouch.addItem(FaderGraphic(controls, (65 * i, 200), (60, 300), (30, 60), 0, 10, "{}".format(controls)), layer=1)
        controls += 1

    xtouch.addItem(FaderGraphic(controls, (530, 200), (60, 300), (30, 60), 0, 10, "{}".format(controls)), layer=1)
    controls += 1

    for i in range(8):
        xtouch.addItem(RotaryEncoderGraphic(controls, (i*65, 0), (60, 60), (15, 15), (30, 30), "{}".format(controls)), layer=1)
        controls += 1

    for i in range(4):
        for j in range(2):
            xtouch.addItem(RotaryEncoderGraphic(controls, (605 + 65 * j, 70 * i), (60, 60), (15, 15), (30, 30), "{}".format(controls)), layer=1)
            controls += 1


    return xtouch


def createXTouchMini():
    xtouch = HardwareGraphic(name="Behringer X Touch Mini", bezel=20, borderrounding=20, layers=2,
                             layerNames=['A', 'B'])

    controls = 0

    xtouch.addItem(FaderGraphic(controls, (530, 0), (60, 160), (20, 40), 0, 10, "{}".format(controls)), layer=0)
    controls += 1

    for i in range(8):
        xtouch.addItem(RotaryEncoderGraphic(controls, (i * 65, 0), (60, 60), (15, 15), (30, 30), "{}".format(controls)), layer=0)
        controls += 1

    for i in range(2):
        for j in range(8):
            xtouch.addItem(ButtonGraphic(controls, (15 + 65 * j, 80 + 40 * i), (30, 20), "{}".format(controls)), layer=0)
            controls += 1

    isActive = True
    for i in range(2):
        btn = ButtonGraphic(999+i, (615, 80 + 40 * i), (30, 20), "{}".format(controls))
        btn.isActive = isActive
        btn.setSelectable(False)
        isActive = not isActive
        xtouch.addItem(btn, layer=0)
        #controls += 1

    xtouch.addItem(FaderGraphic(controls, (530, 0), (60, 160), (20, 40), 0, 10, "{}".format(controls)), layer=1)
    controls += 1

    for i in range(8):
        xtouch.addItem(RotaryEncoderGraphic(controls, (i * 65, 0), (60, 60), (15, 15), (30, 30), "{}".format(controls)), layer=1)
        controls += 1

    for i in range(2):
        for j in range(8):
            xtouch.addItem(ButtonGraphic(controls, (15 + 65 * j, 80 + 40 * i), (30, 20), "{}".format(controls)), layer=1)
            controls += 1

    isActive = False
    for i in range(2):
        btn = ButtonGraphic(999+i, (615, 80 + 40 * i), (30, 20), "{}".format(controls))
        btn.isActive = isActive
        btn.setSelectable(False)
        isActive = not isActive
        xtouch.addItem(btn, layer=1)
        #controls += 1

    xtouch.computeBB()
    return xtouch