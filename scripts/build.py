"""
build.py
A module designed to house constants and functions shared across the build system.
@author _glook
"""

from os import path, mkdir
import pickle


# ========= #
# CONSTANTS #
# ========= #
BUILD_FOLDER = "build"
SYSDATA_FOLDER = "&&systemdata"
ORIG_SYSDATA_FOLDER = "OrigSystemData"
SDR_FILES_DIR = "sdrFiles"
CHARS_FOLDER = 'chars'
STAGES_FOLDER = "stages"
MENUS_FOLDER = "menus"
DOL_FOLDER = "dol"


# ========= #
# FUNCTIONS #
# ========= #

def getBasePath():
    return path.normpath(path.join(path.dirname(__file__), ".."))


def getPathFromBase(*directories):
    return path.normpath(path.join(getBasePath(), *directories))


def getBuildPath():
    return getPathFromBase(BUILD_FOLDER)


def validateOrCreatePath(absolutePath):
    absolutePath = path.abspath(absolutePath)
    if not path.exists(absolutePath):
        # make sure parent paths exist
        validateOrCreatePath(path.join(absolutePath, ".."))
        mkdir(absolutePath)
    elif not path.isdir(absolutePath):
        print(absolutePath + " must be a directory")
        exit(1)
    return absolutePath


def validateOrCreateBuildPath(*directories):
    buildPath = getBuildPath()
    if len(directories) > 0:
        buildPath = path.join(buildPath, *directories)
    return validateOrCreatePath(buildPath)


# ======= #
# CLASSES #
# ======= #

class BuildTracker:
    """Keeps track of build metadata. Basically stores state between builds to make subsequent builds optimized."""
    # Constants
    BUILD_TRACKER_FILE = ".build_tracker"  # should be hidden
    # Type hints
    trackedData: dict

    def __init__(self):
        trackerFilePath = BuildTracker._getTrackerFilePath()
        if path.exists(trackerFilePath):
            with open(trackerFilePath, "rb") as file:
                self.trackedData = pickle.load(file)
        else:
            self.trackedData = {}

    @staticmethod
    def _getTrackerFilePath():
        return path.join(getBuildPath(), BuildTracker.BUILD_TRACKER_FILE)

    def saveTrackedData(self):
        if self.trackedData:
            trackerFilePath = BuildTracker._getTrackerFilePath()
            with open(trackerFilePath, "wb") as file:
                pickle.dump(self.trackedData, file, pickle.HIGHEST_PROTOCOL)

    def hasFileChangedSinceLastBuild(self, sourceFilePath):
        """Returns true if the file at path sourceFilename has been modified since the last time we've built.
        Relies that the file was marked as built with markFileAsBuilt
        """
        oldModifiedTime = self.trackedData.get(sourceFilePath)
        if not oldModifiedTime:
            return True  # If file was never built, always true
        modifiedTime = path.getmtime(sourceFilePath)
        return modifiedTime > oldModifiedTime

    def markFileAsBuilt(self, sourceFilePath):
        """Marks a source file as having been built already so we don't rebuilt it unnecessarily later"""
        self.trackedData[sourceFilePath] = path.getmtime(sourceFilePath)
