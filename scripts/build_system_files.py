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


# ======= #
# HELPERS #
# ======= #

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

# ============== #
# GAME TOC (FST) #
# ============== #

class FileSystemTable:
	"""Holds all the data and methods to get and manipulate the ISO's FST"""
	m_numFiles: int
	m_fstEntries: bytearray
	m_stringTable: bytearray
	m_nextFileOffset: int
	m_fileNames: set

	@staticmethod
	def appendBytes(destinationByteArray: bytearray, sourceBytes):
		for sourceByte in sourceBytes:
			destinationByteArray.append(sourceByte)

	@staticmethod
	def appendInteger(destinationByteArray, sourceInteger):
		FileSystemTable.appendBytes(destinationByteArray, sourceInteger.to_bytes(4, byteorder="big", signed=False))

	@staticmethod
	def appendString(destinationByteArray, sourceString):
		FileSystemTable.appendBytes(destinationByteArray, sourceString.encode("ascii"))

	def __init__(self, gameTocFilePath):
		if not path.exists(gameTocFilePath):
			print("Original Game TOC does not exist")
			exit(1)
		with open(gameTocFilePath, "rb") as stockGameTocData:
			stockGameToc = bytearray(stockGameTocData.read())

		# Next, split the old TOC into 2 parts: the FST Entries and String Table, based on num files in root dir
		self.m_numFiles = int.from_bytes(stockGameToc[8:12], byteorder="big", signed=False)
		self.m_fstEntries = stockGameToc[:(self.m_numFiles * FST_ENTRY_SIZE)]
		self.m_stringTable = stockGameToc[(self.m_numFiles * FST_ENTRY_SIZE):]
		self.m_nextFileOffset = None

		# Get the full list of filenames
		self.m_fileNames = set()
		currentPos = 0
		while currentPos < len(self.m_stringTable):
			try:
				nextPos = self.m_stringTable.index(0, currentPos)
				self.m_fileNames.add(self.m_stringTable[currentPos:nextPos].decode("ascii"))
				currentPos = nextPos + 1
			except ValueError:
				break  # No more found

	def setFirstNewFileOffset(self, fileOffset):
		self.m_nextFileOffset = fileOffset

	def addEntry(self, newFilename, housingDirectory):
		"""Takes a new filename and adds it to the FST.
		Requires the directory that file currently lives, in order to calculate file size.
		"""
		assert self.m_nextFileOffset is not None  # setFirstNewFileOffset needs to be called first

		# Create the FST Entry itself
		nextStringOffset = len(self.m_stringTable)
		FileSystemTable.appendInteger(self.m_fstEntries, nextStringOffset)
		FileSystemTable.appendInteger(self.m_fstEntries, self.m_nextFileOffset)
		fileSize = path.getsize(path.join(housingDirectory, newFilename))
		FileSystemTable.appendInteger(self.m_fstEntries, fileSize)

		# When incrementing the next file offset, add the current fileSize,
		# but round up to give padding and align to disc sector
		byteSize = fileSize % ISO_BLOCK_SIZE
		if byteSize > 0:
			fileSize -= byteSize
			fileSize += ISO_BLOCK_SIZE
		self.m_nextFileOffset += fileSize

		# Now add the filename to string table
		FileSystemTable.appendString(self.m_stringTable, newFilename)
		self.m_stringTable.append(0)  # null terminator
		self.m_fileNames.add(newFilename)

		self.m_numFiles += 1

	def getBytesRepresentation(self):
		# First, set the new number of files
		numFilesBytes = self.m_numFiles.to_bytes(4, byteorder="big", signed=False)
		for i in range(4):
			self.m_fstEntries[8 + i] = numFilesBytes[i]
		# Return the full bytes
		return bytes(self.m_fstEntries + self.m_stringTable)

	def contains(self, fileName):
		return fileName in self.m_fileNames


# ================= #
# ISO.hdr FUNCTIONS #
# ================= #

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
	tocPath = path.join(buildSystemDir, GAME_TOC_FILENAME)  # Path of TOC to build to

	origSystemDataPath = path.join(build.getBuildPath(), build.ORIG_SYSDATA_FOLDER)
	if not path.isdir(origSystemDataPath):
		print("Melee ISO extraction corrupted. Clean and build again.")
		exit(1)

	# ======================== #
	# Build Game.toc (the FST) #
	# ======================== #
	fst = FileSystemTable(path.join(origSystemDataPath, GAME_TOC_FILENAME))

	# Get filenames in SDR that oren't in Melee
	sdrOnlyFilenames = []  # Running list of files unique to SDR
	for filename in listdir(buildFilesDir):  # All files SDR replaces
		if path.isdir(path.join(buildFilesDir, filename)):  # Only deal with files, not dirs
			continue
		if fst.contains(filename):  # If the file exists in Melee, skip
			continue
		# Now we know it's an SDR specific file
		sdrOnlyFilenames.append(filename)

	# Only build if there are new or changed files
	shouldBuildToc = shouldRebuild
	if not shouldRebuild:
		for filename in sdrOnlyFilenames:
			filePath = path.join(buildFilesDir, filename)
			if buildTracker.hasFileChangedSinceLastBuild(filePath):
				shouldBuildToc = True
				break

	if shouldBuildToc:
		if "FIRST_NEW_FILE_OFFSET" not in filesStructure:
			print("FIRST_NEW_FILE_OFFSET missing from game.cfg")
			exit(1)
		fst.setFirstNewFileOffset(int(filesStructure["FIRST_NEW_FILE_OFFSET"]))

		# Add the new items to the TOC
		for filename in sdrOnlyFilenames:
			fst.addEntry(filename, buildFilesDir)

		# Write new TOC to file
		with open(tocPath, "wb") as newTocFile:
			newTocFile.write(fst.getBytesRepresentation())

		# Mark files so FST is rebuilt if source files unchanged
		buildTracker.markFileAsBuilt(configFilePath)
		for filename in sdrOnlyFilenames:
			filePath = path.join(buildFilesDir, filename)
			buildTracker.markFileAsBuilt(filePath)
		buildTracker.saveTrackedData()

		print("TOC/FST file created at " + tocPath)
	else:
		print("TOC/FST file doesn't need to be rebuilt")
	
	# =============================== #
	# Build the ISO.hdr (header) file #
	# =============================== #

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
