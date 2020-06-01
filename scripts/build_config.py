"""
Handles creation and reading of the build configuration.
If imported, gives access to functions and constants for retrieving data from the build config.
If run, creates/updates the build config file based on user's paths (which they specify)
"""

import build
import configparser
from os import path
import tkinter
from tkinter import filedialog


# ========= #
# CONSTANTS #
# ========= #
BUILD_CONFIG_PATH = "configs/build.cfg"
PATHS_SECTION_KEY = "PATHS"
ISO_PATH_KEY = "ISO_PATH"
GCR_PATH_KEY = "GCR_PATH"
DOLPHIN_PATH_KEY = "DOLPHIN_PATH"
XDELTA_PATH_KEY = "XDELTA_PATH"
ISO_1_00_PATH_KEY = "ISO_1_00_PATH"
ISO_1_01_PATH_KEY = "ISO_1_01_PATH"
ISO_1_02_PATH_KEY = "ISO_1_02_PATH"
FILE_TYPE_ALL = ("Any File", "*.*")
FILE_TYPE_ISO = ("ISO", "*.iso")
FILE_TYPE_GCM = ("GCM", "*.gcm")
FILE_TYPE_EXE = ("Executable", "*.exe")


# ======= #
# HELPERS #
# ======= #

def getBuildConfigPath():
	baseDir = build.getBasePath()
	return path.join(baseDir, BUILD_CONFIG_PATH)


def getBuildConfig(configPath=None):
	if not configPath:
		configPath = getBuildConfigPath()
	config = configparser.ConfigParser()
	if path.exists(configPath):
		config.read(configPath)
	return config


def getOrCreatePathsConfigSection(config=None):
	if not config:
		config = getBuildConfig()
	if PATHS_SECTION_KEY not in config:
		config[PATHS_SECTION_KEY] = {}
	return config[PATHS_SECTION_KEY]


def getConfigValue(key, configSection=None):
	if not configSection:
		configSection = getOrCreatePathsConfigSection()
	return configSection.get(key)


def handleConfigItem(configSection, key, prompt, fileTypes):
	"""Takes a section in a configparser and a key.
	If the key is in the section, we ask to update.
	If key is not in the section, update it.
	prompt is the prompt given in the open file dialog
	fileTypes is of form (("File Type", "*.*"), ("JPEG", "*.jpg")
	"""
	if key in configSection:
		if path.exists(configSection[key]):
			ans = input("Would you like to change " + key + " (y/n)? (currently \"" + configSection[key] + "\") ")
			if ans != 'y':
				return
	value = filedialog.askopenfilename(title=prompt,filetypes=fileTypes)
	if value:
		configSection[key] = value
	else:
		print("Skipped " + key)


def validatePath(itemPath, fileDesc):
	if not itemPath:
		print(fileDesc + " path not specified, run configure again")
		exit(1)
	if not path.exists(itemPath):
		print(fileDesc + " doesn't exist, run configure again")
		exit(1)


# =============== #
# "MAIN FUNCTION" #
# =============== #
if __name__ == "__main__":
	tkinter.Tk().withdraw()
	configPath = getBuildConfigPath()
	config = getBuildConfig(configPath)
	paths = getOrCreatePathsConfigSection(config)

	ISO_TYPES = (FILE_TYPE_ISO, FILE_TYPE_GCM, FILE_TYPE_ALL)
	handleConfigItem(paths, ISO_PATH_KEY, "Select Normal Melee ISO (NTSC)", ISO_TYPES)
	EXEC_TYPES = (FILE_TYPE_EXE, FILE_TYPE_ALL)
	handleConfigItem(paths, GCR_PATH_KEY, "Select GameCube Rebuilder Executable", EXEC_TYPES)
	handleConfigItem(paths, DOLPHIN_PATH_KEY, "Optional: Dolphin Executable", EXEC_TYPES)

	# Optional xdelta and version ISOs to make xdelta files
	handleConfigItem(paths, XDELTA_PATH_KEY, "Optional: xDelta Executable", EXEC_TYPES)
	handleConfigItem(paths, ISO_1_00_PATH_KEY, "Optional: Melee v1.00 ISO", ISO_TYPES)
	handleConfigItem(paths, ISO_1_01_PATH_KEY, "Optional: Melee v1.01 ISO", ISO_TYPES)
	handleConfigItem(paths, ISO_1_02_PATH_KEY, "Optional: Melee v1.02 ISO", ISO_TYPES)

	with open(configPath, "w") as configFile:
		config.write(configFile)
	print("Configure finished!")
	input("Press enter to continue")