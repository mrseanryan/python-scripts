
"""
Script to scan a folder for 'similar' files:
- same or similar name (using renaming behaviour used by Samsung S3, S7)
- similar size (differ by only 500 bytes or so)

note: does NOT check the file content!

USAGE:
findSimilarFiles.py <directory> [options]
"""

import datetime
from optparse import OptionParser
import os
import sys
import time

###############################################################
# Define some defaults:

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_VERBOSE = range(3)
logVerbosity = LOG_VERBOSE

FILE_SIZE_TOLERANCE_BYTES = 100 * 1024

END_LINE = "\n"

###############################################################
#usage() - prints out the usage text, from the top of this file :-)
def usage():
	print __doc__

###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog <directory> [options]')
parser.add_option('-w', '--warnings', dest='warnings', action='store_const',
				   const=LOG_WARNINGS, default=LOG_VERBOSE,
				   help='show only warnings (default: show all output)')

(options, args) = parser.parse_args()
if(len(args) != 1):
	usage()
	sys.exit(2)
logVerbosity = options.warnings

startTime = time.time()

## ============================ BEGIN CLASSES ===================================
class FileDetails:
	"""holds details about a file, including modified time"""
	def __init__(self, filePath):
		self.dateTimeStamp = getFileModTime(filePath)
		self.fileName = getFileName(filePath)
		self.filePath = filePath
		self.fileSize = os.path.getsize(filePath)
		self.similarFiles = []
		self.normFileName = normalizeFileName(self.fileName)
		
	def addSimilarFile(self, fileDetail):
		self.similarFiles.append(fileDetail)

## ============================ BEGIN FUNCTIONS ===================================

###############################################################
#printOut()
#this function prints out, according to user's options for verbosity
def printOut(txt, verb = LOG_VERBOSE, bNewLine = True):
	global logVerbosity
	if(bNewLine):
		txt = txt + "\n"
	if verb == LOG_WARNINGS_ONLY:
		if logVerbosity == LOG_WARNINGS: #special case :-(
			sys.stdout.write(txt)
	elif(logVerbosity >= verb):
		sys.stdout.write(txt)

def process(dirPath, startTime):
	printOut("Processing dir: " + dirPath)
	#list all in dir
	srcFiles = getListOfFiles(dirPath)
	printOut("Source dir: " + str(len(srcFiles)) + " files.")
	processFiles(srcFiles)
	reportResults(srcFiles, startTime)

def processFiles(srcFiles):
	for i in range(0, len(srcFiles)):
		srcF = srcFiles[i]
		for j in range(i+1, len(srcFiles)):
			otherF = srcFiles[j]
			if(areFileSizesSimilar(srcF, otherF) and areFileNamesSimilar(srcF.normFileName, otherF.normFileName)):
				srcF.addSimilarFile(otherF)

def areFileNamesSimilar(fileName1, fileName2):
	#Samsumg S7 and/or Dropbox are renaming and slightly modifying photo files (rotation?),
	#resulting in duplicates :-( - but after testing, the size is also slightly different by 500 bytes or so...
	#
	#from testing: the name with the space IS rotated - so you want to keep that one...
	return fileName1 == fileName2

def normalizeFileName(fileName):
	return fileName.replace(" ", "_").replace(".","").replace("-","")

def areFileSizesSimilar(srcF, otherF):
	return abs(srcF.fileSize - otherF.fileSize) < FILE_SIZE_TOLERANCE_BYTES

def reportResults(srcFiles, startTime):
	printOut("Result:", LOG_WARNINGS)
	filesWithSimilarFiles = []
	for file in srcFiles:
		if(len(file.similarFiles) > 0):
			filesWithSimilarFiles.append(file)

	printOut("files with similar other files: (similar name, size)", LOG_WARNINGS)
	for file in filesWithSimilarFiles:
		newFileDesc = "[duplicated?] " + file.filePath
		newFileDesc += END_LINE
		for simFile in file.similarFiles:
			newFileDesc += "  [similar] " + simFile.filePath + END_LINE
		printOut(newFileDesc, LOG_WARNINGS)
	printOut(str(len(filesWithSimilarFiles)) + " possible duplicate files found.", LOG_WARNINGS)
	printOut("  note: from testing: the name with the space IS rotated - so you want to keep that one...", LOG_WARNINGS)
	printOut(str(len(srcFiles)) + " total files found.", LOG_WARNINGS)
	printOut("Time taken: " + getElapsedTime(startTime), LOG_WARNINGS)

def getListOfFiles(dir):
	localFilesFound = []
	basedir = dir
	subdirlist = []
	
	filesInDir = []
	try:
		filesInDir = os.listdir(dir)
	except WindowsError:
		printOut("Error occurred accessing directory " + dir, LOG_WARNINGS);
		return 0
	
	for filename in filesInDir:
		filePath = os.path.join(basedir,filename)
		if os.path.isfile(filePath):
			fileDets = FileDetails(filePath)
			printOut ("File found: " + fileDets.filePath + " size:" + str(fileDets.fileSize))
			localFilesFound.append(fileDets)
		else:
			subdirlist.append(filePath)
	for subdir in subdirlist:
		try:
			localFilesFound = localFilesFound + getListOfFiles(subdir)
		except WindowsError:
			printOut("Error occurred accessing directory " + subdir, LOG_WARNINGS);
	return localFilesFound

def getFileModTime(filePath):
	tm = os.path.getmtime(filePath)
	return datetime.datetime.fromtimestamp(tm)

def getFileName(filePath):
	return os.path.basename(filePath)

def getElapsedTime(startTime):
	elapsedInSeconds = (time.time() - startTime)
	
	m, s = divmod(elapsedInSeconds, 60)
	h, m = divmod(m, 60)
	return "%d hours %d mins %.2fs" % (h, m, s)

## ============================ END FUNCTIONS ===================================

## ============================ BEGIN MAIN ===================================

source_dirpath = args[0]

process(source_dirpath, startTime)
