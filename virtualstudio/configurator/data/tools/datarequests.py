from virtualstudio.common.structs.profile.profile import Profile
from .. import constants


def updateProfile(profile: Profile):
    deviceID = constants.CURRENT_DEVICE

    def __cb(profileset: dict, success: bool):
        pass

    constants.DATA_PROVIDER.updateProfile(deviceID, profile, __cb)
