"""
Build script that sets up the SDR files directory (similar to Melee root structure except only SDR changed files)
Also copies all the SDR specific files from their locations in the source files, except for Game.toc and ISO.hdr
TODO: This should probably support files being deleted as well
"""

import build
from os import listdir, path
import shutil 


# ======= #
# HELPERS #
# ======= #

def copyFiles(destDir, sourceFolder):
	"""sourceFolder: The folder to copy files from, relative to root of repo"""
	sourceDir = build.getPathFromBase(sourceFolder)
	filenames = listdir(sourceDir)
	for filename in filenames:
		sourceFile = path.join(sourceDir, filename)
		if not path.isfile(sourceFile):
			continue
		destinationFile = path.join(destDir, filename)
		# Only copy file if the source is newer (or if destination doesn't exist)
		if (not path.exists(destinationFile)) or (path.getmtime(destinationFile) != path.getmtime(sourceFile)):
			shutil.copy2(sourceFile, destinationFile)


# =============== #
# "MAIN FUNCTION" #
# =============== #
if __name__ == "__main__":
	filesDir = build.validateOrCreateBuildPath(build.SDR_FILES_DIR)
	copyFiles(filesDir, build.CHARS_FOLDER)
	copyFiles(filesDir, build.STAGES_FOLDER)
	copyFiles(filesDir, build.MENUS_FOLDER)

	sysdataDir = build.validateOrCreateBuildPath(build.SDR_FILES_DIR, build.SYSDATA_FOLDER)
	copyFiles(sysdataDir, build.DOL_FOLDER)

	print(filesDir + " set up and source files copied")
