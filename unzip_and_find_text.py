"""
 unzip_and_find_text.py
 Author: Sean Ryan
 Version: 1.0

 Script to unzip an archive, and find text inside it.
 
Usage: unzip_and_find_text.py <archive file path> <regular expression> [options]

The options are:
[-h help]
[-w show Warnings only]
[-y say Yes to all prompts (no interaction)]

Example: unzip_and_find_text.py c:\myZip.zip ".*sheep.*" -w -y
"""
###############################################################
import datetime
from datetime import date
import getopt
from optparse import OptionParser
import os
#pathsep ; on windows  , on unix
from os.path import exists, join, pathsep
import re
import shutil
from string import split
import subprocess
import sys
import tempfile
import time

###############################################################
# Define some defaults:

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_VERBOSE = range(3)
logVerbosity = LOG_VERBOSE

archivePath = ""
regEx = ""
yesAllPrompts = True #to allow super-script to call this script

extensions_to_warn = ['rar', 'zip']
extensions = [ 'log']
tempDir = tempfile.gettempdir()
resultFilePath = tempDir + "\\log_file_search_result.txt"

dateTimeFormat = '%Y %m %d %H:%M'

pathTo7zExe = "C:\\7-Zip\\7z.exe"

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
#usage() - prints out the usage text, from the top of this file :-)
def usage():
	print __doc__

###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog <archive file path> <regular expression> [options]')
parser.add_option('-w', '--warnings', dest='warnings', action='store_const',
	 	 	 	const=LOG_WARNINGS, default=LOG_VERBOSE,
	 	 	 	help='show only warnings (default: show all output)')
parser.add_option('-y', '--yes', dest='yes_all', action='store_const',
	 	 	 	const=True, default=True,
	 	 	 	help='automatically say Yes to allow prompts (default: prompt user)')

(options, args) = parser.parse_args()
if(len(args) != 2):
	usage()
	sys.exit(2)
logVerbosity = options.warnings
archivePath = args[0]
regEx = args[1]
yesAllPrompts = options.yes_all

###############################################################
#print out summary of the configuration, and prompt user to continue:
print "Configuration:"
print "--------------"

print "archivePath: " + archivePath + "\n"
print "regEx: " + regEx + "\n"

print ""

if logVerbosity == LOG_WARNINGS:
	print "Output will show warnings only\n"
elif logVerbosity == LOG_VERBOSE:
	print "Output is verbose\n"
else:
	print "Invalid verbosity level: " + logVerbosity
	sys.exit(1)

print "We will search the archive " + archivePath + " for the given regular expression."

print ""

if ask_ok("Do you wish to continue ? (Y/N)"):
	#do nothing
	print "ok"
else:
	print "Exiting"
	sys.exit()
	
print ""

numWarnings = 0

###############################################################

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

###############################################################
def getFileExtension(filename):
	iPosLastStop = filename.rfind(".")
	if(iPosLastStop >= 0):
		return filename.lower()[iPosLastStop + 1:]
	else:
		return ""

def IsFileExtensionNotExpected(filename):
	global extensions_to_warn
	if(getFileExtension(filename) in extensions_to_warn):
		return True
	else:
		return False

def IsFileExtensionOk(filename):
	global extensions
	for ext in extensions:
		if (filename.lower().endswith("." + ext.lower())):
			return True
	return False

###############################################################
#search for files that were extracted from the archive:

###############################################################
#search_files - recursively search the given directory, and populate the map with files that match our list of extensions
def search_files(dir, result_dict):
	basedir = dir
	#print "Files in ", dir, ": "
	subdirlist = []
	for filename in os.listdir(dir):
		if os.path.isfile(os.path.join(basedir,filename)):
			if IsFileExtensionOk(filename):
				printOut ("File found: " + filename)
				setOfPaths = set()
				if (filename in result_dict):
					setOfPaths = result_dict[filename]
				else:
					result_dict[filename] = setOfPaths
				setOfPaths.add( os.path.join(basedir, filename) )
			if IsFileExtensionNotExpected(filename):
				printOut("Warning: unexpected file found: " + filename, LOG_WARNINGS)
				numWarnings = numWarnings + 1
		else:
			subdirlist.append(os.path.join(basedir, filename))
	for subdir in subdirlist:
		search_files(subdir, result_dict)

