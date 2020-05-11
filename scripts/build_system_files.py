import configparser
from os import listdir, path


#===========#
# CONSTANTS #
#===========#
FST_ENTRY_SIZE = 12
ISO_BLOCK_SIZE = 0x800
CONFIG_FOLDER = "configs"
GAME_CFG_FILENAME = "game.cfg"
SYSTEM_DATA_FOLDER = "&&SystemData"
GAME_TOC_FILENAME = "Game.toc"
ISO_HDR_FILENAME = "ISO.hdr"


#==========================#
# GAME TOC (FST) FUNCTIONS #
#==========================#

def appendBytes(destByteArray, sourceBytes):
	for sourceByte in sourceBytes:
		destByteArray.append(sourceByte)

def appendInteger(destByteArray, sourceInteger):
	appendBytes(destByteArray, sourceInteger.to_bytes(4, byteorder="big", signed=False))

def appendString(destByteArray, sourceString):
	appendBytes(destByteArray, sourceString.encode("ascii"))

# Determine which files are new files for SDR not in Melee
def getSdrOnlyFilenames(buildRootDir, isoRootPathDir):
	sdrFilenames = listdir(buildRootDir)
	sdrOnlyFilenames = []
	for sdrFilename in sdrFilenames:
		sdrFilePath = path.join(buildRootDir, sdrFilename)
		if path.isdir(sdrFilePath): # Only deal with files, not dirs
			continue;
	
		possibleMeleeFilename = path.join(isoRootPathDir, sdrFilename)
		if not path.exists(possibleMeleeFilename): # This is SDR specific file
			sdrOnlyFilenames.append(sdrFilename)
	return sdrOnlyFilenames

# Add the new files to Game.toc, making sure not to change existing bytes on ISO, to make xdelta smaller
def createNewToc(buildRootDir, isoRootPathDir, newFilenames, nextFileOffset):
	# First, get the old Game.toc data
	stockGameTocFilename = path.join(isoRootPathDir, SYSTEM_DATA_FOLDER, GAME_TOC_FILENAME)
	stockGameToc = None
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
		fileSize = path.getsize(path.join(buildRootDir, filename))
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


#===================#
# ISO.hdr FUNCTIONS #
#===================#

def getAndValidateGameConfigSections(baseDir):
	configPath = path.join(baseDir, CONFIG_FOLDER, GAME_CFG_FILENAME)
	config = configparser.ConfigParser()
	config.read(configPath)
	if "METADATA" not in config:
		print("METADATA missing from " + GAME_CFG_FILENAME)
		exit(1)
	if "FILES_STRUCTURE" not in config:
		print("FILES_STRUCTURE missing from " + GAME_CFG_FILENAME)
		exit(1)
	return config["METADATA"], config["FILES_STRUCTURE"]
	
def getOriginalIsoHdrData(isoRootPathDir):
	isoHdrPath = path.join(isoRootPathDir, SYSTEM_DATA_FOLDER, ISO_HDR_FILENAME)
	with open(isoHdrPath, "rb") as isoHdrFile:
		return bytearray(isoHdrFile.read())

# Does validation on config item and sets the config string into ISO.hdr
# dest = The bytearray holding full ISO.hdr data
# source = The config object holding our config metadata
# key = The item in the config where our new string is
# offset = Which byte in ISO.hdr to start writing to
# min_length = The minimum length the string must be
# max_length = The maximum length the string must be
def setIsoHdrString(dest, source, key, offset, min_length, max_length, withTerminator=False):
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
		dest[offset + i] = bytes[i]

# Does validation on config item and sets the config string into ISO.hdr
# dest = The bytearray holding full ISO.hdr data
# source = The config object holding our config metadata
# key = The item in the config where our new string is
# offset = Which byte in ISO.hdr to start writing to
# min_length = The minimum length the string must be
# max_length = The maximum length the string must be
def setIsoHdrByte(dest, source, key, offset):
	if key not in source:
		print(key + " missing from game.cfg")
		exit(1)
	byte = int(source[key])
	if byte < 0 or byte > 255:
		print(key + " must be between 0 and 255")
		exit(1)
	dest[offset] = byte

