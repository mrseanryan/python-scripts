
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

IDENTICAL_FILES = "Identical files"
DIFFERENT_FILES = "Different files"

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

class GroupBySize:
	"""A group of files. All files in this group, have the same size."""
	def __init__(self, id, fileSize):
		self.id = id
		self.fileSize = fileSize
		self.sourceFiles = []
		self.targetFiles = []
	
	def addSourceFile(self, sourceFile):
		self.sourceFiles.append(sourceFile)
	
	def addTargetFile(self, file):
		self.targetFiles.append(file)
	
	#TODO is there a more Pythonic way to do this:
	def toString(self):
		return ( "id:" + str(self.id) +
			" file size: " + str(self.fileSize) +
			" source files: " + str(len(self.sourceFiles)) +
			" target files: " + str(len(self.targetFiles)) )

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
	groupsBySize = groupBySize(srcFiles, targetFiles)
	for fileSize in groupsBySize:
		printOutGroup(groupsBySize[fileSize])
	#TODO extract as processGroups
	for fileSize in groupsBySize:
		group = groupsBySize[fileSize]
		printOut("Processing group " + str(group.id) + " of " + str(len(groupsBySize)))
		for srcF in group.sourceFiles:
			srcF.isNew = True
			for tF in group.targetFiles:
				if(compareFiles(srcF, tF) == IDENTICAL_FILES):
					srcF.isNew = False
	#
	reportResults(srcFiles)

def reportResults(srcFiles):
	printOut("Result:")
	oldFiles = []
	newFiles = []
	for file in srcFiles:
		if(file.isNew):
			newFiles.append(file)
		else:
			oldFiles.append(file)
	printOut("old files: (they ARE duplicated in target directory)")
	for file in oldFiles:
		printOut("[old] " + file.filePath)
	printOut(str(len(oldFiles)) + " old files found.")
	printOut("new files: (they are NOT found in target directory)")
	for file in newFiles:
		printOut("[new] " + file.filePath)
	printOut(str(len(newFiles)) + " new files found.")
	printOut(str(len(oldFiles) + len(newFiles)) + " total source files.")

def compareFiles(file1, file2):
	#TODO impl me
	return IDENTICAL_FILES
	
def groupBySize(srcFiles, targetFiles):
	fileSizeToGroup = dict()
	for srcFile in srcFiles:
		if srcFile.fileSize not in fileSizeToGroup:
			fileSizeToGroup[srcFile.fileSize] = GroupBySize(len(fileSizeToGroup), srcFile.fileSize)
		group = fileSizeToGroup[srcFile.fileSize]
		group.addSourceFile(srcFile)
		for tgtFile in targetFiles:
			if srcFile.fileSize == tgtFile.fileSize:
				group.addTargetFile(tgtFile)
	return fileSizeToGroup

def printOutGroup(group):
	printOut("Group: ")
	printOut(group.toString())

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
			fileDets = FileDetails(filePath)
			printOut ("File found: " + fileDets.filePath + " size:" + str(fileDets.fileSize))
			localFilesFound.append(fileDets)
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