###############################################################
def clearOutDir(dirPath):
	if os.access(dirPath, os.R_OK):
		shutil.rmtree(dirPath, False) #False = do NOT ignore errors
	os.mkdir(dirPath)

def copyFile(srcPath, destPath):
	shutil.copy(srcPath, destPath)

def getFileName(filePath):
	return os.path.basename(filePath)

def runExe(targetScriptPath, args):
	scriptWorkingDir = os.path.dirname(targetScriptPath)
	toExec = targetScriptPath + " " + args
	printOut("Running exe " + toExec)
	process = subprocess.Popen(toExec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd = scriptWorkingDir)
	(stdout_cap, stderr_cap) = process.communicate()
	if(len(stderr_cap) > 0):
		raise Exception(str(stderr_cap))
	#TODO - catch error return code !
	
def unrarFile(archivePath, extractedPath):
	#just use 7z again :-)
	unzipFile(archivePath, extractedPath)

def unzipFile(archivePath, extractedPath):
	exe = pathTo7zExe
	args = 'x "' + os.path.abspath(archivePath) + '" -o' + os.path.abspath(extractedPath)
	runExe(exe, args)

###############################################################
def unzipArchive(archivePath, extractedPath):
	clearOutDir(extractedPath)
	ext = getFileExtension(archivePath)
	if(ext == 'log'):
		#just copy the file:
		copyFile(archivePath, extractedPath + "\\" + getFileName(archivePath))
	elif(ext == 'rar'):
		#un-rar the file:
		unrarFile(archivePath, extractedPath)
		return
	elif(ext == 'zip'):
		#un-zip the file:
		unzipFile(archivePath, extractedPath)
	else:
		raise Exception ("Unrecognised extension: " + ext)
	
def appendToResultFile(text):
	global text_file
	global dateTimeFormat
	#timeNow = date.fromtimestamp(time.time())
	timeNow = datetime.datetime.now()
	text_file.write(timeNow.strftime(dateTimeFormat) + " - " + text + "\n")
	printOut("\n" + text)

def writeToResultFile(archivePath, regEx, foundInFiles):
	appendToResultFile("=================================")
	appendToResultFile("Found text '" + regEx + "' in the file: " + archivePath)
	appendToResultFile("=================================")
	appendToResultFile("The text was found in " + str(len(foundInFiles)) + " files:")
	appendToResultFile("\n".join(foundInFiles))
	appendToResultFile("=================================")
	appendToResultFile("")

###############################################################
#search the files:
#TODO - support RegEx not just text search
def searchFilesForText(archivePath, targetFilePaths, regEx, extractedPath):
	printOut("\nSearching archive: " + archivePath)
	foundInFiles = []
	for fileName in targetFilePaths:
		srcFilePathSet = targetFilePaths[fileName]
		for srcFilePath in srcFilePathSet:
			printOut ("\nSearching file " + srcFilePath)
			iNumFoundInFile = findTextInFile(srcFilePath, regEx)
			if(iNumFoundInFile > 0):
				extractedRelativePath = srcFilePath[len(extractedPath):]
				foundInFiles.append(extractedRelativePath)
	if(len(foundInFiles) > 0):
		writeToResultFile(archivePath, regEx, foundInFiles)

###############################################################
#find the given text, in the give txt file.
#returns: the number of instances found
def findTextInFile(textSrcFilePath, textToFind):
	iNumFound = 0
	textToFind = textToFind.lower()
	srcFile = open(textSrcFilePath, "r")
	for line in srcFile:
		line = line.lower()
		if (line.find(textToFind) >= 0):
			iNumFound = iNumFound + 1
	return iNumFound

###############################################################
#main process:
text_file = open(resultFilePath, 'a')
appendToResultFile("Searching archive or uncompressed log: " + archivePath)

extractedPath = tempDir + "\\unzipped_log_archive"
unzipArchive(archivePath, extractedPath)
#get list of the extracted files:
targetFilePaths = dict()
search_files(extractedPath, targetFilePaths)
#search the files:
searchFilesForText(archivePath, targetFilePaths, regEx, extractedPath)
text_file.close()

clearOutDir(extractedPath)

###############################################################
#print summary of results		
print ""
print str(numWarnings) + " warnings"
