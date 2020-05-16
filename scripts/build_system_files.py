"""
Build script that, based on files in the sdrFiles build directory and our own configurations,
builds the Table of Contents and Header files for the SDR ISO
TODO: This probably should support files being deleted, which would shrink the FST
"""

import build
import configparser
import extract_melee_iso
from os import listdir, path


# ========= #
# CONSTANTS #
# ========= #
FST_ENTRY_SIZE = 12
ISO_BLOCK_SIZE = 0x800
CONFIG_FILE = "configs/game.cfg"
GAME_TOC_FILENAME = "Game.toc"
ISO_HDR_FILENAME = "ISO.hdr"


# ======================== #
# GAME TOC (FST) FUNCTIONS #
# ======================== #

def appendBytes(destinationByteArray, sourceBytes):
	for sourceByte in sourceBytes:
		destinationByteArray.append(sourceByte)


def appendInteger(destinationByteArray, sourceInteger):
	appendBytes(destinationByteArray, sourceInteger.to_bytes(4, byteorder="big", signed=False))


def appendString(destinationByteArray, sourceString):
	appendBytes(destinationByteArray, sourceString.encode("ascii"))


def getSdrUniqueFilenames(sdrFilesDirectory, isoRootPathDirectory):
	"""Determine which files are new files for SDR not in Melee"""
	sdrFilenames = listdir(sdrFilesDirectory)
	sdrUniqueFilenames = []
	for sdrFilename in sdrFilenames:
		sdrFilePath = path.join(sdrFilesDirectory, sdrFilename)
		if path.isdir(sdrFilePath): # Only deal with files, not dirs
			continue;
	
		possibleMeleeFilename = path.join(isoRootPathDirectory, sdrFilename)
		if not path.exists(possibleMeleeFilename): # This is SDR specific file
			sdrUniqueFilenames.append(sdrFilename)
	return sdrUniqueFilenames


def createNewToc(sdrFilesDirectory, originalSystemDataDirectory, newFilenames, nextFileOffset):
	"""Add the new files to Game.toc, making sure not to change
	existing bytes on ISO, to make xdelta smaller
	"""
	# First, get the old Game.toc data
	stockGameTocFilename = path.join(originalSystemDataDirectory, GAME_TOC_FILENAME)
	with open(stockGameTocFilename, "rb") as stockGameTocData:
		stockGameToc = bytearray(stockGameTocData.read())
		
	# Next, split the old TOC into 2 parts: the FST Entries and String Table, based on num files in root dir
	numFiles = int.from_bytes(stockGameToc[8:12], byteorder="big", signed=False)
	fstEntries = stockGameToc[:(numFiles * FST_ENTRY_SIZE)]
	stringTable = stockGameToc[(numFiles * FST_ENTRY_SIZE):]

	# Write the new number of files in the root dir
	numFiles += len(newFilenames)
	numFilesBytes = numFiles.to_bytes(4, byteorder="big", signed=False)
	for i in range(4):
		fstEntries[8 + i] = numFilesBytes[i]
	
	# Add the new items to the TOC
	for filename in newFilenames:
		nextStringOffset = len(stringTable)
		appendInteger(fstEntries, nextStringOffset)
		appendInteger(fstEntries, nextFileOffset)
		fileSize = path.getsize(path.join(sdrFilesDirectory, filename))
		appendInteger(fstEntries, fileSize)
		# When incrementing the next file offset, add the current filesize,
		# but round up to give padding and align to disc sector
		byteSize = fileSize % ISO_BLOCK_SIZE
		if byteSize > 0:
			fileSize -= byteSize
			fileSize += ISO_BLOCK_SIZE
		nextFileOffset += fileSize
		appendString(stringTable, filename)
		stringTable.append(0) # null terminator
	
	# Last, build new toc bytes and return it
	return bytes(fstEntries + stringTable)


# ================= #
# ISO.hdr FUNCTIONS #
# ================= #

