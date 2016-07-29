
"""
Script to scan a source folder against a target folder,
and report which files a are NEW (not in target)
and which files are OLD (they ARE in target).

USAGE:
newOrOld.py <source directory> <target directory> [options]
"""

import datetime
from optparse import OptionParser
import os
import sys


###############################################################
# Define some defaults:

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_VERBOSE = range(3)
logVerbosity = LOG_VERBOSE

###############################################################
#usage() - prints out the usage text, from the top of this file :-)
def usage():
	print __doc__

###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog  <source directory>	<target directory> [options]')
parser.add_option('-w', '--warnings', dest='warnings', action='store_const',
				   const=LOG_WARNINGS, default=LOG_VERBOSE,
				   help='show only warnings (default: show all output)')

(options, args) = parser.parse_args()
if(len(args) != 2):
	usage()
	sys.exit(2)
logVerbosity = options.warnings

## ============================ BEGIN CLASSES ===================================
class FileDetails:
	"""holds details about a file, including modified time"""
	def __init__(self, filePath):
		self.dateTimeStamp = getFileModTime(filePath)
		self.fileName = getFileName(filePath)
		self.filePath = filePath
		self.fileSize = os.path.getsize(filePath)

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

def process(sourceDirPath, targetDirPath):
	printOut("Processing source dir: " + sourceDirPath)
	#list all in source
	srcFiles = getListOfFiles(sourceDirPath)
	printOut("Source dir: " + str(len(srcFiles)) + " files.")
	#list all in target
	targetFiles = getListOfFiles(targetDirPath)
	printOut("Target dir: " + str(len(targetFiles)) + " files.")
	#group by size
	#xxx use a class GroupBySize - {size:101, srcFiles:[], targetFiles:[], id:x}
	#for each group:
	# for each srcF in srcFiles:
	#   for each tF in tgtFiles:
	#     if(cF(srcF, tF) == CompareResult.Identical):
	#       srcF.IsNew = False
	#
	#report the results

def getListOfFiles(dir):
	localFilesFound = []
	basedir = dir
	subdirlist = []
	
	filesInDir = []
	try:
		filesInDir = os.listdir(dir)
	except WindowsError:
		printOut("Error occurred accessing directory " + dir);
		return 0
	
	for filename in filesInDir:
		filePath = os.path.join(basedir,filename)
		if os.path.isfile(filePath):
			printOut ("File found: " + filePath)
			localFilesFound.append(FileDetails(filePath))
		else:
			subdirlist.append(filePath)
	for subdir in subdirlist:
		try:
			localFilesFound = localFilesFound + getListOfFiles(subdir)
		except WindowsError:
			printOut("Error occurred accessing directory " + subdir);
	return localFilesFound

def getFileModTime(filePath):
	tm = os.path.getmtime(filePath)
	return datetime.datetime.fromtimestamp(tm)

def getFileName(filePath):
	return os.path.basename(filePath)

## ============================ END FUNCTIONS ===================================

## ============================ BEGIN MAIN ===================================

source_dirpath = args[0]
target_dirpath = args[1]

process(source_dirpath, target_dirpath)
