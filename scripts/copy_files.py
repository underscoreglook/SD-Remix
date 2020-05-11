from os import listdir, path
import shutil 

# sourceFolder: The folder to copy files from, relative to root of repo
def copyFilesToBuildRoot(rootDir, sourceFolder):
	sourceDir = path.join(scriptDir, "..", sourceFolder)
	filenames = listdir(sourceDir)
	for filename in filenames:
		sourceFile = path.join(sourceDir, filename)
		if not path.isfile(sourceFile):
			continue
		destFile = path.join(rootDir, filename)
		shutil.copyfile(sourceFile, destFile)

if __name__ == "__main__":
	scriptDir = path.dirname(__file__)
	rootDir = path.join(scriptDir, "../build/root")

	# First, check that the build/root dir exists
	if not path.isdir(rootDir):
		print("root directory does not exist")
		exit(1)
	copyFilesToBuildRoot(rootDir, "chars")
	copyFilesToBuildRoot(rootDir, "stages")
	copyFilesToBuildRoot(rootDir, "menus")