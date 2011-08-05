"""
backup_directory.py version 1.1

Simple script to archive a directory, in order to have a backup.

You can schedule this script to run using Windows Scheduler.

usage:    backup_directory.py <source directory> <target directory to store archive> <number of backups to keep> [options]

Dependencies:
7za.exe
Python 2.5 or higher

The options are:
[-h help]
[-r result file path]
[-w show Warnings only]
[-y say Yes to all prompts (no interaction)]

Example: backup_directory.py c:\myData c:\myZipFiles 3 -w -y
"""

from optparse import OptionParser
from os.path import exists, join, pathsep
import datetime
import os
import shutil
import subprocess
import sys
import tempfile
import time


#####################################################################
#constants
PATH_TO_7ZA = "bin\\ThirdParty\\7za.exe"

#####################################################################


###############################################################
# Define some defaults:

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_ERRORS, LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_INFO, LOG_VERBOSE = range(5)
logVerbosity = LOG_VERBOSE

searchDirPath = ""

archiveDirPath = ""

numArchivesToKeep = 0

dateTimeFormat = '%Y %m %d %H:%M'

startTime = time.time()

###############################################################
#ask_ok() - prompts the user to continue
def ask_ok(prompt, retries=3, complaint='Yes or no, please!'):
	global yesAllPrompts
	if yesAllPrompts:
		print prompt + " (Y)"
		return True
	while True:
		ok = raw_input(prompt)
		if ok in ('y', 'ye', 'yes'):
			return True
		if ok in ('n', 'no', 'nop', 'nope'):
			return False
		retries = retries - 1
		if retries < 0:
			raise IOError('refusenik user')
		print complaint		

###############################################################
#printOut()
#this function prints out, according to user's options for verbosity
def printOut(txt, verb = LOG_VERBOSE, bNewLine = True):
	global logVerbosity
	if verb == LOG_ERRORS:
		txt = "!!! Error: " + txt
	elif verb == LOG_WARNINGS:
		txt = "!!! Warning: " + txt
	if(bNewLine):
		txt = txt + "\n"
	if verb == LOG_WARNINGS_ONLY:
		if logVerbosity <= LOG_WARNINGS:
			sys.stdout.write(txt)
	elif(logVerbosity >= verb):
		sys.stdout.write(txt)

###############################################################
#usage() - prints out the usage text, from the top of this file :-)
def usage():
	print __doc__

###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog <source dir path> <archive dir path> <number of archives to keep> [options]')
parser.add_option('-w', '--warnings', dest='warnings', action='store_const',
	 	 	 	const=LOG_WARNINGS, default=LOG_VERBOSE,
	 	 	 	help='show only warnings (default: show all output)')
parser.add_option('-y', '--yes', dest='yes_all', action='store_const',
	 	 	 	const=True, default=True,
	 	 	 	help='automatically say Yes to allow prompts (default: prompt user)')

(options, args) = parser.parse_args()
if(len(args) != 3):
	usage()
	sys.exit(2)
logVerbosity = options.warnings
searchDirPath = args[0]
archiveDirPath = args[1]
numArchivesToKeep = int(args[2])
yesAllPrompts = options.yes_all

###############################################################
#print out summary of the configuration, and prompt user to continue:
print "Configuration:"
print "--------------"

print "searchDirPath: " + searchDirPath + "\n"
print "archiveDirPath: " + archiveDirPath + "\n"
print "numArchivesToKeep: " + str(numArchivesToKeep) + "\n"

print ""

if logVerbosity == LOG_WARNINGS:
	print "Output will show warnings only\n"
elif logVerbosity == LOG_VERBOSE:
	print "Output is verbose\n"
else:
	print "Invalid verbosity level: " + logVerbosity
	sys.exit(1)

print "We will backup the directory " + searchDirPath + " to an archive located in the directory " + archiveDirPath

print ""

if ask_ok("Do you wish to continue ? (Y/N)"):
	#do nothing
	print "ok"
else:
	print "Exiting"
	sys.exit()
	
print ""

###############################################################
#counters

numWarnings = 0
numErrors = 0

###############################################################

def getArchiveSuffix():
	return "_auto_"

def IsFileAnArchive(filePath):
	return getArchiveSuffix() in filePath and filePath.endswith(".zip")

###############################################################
# Function to get the datetime on which the given file was last modified.
def getFileModTime(filePath):
    tm = os.path.getmtime(filePath)
    return datetime.datetime.fromtimestamp(tm)

def getFileName(filePath):
	return os.path.basename(filePath)

###############################################################
class FileDetails:
	"""holds details about a file, including modified time"""
	def __init__(self, filePath):
		self.dateTimeStamp = getFileModTime(filePath)
		self.fileName = getFileName(filePath)
		self.filePath = filePath
		self.fileSize = os.path.getsize(filePath)

def getDescOfFileDetails(fileDetails):
	descOfDetails = ""
	for fileDetail in fileDetails:
		descOfDetails = descOfDetails + fileDetail.fileName + " : " + str(fileDetail.dateTimeStamp) + ", "
	return descOfDetails

