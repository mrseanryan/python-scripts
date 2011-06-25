"""
 find_files_by_size.py
 Author: Sean Ryan
 Version: 1.1

 Script to recursively find files with matching size.

Dependencies: Python 2.7 (3)
 
Usage: find_files_by_size.py <source directory> <size in bytes> [options]

The options are:
[-e semi-colon separated list of file extensions] - use * to match ANY file
[-h help]
[-w show Warnings only]
[-y say Yes to all prompts (no interaction)]

Example: find_files_by_size.py c:\\ 4096 -e dll;exe;pdb
"""
###############################################################

from optparse import OptionParser
import getopt
import sys
import re
import os
import shutil
import datetime
import time
from os.path import exists, join

#pathsep ; on windows  , on unix
from os import pathsep

#from string import split

###############################################################
# Define some defaults:
sourceDirPath = '' #location to search for files
sizeInBytes = 0

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_VERBOSE = range(3)
logVerbosity = LOG_VERBOSE

extensions = '*' 	#'dll;exe;pdb;xml'
extensions_list = set()

###############################################################
#ask_ok() - prompts the user to continue
def ask_ok(prompt, retries=3, complaint='Yes or no, please!'):
	global yesAllPrompts
	if yesAllPrompts:
		print (prompt + " (Y)")
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
		print (complaint)

###############################################################
#usage() - prints out the usage text, from the top of this file :-)
def usage():
	print (__doc__)

dateTimeFormat = '%d %m %Y %H:%M'
datetime.datetime.strptime('01 12 2006 12:32', dateTimeFormat)
	
###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog <source directory> <size in bytes> [options]')
parser.add_option('-e', '--extensions', dest='extensions', default='dll;exe;pdb;xml',
				   help='only files that match these extensions will be processed (default: dll;exe;pdb;xml)')
parser.add_option('-w', '--warnings', dest='warnings', action='store_const',
				   const=LOG_WARNINGS, default=LOG_VERBOSE,
				   help='show only warnings (default: show all output)')
parser.add_option('-y', '--yes', dest='yes_all', action='store_const',
				   const=True, default=False,
				   help='automatically say Yes to allow prompts (default: prompt user)')

(options, args) = parser.parse_args()
if(len(args) != 2):
	usage()
	sys.exit(2)
logVerbosity = options.warnings
extensions = options.extensions
sourceDirPath = args[0]
sizeInBytes = int(args[1])
yesAllPrompts = options.yes_all

###############################################################
#copy the args to our variables
extensions_list = extensions.split(';')

###############################################################
#print out summary of the configuration, and prompt user to continue:
print ("Configuration:")
print ("--------------")

print ("sourceDirPath: " + sourceDirPath + "\n")
print ("sizeInBytes: " + str(sizeInBytes) + "\n")
print ("extensions: ")
for ext in extensions_list:
	print (ext + " ")

print ("")

if logVerbosity == LOG_WARNINGS:
	print ("Output will show warnings only\n")
elif logVerbosity == LOG_VERBOSE:
	print ("Output is verbose\n")
else:
	print ("Invalid verbosity level: " + logVerbosity)
	sys.exit(1)

print ("We will recursively search for all matching files, that have a filesize exactly equal to " + str(sizeInBytes) + " bytes.")

print ("")

if ask_ok("Do you wish to continue ? (Y/N)"):
	#do nothing
	print ("ok")
else:
	print ("Exiting")
	sys.exit()
	
print ("")

print ("Searching for files ...\n")

numWarnings = 0

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
#IsFileExtensionOk() - does this filename match the list of extensions given by user
def IsFileExtensionOk(filename):
	global extensions_list
	for ext in extensions_list:
		if(ext == '*'):
			return True
		if (filename.endswith("." + ext)):
			return True
	return False
	
###############################################################
#IsFileSizeOk() - does this file have the same size given by user
def IsFileSizeOk(filePath):
	global sizeInBytes
	fileSizeInBytes = os.path.getsize(filePath)
	if (sizeInBytes == fileSizeInBytes):
		return True
	else:
		return False

###############################################################
#search_files - recursively search the given directory, and populate the map with files that match our list of extensions
def search_files_by_size_and_ext(dir):
	iNumFilesFoundLocal = 0
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
			if IsFileExtensionOk(filename) and IsFileSizeOk(filePath):
				printOut ("File found: " + filePath)
				iNumFilesFoundLocal = iNumFilesFoundLocal + 1
		else:
			subdirlist.append(filePath)
	for subdir in subdirlist:
		try:
			iNumFilesFoundLocal += search_files_by_size_and_ext(subdir)
		except WindowsError:
			printOut("Error occurred accessing directory " + subdir);
	return iNumFilesFoundLocal

###############################################################
#search for source files, that match the extensions given by user
printOut ("Matching files:" + "\n" + "-----------------")
iNumFilesFound = 0
iNumFilesFound = search_files_by_size_and_ext(sourceDirPath)

###############################################################
#print summary of results		
print ("")
print ("Found " + str(iNumFilesFound) + " matching files.")
print (str(numWarnings) + " warnings")
