"""
Build script for extracting the Melee ISO to the build directory.
Exits with 1 if there's a failure and files were not extracted.
"""

import build
import build_config as Config
import subprocess

from os import path


# ========= #
# CONSTANTS #
# ========= #
ROOT_NODE = "root"


# ======= #
# HELPERS #
# ======= #

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
	# First, make sure directory structure is set up
	buildPath = build.validateOrCreateBuildPath()
		
	# If already extracted, then don't extract
	rootPath = path.join(buildPath, ROOT_NODE)
	if path.exists(rootPath):
		print("Melee ISO already extracted, skipping")
		exit(0) # Considered a success
		
	# Get and validate paths of external items
	paths = Config.getOrCreatePathsConfigSection()
	isoPath = Config.getConfigValue(Config.ISO_PATH_KEY, paths)
	validatePath(isoPath, "Melee NTSC ISO")
	gcrPath = Config.getConfigValue(Config.GCR_PATH_KEY, paths)
	validatePath(gcrPath, "GameCube Rebuilder")
		
	# Do the extraction, from the iso, extracting the root node, to the build directory
	cliStr = "\"" + gcrPath + "\" \"" + isoPath + "\" \"" + ROOT_NODE + "\" e \"" + buildPath + "\""
	print("Extracting Melee ISO: " + cliStr)
	result = subprocess.call(cliStr)
	if result == 0:
		print("Melee ISO extracted successfully!")
	else:
		print("Something went wrong extracting the ISO")
	exit(result)