#search the archive dir for existing archives
#returns existingArchives 
def findExistingArchives(archiveDirPath):
	existingArchives = list()
	
	for filename in os.listdir(archiveDirPath):
		filePath = os.path.join(archiveDirPath,filename)
		if os.path.isfile(filePath):
			if IsFileAnArchive(filename):
				existingArchives.append(FileDetails(filePath))
	#sort the archives, starting with the newest:
	
	existingArchives = sorted(existingArchives, key=lambda fileDetails: fileDetails.dateTimeStamp)
	
	#reverse the list, so that it starts with the oldest:
	existingArchives.reverse()
	
	print "\nExisting archives found: " + getDescOfFileDetails(existingArchives)
	
	return existingArchives

#decide which archive(s) will be deleted at the end (prompt user)
#returns oldArchives
def getOldArchives(existingArchives, numArchivesToKeep):
	oldArchives = list()
	archivesToDelete = list()
	
	numArchivesToDelete = len(existingArchives) + 1 - numArchivesToKeep # we should have a total of numArchivesToKeep, after current archive has been created

	while( len(archivesToDelete) < numArchivesToDelete ):
		archivesToDelete.append(existingArchives.pop())
	
	return archivesToDelete

def promptUserIfOkToDeleteArchives(oldArchives):
	strListOfArchives = getDescOfFileDetails(oldArchives)
	print "\nOld archives found: " + strListOfArchives
	if(len(oldArchives) == 0):
		print " (none found)"
	else:
		ask_ok("Do you wish to delete the old archives ?")

def runExe(targetScriptPath, args):
	scriptWorkingDir = os.path.dirname(targetScriptPath)
	toExec = targetScriptPath + " " + args
	printOut("Running exe " + toExec)
	process = subprocess.Popen(toExec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd = scriptWorkingDir)
	#TODO - optionally send some text<ENTER> to skip password protected archvies OR look at archvie first
	(stdout_cap, stderr_cap) = process.communicate()
	if(len(stderr_cap) > 0):
		raise Exception(str(stderr_cap))
		#TODO - try to process contents of archive anyway (can have a partially successful extraction)
	printOut(" >> " + str(stdout_cap));
	if(process.returncode != 0):
		raise Exception("Process returned error code:" + str(process.returncode))

def zipFile(dirPath, archivePath):
	exe = os.path.abspath(PATH_TO_7ZA)
	args = 'a "' + os.path.abspath(archivePath) +'" "' +  os.path.abspath(dirPath) + '" -tzip -mx7 -y' #.zip and high compression
	runExe(exe, args)

def getUniqueArchiveName(searchDirPath, archiveDirPath):
	numZipId = 0
	bIsUniquePath = False
	newArchiveFileName = ""
	#TODO - make this a bit smarter, so that numbers ALWAYS go up, even when old archives are deleted.
	while(not bIsUniquePath):
		numZipId = numZipId + 1
		newArchiveFileName = getFileName(searchDirPath) + getArchiveSuffix() + str(numZipId) + ".zip"
		newArchiveAbsPath = os.path.abspath(archiveDirPath + "\\" + newArchiveFileName)
		bIsUniquePath = not os.path.exists(newArchiveAbsPath)
	return newArchiveFileName

#make the zip of the source dir, to TEMP
#returns newArchiveFilePath
def createArchive(searchDirPath, archiveDirPath):
	tempDirPath = tempfile.gettempdir()
	newArchiveFilePath = tempDirPath + "\\" + getUniqueArchiveName(searchDirPath, archiveDirPath)
	#xxx next line is temporary!
	if os.path.exists(newArchiveFilePath):
		os.remove(newArchiveFilePath)
	zipFile(searchDirPath, newArchiveFilePath)
	return newArchiveFilePath

#move the zip to the archive dir
def moveFile(newArchiveFilePath, archiveDirPath):
	if(len(newArchiveFilePath) == 0):
		raise Exception("newArchiveFilePath is empty!")
	shutil.move(newArchiveFilePath, archiveDirPath)

#delete the old archive(s)
def deleteFiles(oldArchives):
	for pathDetails in oldArchives:
		os.remove(pathDetails.filePath)

def getElapsedTime(startTime):
	elapsed = (time.time() - startTime)
	elapsedTime = time.localtime( elapsed )
	dateTimeFormat = '%H hours %M minutes %S seconds'
	return (time.strftime(dateTimeFormat, elapsedTime))

#print a summary
def printSummary(numWarnings, numErrors, numOldArchives, searchDirPath, newArchiveFilePath, startTime):
	print "Archived the directory " + searchDirPath + " to the archive file " + newArchiveFilePath
	print str(numWarnings) + " warnings occurred"
	print str(numErrors) + " errors occurred"
	print str(numOldArchives) + " old archives were deleted"
	print("Time taken: " + getElapsedTime(startTime))

###############################################################
#main

#1. search the archive dir for existing archives
existingArchives = findExistingArchives(archiveDirPath)

#2. decide which archive(s) will be deleted at the end (prompt user)
oldArchives = getOldArchives(existingArchives, numArchivesToKeep)

promptUserIfOkToDeleteArchives(oldArchives)

#3. make the zip of the source dir, to TEMP
newArchiveFilePath = createArchive(searchDirPath, archiveDirPath)

#4. move the zip to the archive dir
moveFile(newArchiveFilePath, archiveDirPath)

#5. delete the old archive(s)
deleteFiles(oldArchives)

#6. print a summary
printSummary(numWarnings, numErrors, len(oldArchives), searchDirPath, newArchiveFilePath, startTime)