def getAndValidateGameConfigSections():
	configPath = path.join(build.getBasePath(), CONFIG_FILE)
	config = configparser.ConfigParser()
	config.read(configPath)
	if "METADATA" not in config:
		print("METADATA missing from " + CONFIG_FILE)
		exit(1)
	if "FILES_STRUCTURE" not in config:
		print("FILES_STRUCTURE missing from " + CONFIG_FILE)
		exit(1)
	return config["METADATA"], config["FILES_STRUCTURE"], configPath


def getOriginalIsoHdrData(originalSystemDataPath):
	isoHdrPath = path.join(originalSystemDataPath, ISO_HDR_FILENAME)
	with open(isoHdrPath, "rb") as isoHdrFile:
		return bytearray(isoHdrFile.read())


def setIsoHdrString(destination, source, key, offset, min_length, max_length, withTerminator=False):
	"""Does validation on config item and sets the config string into ISO.hdr
	dest = The bytearray holding full ISO.hdr data
	source = The config object holding our config metadata
	key = The item in the config where our new string is
	offset = Which byte in ISO.hdr to start writing to
	min_length = The minimum length the string must be
	max_length = The maximum length the string must be
	"""
	if key not in source:
		print(key + " missing from game.cfg")
		exit(1)
	bytes = bytearray(source[key], "ascii")
	if withTerminator:
		bytes.append(0)
	if len(bytes) < min_length:
		print(key + " must be at least length " + str(min_length))
		exit(1)
	if len(bytes) > max_length:
		print(key + " must be at most length " + str(max_length))
		exit(1)
	for i in range(len(bytes)):
		destination[offset + i] = bytes[i]


def setIsoHdrByte(destination, source, key, offset):
	""" Does validation on config item and sets the config string into ISO.hdr
	dest = The bytearray holding full ISO.hdr data
	source = The config object holding our config metadata
	key = The item in the config where our new string is
	offset = Which byte in ISO.hdr to start writing to
	min_length = The minimum length the string must be
	max_length = The maximum length the string must be
	"""
	if key not in source:
		print(key + " missing from game.cfg")
		exit(1)
	byte = int(source[key])
	if byte < 0 or byte > 255:
		print(key + " must be between 0 and 255")
		exit(1)
	destination[offset] = byte


def addToIsoHdrInteger(destination, source, key, offset):
	"""Takes the value in HDR at a location and adds the value from the config
	dest = The bytearray holding full ISO.hdr data
	source = The config object holding our config metadata
	key = The item in the config that tells us how much to add by
	offset = Which byte in ISO.hdr the integer starts
	"""
	if key not in source:
		print(key + " missing from game.cfg")
		exit(1)
	addend = int(source[key])
	original = int.from_bytes(destination[offset:(offset + 4)], byteorder="big", signed=False)
	sum = addend + original
	bytes = sum.to_bytes(4, byteorder="big", signed=False)
	for i in range(len(bytes)):
		destination[offset + i] = bytes[i]


def setIsoHdrInteger(destination, source, key, offset):
	"""Like addToIsoHdrInteger except it sets the integer to the value exactly in the config"""
	if key not in source:
		print(key + " missing from game.cfg")
		exit(1)
	setIsoHdrIntegerRaw(destination, source, int(source[key]), offset)


def setIsoHdrIntegerRaw(destination, source, value, offset):
	"""Like setToIsoHdrInteger except the new value is provided as a parameter instead of from config"""
	bytes = value.to_bytes(4, byteorder="big", signed=False)
	for i in range(len(bytes)):
		destination[offset + i] = bytes[i]


