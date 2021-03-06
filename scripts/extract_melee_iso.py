"""
Build script for extracting the Melee ISO to the build directory.
Exits with 1 if there's a failure and files were not extracted.
"""

import build
import build_config as Config
import shutil
import subprocess

from os import path


# ========= #
# CONSTANTS #
# ========= #
ROOT_NODE = "root"


# =============== #
# "MAIN FUNCTION" #
# =============== #
if __name__ == "__main__":
	# First, make sure directory structure is set up
	buildPath = build.validateOrCreateBuildPath()
		
	# If already extracted, then don't extract
	meleeFilesPath = path.join(buildPath, build.MELEE_FILES_DIR)
	if path.exists(meleeFilesPath):
		print("Melee ISO already extracted, skipping")
		exit(0) # Considered a success
		
	# Get and validate paths of external items
	paths = Config.getOrCreatePathsConfigSection()
	isoPath = Config.getConfigValue(Config.ISO_PATH_KEY, paths)
	Config.validatePath(isoPath, "Melee NTSC ISO")
	gcrPath = Config.getConfigValue(Config.GCR_PATH_KEY, paths)
	Config.validatePath(gcrPath, "GameCube Rebuilder")
		
	# Do the extraction, from the iso, extracting the root node, to the build directory
	cliStr = "\"" + gcrPath + "\" \"" + isoPath + "\" \"" + ROOT_NODE + "\" e \"" + buildPath + "\""
	print("Extracting Melee ISO: " + cliStr)
	result = subprocess.call(cliStr)
	if result == 0:
		sourceSystemDataPath = path.join(meleeFilesPath, build.SYSDATA_FOLDER)
		destSystemDataPath = path.join(buildPath, build.ORIG_SYSDATA_FOLDER)
		shutil.copytree(sourceSystemDataPath, destSystemDataPath)
		print("Melee ISO extracted successfully!")
	else:
		print("Something went wrong extracting the ISO")
		shutil.rmtree(meleeFilesPath)
	exit(result)