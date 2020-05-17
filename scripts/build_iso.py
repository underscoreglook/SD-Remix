"""
Build script that takes the extracted Melee ISO files, copies the SD Remix files, and creates an ISO from them.
Exits with 1 if there was a failure (missing files or configs, or builder failed)
"""

import build
import build_config as Config
import shutil
import subprocess

from os import listdir, path, remove


# ======= #
# HELPERS #
# ======= #

def copyDirectory(sourceDirectory, destinationDirectory):
    """Recursively copies the files in the source directory to the destination directory if the source file is newer.
    If any files were copied, returns True
    """
    filenames = listdir(sourceDirectory)
    copied = False
    for filename in filenames:
        sourceFilePath = path.join(sourceDirectory, filename)
        destFilePath = path.join(destinationDirectory, filename)
        if path.isdir(sourceFilePath):
            if path.isdir(destFilePath):
                if copyDirectory(sourceFilePath, destFilePath):
                    copied = True
        else:
            if not path.exists(destFilePath) or path.getmtime(sourceFilePath) != path.getmtime(destFilePath):
                shutil.copy2(sourceFilePath, destFilePath)
                copied = True
    return copied


# =============== #
# "MAIN FUNCTION" #
# =============== #
if __name__ == "__main__":
    # Get and validate directories
    meleeFilesDir = build.getBuildPath(build.MELEE_FILES_DIR)
    build.validateDirectory(meleeFilesDir)
    sdrFilesDir = build.getBuildPath(build.SDR_FILES_DIR)
    build.validateDirectory(sdrFilesDir)
    buildIsoPath = build.getBuildPath(build.ISO_FILENAME)

    # Go through all the SDR Files, copy any changed files
    print("Attempting to copy SDR files...")
    if not copyDirectory(sdrFilesDir, meleeFilesDir) and path.exists(buildIsoPath):
        print("No files change, no need to rebuild")
        exit(0)  # Considered success
    print("Files copied successfully")

    # Build the ISO
    paths = Config.getOrCreatePathsConfigSection()
    gcrPath = Config.getConfigValue(Config.GCR_PATH_KEY, paths)
    Config.validatePath(gcrPath, "GameCube Rebuilder")
    cliStr = "\"" + gcrPath + "\" \"" + meleeFilesDir + "\" \"" + buildIsoPath + "\""
    print("Building SD Remix ISO: " + cliStr)
    result = subprocess.call(cliStr)
    if result == 0:
        print("ISO Build successfully at " + buildIsoPath)
    else:
        print("Something went wrong building the ISO")
        if path.exists(buildIsoPath):
            remove(buildIsoPath)
    exit(result)