# =============== #
# "MAIN FUNCTION" #
# =============== #
if __name__ == "__main__":
	# Get basic data
	buildTracker = build.BuildTracker()
	metadata, filesStructure, configFilePath = getAndValidateGameConfigSections()
	shouldRebuild = buildTracker.hasFileChangedSinceLastBuild(configFilePath)

	# Setup/Verify build directories
	buildSystemDir = build.validateOrCreateBuildPath(build.SDR_FILES_DIR, build.SYSDATA_FOLDER)
	buildFilesDir = path.normpath(path.join(buildSystemDir, ".."))

	isoRootPathDir = path.join(build.getBuildPath(), extract_melee_iso.ROOT_NODE)
	if not path.isdir(isoRootPathDir):
		print("Melee ISO root dir invalid: " + isoRootPathDir)
		exit(1)

	origSystemDataPath = path.join(build.getBuildPath(), build.ORIG_SYSDATA_FOLDER)
	if not path.isdir(origSystemDataPath):
		print("Melee ISO extraction corrupted. Clean and build again.")
		exit(1)

	# ======================== #
	# Build Game.toc (the FST) #
	# ======================== #
	sdrOnlyFilenames = getSdrUniqueFilenames(buildFilesDir, isoRootPathDir)

	# Only build if there are new or changed files
	shouldBuildToc = shouldRebuild
	if not shouldRebuild:
		for filename in sdrOnlyFilenames:
			filePath = path.join(buildFilesDir, filename)
			if buildTracker.hasFileChangedSinceLastBuild(filePath):
				shouldBuildToc = True
				break

	tocPath = path.join(buildSystemDir, GAME_TOC_FILENAME)
	if shouldBuildToc:
		if "FIRST_NEW_FILE_OFFSET" not in filesStructure:
			print("FIRST_NEW_FILE_OFFSET missing from game.cfg")
			exit(1)
		firstFileOffset = int(filesStructure["FIRST_NEW_FILE_OFFSET"])
		newToc = createNewToc(buildFilesDir, origSystemDataPath, sdrOnlyFilenames, firstFileOffset)

		# Write new TOC to file
		with open(tocPath, "wb") as newTocFile:
			newTocFile.write(newToc)

		buildTracker.markFileAsBuilt(configFilePath)
		for filename in sdrOnlyFilenames:
			filePath = path.join(buildFilesDir, filename)
			buildTracker.markFileAsBuilt(filePath)
		buildTracker.saveTrackedData()

		print("TOC/FST file created at " + tocPath)
	else:
		print("TOC/FST file doesn't need to be rebuilt")
	
	# ============================= #
	# Now to build the ISO.hdr file #
	# ============================= #

	# Only build if the config has changed or the Game.toc has changed
	if shouldRebuild or buildTracker.hasFileChangedSinceLastBuild(tocPath):
		# Setup
		isoHdrData = getOriginalIsoHdrData(origSystemDataPath)

		# Set new data
		tocLength = path.getsize(tocPath)
		setIsoHdrString(isoHdrData, metadata, "GAME_ID", 0, 4, 4)
		setIsoHdrString(isoHdrData, metadata, "MAKER_CODE", 4, 2, 2)
		setIsoHdrByte(isoHdrData, metadata, "REVISION", 7)
		setIsoHdrString(isoHdrData, metadata, "GAME_NAME", 0x20, 1, 0x3e0, True)
		addToIsoHdrInteger(isoHdrData, filesStructure, "DH_BIN_LOCATION_MOVE_BYTES", 0x400)
		addToIsoHdrInteger(isoHdrData, filesStructure, "DOL_LOCATION_MOVE_BYTES", 0x420)
		addToIsoHdrInteger(isoHdrData, filesStructure, "TOC_LOCATION_MOVE_BYTES", 0x424)
		setIsoHdrIntegerRaw(isoHdrData, filesStructure, tocLength, 0x428) # FST Size
		setIsoHdrIntegerRaw(isoHdrData, filesStructure, tocLength, 0x42C) # Max FST Size
		setIsoHdrInteger(isoHdrData, filesStructure, "NEW_USER_LENGTH", 0x434) # Max FST Size

		# Write file
		headerBuildFilePath = path.join(buildSystemDir, ISO_HDR_FILENAME)
		with open(headerBuildFilePath, "wb") as headerBuildFile:
			headerBuildFile.write(bytes(isoHdrData))

		buildTracker.markFileAsBuilt(configFilePath)
		buildTracker.markFileAsBuilt(tocPath)
		buildTracker.saveTrackedData()

		print("Header file created at " + headerBuildFilePath)
	else:
		print("Header file doesn't need to be rebuilt")
