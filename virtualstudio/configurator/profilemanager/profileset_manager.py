from typing import Optional, Callable

from virtualstudio.common.profile_manager.profileset import ProfileSet

from time import sleep

from virtualstudio.configurator.profilemanager.profile_info import ProfileInfo, fromDict as profileFromDict


class ProfileState:

    def __init__(self):
        self.currentProfile = None
        self.functionBacklog = []

    def copyState(self, other):
        self.currentProfile = other.currentProfile
        self.functionBacklog = other.functionBacklog

    def clearState(self):
        self.currentProfile = None
        self.functionBacklog = []

    def appendToBacklog(self, function: Callable[[], None]):
        self.functionBacklog.append(function)

    def hasBacklog(self) -> bool:
        return len(self.functionBacklog) > 0

    def executeBacklog(self):
        for func in self.functionBacklog:
            func()


CURRENT_PROFILE_SET: Optional[ProfileSet] = None
CURRENT_PROFILE_STATE: ProfileState = ProfileState()

NEXT_PROFILE_STATE: ProfileState = ProfileState()


AWAITING_NEW_SET = False


def loadProfileSetFromDict(values: dict):
    def fromDict(dict):
        hardwareFamily = dict["hardwareFamily"]
        profileSet = ProfileSet(hardwareFamily)

        for profileDict in dict["profiles"]:
            profileSet.appendProfile(profileFromDict(profileDict))

        return profileSet

    global CURRENT_PROFILE_SET, AWAITING_NEW_SET
    CURRENT_PROFILE_SET = fromDict(values)
    CURRENT_PROFILE_STATE.copyState(NEXT_PROFILE_STATE)
    NEXT_PROFILE_STATE.clearState()
    AWAITING_NEW_SET = False
    if CURRENT_PROFILE_STATE.hasBacklog():
        CURRENT_PROFILE_STATE.executeBacklog()




def expectNewProfileSet():
    global AWAITING_NEW_SET
    AWAITING_NEW_SET = True


def addProfile(profile: ProfileInfo):
    if AWAITING_NEW_SET:
        def __wrapBacklog():
            addProfile(profile)

        NEXT_PROFILE_STATE.appendToBacklog(__wrapBacklog)
        return

    if CURRENT_PROFILE_SET is not None:
        CURRENT_PROFILE_SET.appendProfile(profile)
        setCurrentProfile(profileName=profile.name)


def setCurrentProfile(profileName: str):
    if AWAITING_NEW_SET:
        NEXT_PROFILE_STATE.currentProfile = profileName
        return
    CURRENT_PROFILE_STATE.currentProfile = profileName


def getCurrentProfileName():
    if AWAITING_NEW_SET:
        return NEXT_PROFILE_STATE.currentProfile
    return CURRENT_PROFILE_STATE.currentProfile


def getProfileByName(name: str):
    if AWAITING_NEW_SET:
        sleep(0.1)

    return CURRENT_PROFILE_SET.getProfile(name)