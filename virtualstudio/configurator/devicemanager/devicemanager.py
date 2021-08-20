from typing import Tuple

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

def getFamily(device: dict):
    return "{} {}".format(getManufacturer(device), getName(device))

def getIdentifier(device: dict):
    return device["identifier"]


def getCurrentProfile(device: dict):
    return device["currentProfile"]


def setCurrentProfile(device: dict, profileName: str):
    device["currentProfile"] = profileName


def hasParameters(device):
    return ("parameters" in device)

def getParameterIconResolution(device, default: Tuple[int, int] = None):
    if not hasParameters(device):
        return default

    if "icon_resolution" not in device["parameters"]:
        return default

    return device["parameters"]["icon_resolution"]


def getParameterIconFormat(device, default: str = "JPEG"):
    if not hasParameters(device):
        return default

    if "icon_format" not in device["parameters"]:
        return default

    return device["parameters"]["icon_format"]


def getParameterIconFlip(device, default: Tuple[bool, bool] = (False, False)):
    if not hasParameters(device):
        return default

    if "icon_flip" not in device["parameters"]:
        return default

    return device["parameters"]["icon_flip"]

