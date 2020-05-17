"""
Given the built ISO, creates diff patches from various Melee NTCS ISOs ot turn it into SDR.
The diffing tool we use is currently xdelta.
"""

import build
import build_config
import subprocess

from os import path


# =============== #
# "MAIN FUNCTION" #
# =============== #
if __name__ == "__main__":
    # First, check for the ISO
    sdrIsoPath = build.getBuildPath(build.ISO_FILENAME)
    if not path.exists(sdrIsoPath):
        print("SDR ISO has not been built. Run \"build iso\" to build an ISO")
        exit(1)

    # Second, check for the xdelta program
    paths = build_config.getOrCreatePathsConfigSection()
    xdeltaPath = build_config.getConfigValue(build_config.XDELTA_PATH_KEY, paths)
    build_config.validatePath(xdeltaPath, "xDelta")

    # Helper function to create a diff on one of the versions of Melee
    def createDiff(meleeIsoConfigKey: str, isoMinorVersion: int):
        # Get the path and make sure it exists
        meleeIsoPath = build_config.getConfigValue(meleeIsoConfigKey, paths)
        if not meleeIsoPath:
            print("ISO for v1.0{} not specified, skipping patch for this file".format(isoMinorVersion))
            return True  # don't error, consider it successful
        if not path.exists(meleeIsoPath):
            print("ISO for v1.0{} doesn't exist. Run configure again to specify. Skipping patch for this".format(
                isoMinorVersion))
            return True  # don't error, consider it successful
        # Get patch destination path
        patchFileName = "SDR from 1.0{}.xdelta".format(isoMinorVersion)
        patchFilePath = build.getBuildPath(patchFileName)
        # Only create the patch if the ISO is newer than the last patch created
        if path.exists(patchFilePath) and path.getmtime(sdrIsoPath) <= path.getmtime(patchFilePath):
            print("Patch for ISO for v1.0{} already up to date".format(isoMinorVersion))
            return True  # This would create the same patch as before, so we're done
        else:
            print("Starting patching for v1.0{}...".format(isoMinorVersion))
            cliStr = '"{}" -e -s "{}" "{}" "{}"'.format(xdeltaPath, meleeIsoPath, sdrIsoPath, patchFilePath)
            result = subprocess.call(cliStr)
            if result > 0:
                print("Something went wrong making patch for ISO for v1.0{}".format(isoMinorVersion))
                return False
            else:
                print("Patch for v1.0{} created at {}".format(isoMinorVersion, patchFilePath))
                return True

    # Attempt to created patches for 3 ISOs
    success0 = createDiff(build_config.ISO_1_00_PATH_KEY, 0)
    success1 = createDiff(build_config.ISO_1_01_PATH_KEY, 1)
    success2 = createDiff(build_config.ISO_1_02_PATH_KEY, 2)
    if success0 and success1 and success2:
        print("Patches created successfully!")
        exit(0)
    else:
        print("There were errors creating patches, please check output")
        exit(1)
