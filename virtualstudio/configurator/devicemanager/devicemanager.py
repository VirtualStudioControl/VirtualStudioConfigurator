DEVICES = {}


def appendDevice(device: dict):
    global DEVICES
    DEVICES[device["identifier"]] = device


def appendDevices(devices: list):
    for device in devices:
        appendDevice(device)


def getDevice(identifier: str):
    return DEVICES[identifier]


def getType(device: dict):
    return device["type"]


def getName(device: dict):
    return device["name"]


def getManufacturer(device: dict):
    return device["manufacturer"]


def getIdentifier(device: dict):
    return device["identifier"]


def getCurrentProfile(device: dict):
    return device["currentProfile"]


def setCurrentProfile(device: dict, profileName: str):
    device["currentProfile"] = profileName
