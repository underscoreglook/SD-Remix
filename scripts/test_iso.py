"""
Script that takes the configured Dolphin executable and runs the built SDR ISO, if it has been built.
exits with error if Dolphin path unspecified or invalid
exits with error if iso not built
"""

import build
import build_config
import subprocess

from os import path


# =============== #
# "MAIN FUNCTION" #
# =============== #
if __name__ == "__main__":
    paths = build_config.getOrCreatePathsConfigSection()
    dolphinPath = build_config.getConfigValue(build_config.DOLPHIN_PATH_KEY, paths)
    build_config.validatePath(dolphinPath, "Dolphin")

    sdrIsoPath = build.getBuildPath(build.ISO_FILENAME)
    if not path.exists(sdrIsoPath):
        print("SDR ISO has not been built. Run \"build iso\" to build an ISO")
        exit(1)

    subprocess.Popen([dolphinPath, "-b", "-e=" + sdrIsoPath])
