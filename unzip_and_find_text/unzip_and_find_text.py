"""
 unzip_and_find_text.py
 Author: Sean Ryan
 Version: 1.1

 Script to unzip an archive, and find text inside it.
 
Usage: unzip_and_find_text.py <search dir path> <regular expression> [options]

The options are:
[-h help]
[-r result file path]
[-w show Warnings only]
[-y say Yes to all prompts (no interaction)]

Example: unzip_and_find_text.py c:\myZipFiles "sheep" -w -y
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
import stat
import sys
import tempfile
import time
import traceback

###############################################################
# Define some defaults:

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_ERRORS, LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_INFO, LOG_VERBOSE = range(5)
logVerbosity = LOG_VERBOSE

searchDirPath = ""
regEx = ""
yesAllPrompts = True #to allow super-script to call this script

extensions_of_archives  = ['rar', 'zip']
extensions_of_text_files = ['txt', 'log']
extensions = [ 'log', 'rar', 'zip']
tempDir = tempfile.gettempdir()
defaultResultFilePath = tempDir + "\\log_file_search_result.txt"
resultFilePath = defaultResultFilePath

dateTimeFormat = '%Y %m %d %H:%M'

pathTo7zExe = "C:\\7-Zip\\7z.exe"

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
#usage() - prints out the usage text, from the top of this file :-)
def usage():
	print __doc__

###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog <search dir path> <regular expression> [options]')
parser.add_option('-r', '--resultfile', dest='resultFilePath', type='string', nargs=1,
	 	 	 	default=defaultResultFilePath,
	 	 	 	help='show only warnings (default: show all output)')
parser.add_option('-w', '--warnings', dest='warnings', action='store_const',
	 	 	 	const=LOG_WARNINGS, default=LOG_VERBOSE,
	 	 	 	help='show only warnings (default: show all output)')
parser.add_option('-y', '--yes', dest='yes_all', action='store_const',
	 	 	 	const=True, default=True,
	 	 	 	help='automatically say Yes to allow prompts (default: prompt user)')

#TODO - add a way to specifiy a LIST of search strings - maybe in a text file.
#				then we can speed up the search, by searching for multiple strings at once
#				this may make output harder to read ?
				
(options, args) = parser.parse_args()
if(len(args) != 2):
	usage()
	sys.exit(2)
logVerbosity = options.warnings
searchDirPath = args[0]
regEx = args[1]
resultFilePath = options.resultFilePath
yesAllPrompts = options.yes_all

###############################################################
#print out summary of the configuration, and prompt user to continue:
print "Configuration:"
print "--------------"

print "searchDirPath: " + searchDirPath + "\n"
print "regEx: " + regEx + "\n"

print ""

if logVerbosity == LOG_WARNINGS:
	print "Output will show warnings only\n"
elif logVerbosity == LOG_VERBOSE:
	print "Output is verbose\n"
else:
	print "Invalid verbosity level: " + logVerbosity
	sys.exit(1)

print "We will search the directory " + searchDirPath + " for archives and uncompresssed log files, that contain the given regular expression."

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
iNumErrors = 0
iNumArchivesFoundWithText = 0
iNumArchivesProcessed = 0 #includes embedded archives
iNumTopLevelFilesProcessed = 0 #excludes embedded archives
iNumTopLevelFiles = 0

###############################################################
def ensureDirExists(dirPath):
	#create the directory if it does not exist:
	if not os.path.exists(dirPath):
		os.mkdir(dirPath)

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
def getFileExtension(filename):
	iPosLastStop = filename.rfind(".")
	if(iPosLastStop >= 0):
		return filename.lower()[iPosLastStop + 1:]
	else:
		return ""

def IsFileAnArchive(filename):
	global extensions_of_archives
	if(getFileExtension(filename) in extensions_of_archives):
		return True
	else:
		return False

def IsFileATextFile(filename):
	global extensions_of_text_files
	if(getFileExtension(filename) in extensions_of_text_files):
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
#search_files - recursively search the given directory, and populate the map with files that match our list of extensions
#
#returns: the number of files found
def search_files(dir, result_dict):
	global numWarnings
	basedir = dir
	#print "Files in ", dir, ": "
	subdirlist = []
	iNumFiles = 0
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
				iNumFiles = iNumFiles + 1
		else:
			subdirlist.append(os.path.join(basedir, filename))
	for subdir in subdirlist:
		iNumFiles = iNumFiles + search_files(subdir, result_dict)
	return iNumFiles

###############################################################
def clearOutDir(dirPath):
	if os.access(dirPath, os.R_OK):
		shutil.rmtree(dirPath, False, onerror=remove_readonly) #False = do NOT ignore errors
	os.mkdir(dirPath)

def remove_readonly(fn, path, excinfo):
    if fn is os.rmdir:
        os.chmod(path, stat.S_IWRITE)
        os.rmdir(path)
    elif fn is os.remove:
        os.chmod(path, stat.S_IWRITE)
        os.remove(path)
	
def copyFile(srcPath, destPath):
	shutil.copy(srcPath, destPath)

def getFileName(filePath):
	return os.path.basename(filePath)

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

def unrarFile(archivePath, extractedPath):
	#just use 7z again :-)
	unzipFile(archivePath, extractedPath)

def unzipFile(archivePath, extractedPath):
	exe = pathTo7zExe
	args = 'x "' + os.path.abspath(archivePath) + '" -o"' + os.path.abspath(extractedPath) + '" -y'
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

#TODO - make a class for the Result File
def appendToResultFile(text):
	global text_file
	global dateTimeFormat
	timeNow = datetime.datetime.now()
	text_file.write(timeNow.strftime(dateTimeFormat) + " - " + text + "\n")
	printOut("\n" + text)

def flushResultFile():
	global text_file
	text_file.flush()

def writeToResultFile(archivePath, regEx, foundInFiles):
	appendToResultFile("=================================")
	appendToResultFile("Found text '" + regEx + "' in the file: " + archivePath)
	appendToResultFile("=================================")
	appendToResultFile("The text was found in " + str(len(foundInFiles)) + " files:")
	appendToResultFile("\n".join(foundInFiles))
	appendToResultFile("=================================")
	appendToResultFile("")

###############################################################
#process the archives:
def processArchives(archiveFilePaths, regEx, archiveParentName = ""):
	global numWarnings, iNumErrors, iNumTopLevelFiles, iNumTopLevelFilesProcessed, unzippedDir
	for fileName in archiveFilePaths:
		srcFilePathSet = archiveFilePaths[fileName]
		for archivePath in srcFilePathSet:
			try: #to allow further archives to be processed
				archiveHierarchicalName = archiveParentName + "_" + getFileName(archivePath)
				appendToResultFile("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
				appendToResultFile("Processing archive or uncompressed log: " + archivePath)
				extractedPath = unzippedDir + archiveHierarchicalName
				unzipArchive(archivePath, extractedPath)
				#get list of the extracted files:
				targetFilePaths = dict()
				search_files(extractedPath, targetFilePaths)
				#check for embedded archives - we process these, recursively
				embeddedArchiveFilePaths = dict()
				for archiveFileName in targetFilePaths:
					if(IsFileAnArchive(archiveFileName)):
						embeddedArchiveFilePaths[archiveFileName] = targetFilePaths[archiveFileName]
						printOut("Found an embedded archive " + archiveFileName)
				#search the files:
				searchFilesForText(archivePath, targetFilePaths, regEx, extractedPath)
				#process the embedded archives:
				processArchives(embeddedArchiveFilePaths, regEx, archiveHierarchicalName)
				clearOutDir(extractedPath)
			except Exception as ex:
				traceback.print_exc(file=sys.stdout)
				printOut("Error occurred with archive " + archivePath + " - " + str(ex), LOG_ERRORS)
				print type(ex)     # the exception instance
				print ex.args      # arguments stored in .args
				iNumErrors = iNumErrors + 1
			except:
				traceback.print_exc(file=sys.stdout)
				printOut("Error occurred with archive " + archivePath + " - " + str(sys.exc_info()[0]), LOG_ERRORS)
				iNumErrors = iNumErrors + 1
			#flush our output, to keep the output up to date:
			flushResultFile()
			sys.stdout.flush()
			if(len(archiveParentName) == 0):
				iNumTopLevelFilesProcessed = iNumTopLevelFilesProcessed + 1
				printOut ( "\r>> Progress: " + str((iNumTopLevelFilesProcessed * 100) / iNumTopLevelFiles) + "%", LOG_INFO, False ) #show some progress, even if low verbosity

###############################################################
#search the files:
#TODO - support RegEx not just text search
def searchFilesForText(archivePath, targetFilePaths, regEx, extractedPath):
	printOut("\nSearching archive: " + archivePath)
	global iNumArchivesFoundWithText, iNumArchivesProcessed, numWarnings
	foundInFiles = []
	for fileName in targetFilePaths:
		if(IsFileATextFile(fileName)):
			srcFilePathSet = targetFilePaths[fileName]
			for srcFilePath in srcFilePathSet:
				printOut ("\nSearching file " + srcFilePath)
				iNumFoundInFile = findTextInFile(srcFilePath, regEx)
				if(iNumFoundInFile > 0):
					extractedRelativePath = srcFilePath[len(extractedPath):]
					foundInFiles.append(extractedRelativePath)
		else:
			printOut("Not searching text in file " + fileName, LOG_WARNINGS)
			numWarnings = numWarnings + 1
	if(len(foundInFiles) > 0):
		writeToResultFile(archivePath, regEx, foundInFiles)
		iNumArchivesFoundWithText = iNumArchivesFoundWithText + 1
	iNumArchivesProcessed = iNumArchivesProcessed + 1

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

def getElapsedTime(startTime):
	elapsed = (time.time() - startTime)
	elapsedTime = time.localtime( elapsed )
	dateTimeFormat = '%H hours %M minutes %S seconds'
	return (time.strftime(dateTimeFormat, elapsedTime))

###############################################################
#main process:
text_file = open(resultFilePath, 'a')

appendToResultFile("Beginning prcoessing...")

#make the unzipped location be named after the result file, to allow for concurrent instances
unzippedDir = tempDir + "\\unzipped_log_archive__" + getFileName(resultFilePath) + "\\"
ensureDirExists(unzippedDir)
clearOutDir(unzippedDir)

#find archives + uncompressed log files:
printOut("Searching for archive files and uncompressed logs ...")
archiveFilePaths = dict()
iNumTopLevelFiles = search_files(searchDirPath, archiveFilePaths)

#process the archives:
processArchives(archiveFilePaths, regEx)

clearOutDir(unzippedDir)
os.rmdir(unzippedDir)

###############################################################
#print summary of results		
summary = ""
summary += "\n" + ""
summary += "\n" + "Text was found in " + str(iNumArchivesFoundWithText) + " files"
summary += "\n" + str(iNumTopLevelFilesProcessed) + " top level files were processed"
summary += "\n" + str(iNumArchivesProcessed) + " top level files and embedded archives were processed"
summary += "\n" + str(numWarnings) + " warnings occurred"
summary += "\n" + str(iNumErrors) + " errors occurred"

appendToResultFile(summary)

appendToResultFile("Time taken: " + getElapsedTime(startTime))

appendToResultFile("Finished prcoessing.")

text_file.close()

if(iNumErrors > 0):
	raise Exception("Errors occurred!")