# Takes the value in HDR at a location and adds the value from the config
# dest = The bytearray holding full ISO.hdr data
# source = The config object holding our config metadata
# key = The item in the config that tells us how much to add by
# offset = Which byte in ISO.hdr the integer starts
def addToIsoHdrInteger(dest, source, key, offset):
	if key not in source:
		print(key + " missing from game.cfg")
		exit(1)
	addend = int(source[key])
	original = int.from_bytes(dest[offset:(offset+4)], byteorder="big", signed=False)
	sum = addend + original
	bytes = sum.to_bytes(4, byteorder="big", signed=False)
	for i in range(len(bytes)):
		dest[offset + i] = bytes[i]
		
# Like addToIsoHdrInteger except it sets the integer to the value exactly in the config
def setIsoHdrInteger(dest, source, key, offset):
	if key not in source:
		print(key + " missing from game.cfg")
		exit(1)
	setIsoHdrIntegerRaw(dest, source, int(source[key]), offset)
		
# Like setToIsoHdrInteger except the new value is provided as a parameter instead of from config
def setIsoHdrIntegerRaw(dest, source, value, offset):
	bytes = value.to_bytes(4, byteorder="big", signed=False)
	for i in range(len(bytes)):
		dest[offset + i] = bytes[i]


#=================#
# "MAIN FUNCTION" #
#=================#
if __name__ == "__main__":
	baseDir = path.join(path.dirname(__file__), "..")
	metadata, filesStructure = getAndValidateGameConfigSections(baseDir)
	
	buildRootDir = path.join(baseDir, "build/root")
	buildSystemDir = path.join(buildRootDir, SYSTEM_DATA_FOLDER)
	
	if not path.isdir(buildSystemDir):
		print("System Data folder doesn't exist")
		exit(1)
	
	isoRootPathDirFile = path.join(baseDir, "configs", "isoRootPath.txt")
	if not path.exists(isoRootPathDirFile):
		print("configs/isRootPath.txt is not specified")
		exit(1)
	
	isoRootPathDir = None
	with open(isoRootPathDirFile, "r") as isoRootPathDirFileData:
		isoRootPathDir = isoRootPathDirFileData.readline()
	if not path.isdir(isoRootPathDir):
		print("Melee ISO root dir invalid: " + isoRootPathDir)
		exit(1)
	
	sdrOnlyFilenames = getSdrOnlyFilenames(buildRootDir, isoRootPathDir)
	if "FIRST_NEW_FILE_OFFSET" not in filesStructure:
		print("FIRST_NEW_FILE_OFFSET missing from game.cfg")
		exit(1)
	firstFileOffset = int(filesStructure["FIRST_NEW_FILE_OFFSET"])
	newToc = createNewToc(buildRootDir, isoRootPathDir, sdrOnlyFilenames, firstFileOffset)
	
	# Write new TOC to file
	newTocPath = path.join(buildSystemDir, GAME_TOC_FILENAME)
	with open(newTocPath, "wb") as newTocFile:
		newTocFile.write(newToc)
	print("TOC/FST file created")
	
	#
	# Now to build the ISO.hdr file
	#
	
	# Setup
	isoHdrData = getOriginalIsoHdrData(isoRootPathDir)
	
	# Set new data
	setIsoHdrString(isoHdrData, metadata, "GAME_ID", 0, 4, 4)
	setIsoHdrString(isoHdrData, metadata, "MAKER_CODE", 4, 2, 2)
	setIsoHdrByte(isoHdrData, metadata, "REVISION", 7)
	setIsoHdrString(isoHdrData, metadata, "GAME_NAME", 0x20, 1, 0x3e0, True)
	addToIsoHdrInteger(isoHdrData, filesStructure, "DH_BIN_LOCATION_MOVE_BYTES", 0x400)
	addToIsoHdrInteger(isoHdrData, filesStructure, "DOL_LOCATION_MOVE_BYTES", 0x420)
	addToIsoHdrInteger(isoHdrData, filesStructure, "TOC_LOCATION_MOVE_BYTES", 0x424)
	setIsoHdrIntegerRaw(isoHdrData, filesStructure, len(newToc), 0x428) # FST Size
	setIsoHdrIntegerRaw(isoHdrData, filesStructure, len(newToc), 0x42C) # Max FST Size
	setIsoHdrInteger(isoHdrData, filesStructure, "NEW_USER_LENGTH", 0x434) # Max FST Size
	
	# Write file
	headerBuildFilename = path.join(buildSystemDir, ISO_HDR_FILENAME)
	with open(headerBuildFilename, "wb") as headerBuildFile:
		headerBuildFile.write(bytes(isoHdrData))
	print("Header file created")