"""
 find_and_insert.py
 Author: Sean Ryan
 Version: 1.0

 Custom script to find some special header + footer text, and insert matching SQL 'print'  statements.

Fnd line like this, and add a matching printing line after it:
/*============= BEGIN ORIGINAL SQL FILE NAME: blah =============*/
print 'blah'

find line like this, and add a matching printing line BEFORE it:
print 'blah'
/*============= END ORIGINAL SQL FILE NAME: blah =============*/

Usage: find_and_insert.py <target directory> [options]

The options are:
[-e semi-colon separated list of file extensions]
[-h help]
[-w show Warnings only]
[-y say Yes to all prompts (no interaction)]

Example: find_and_insert.py test_data  -e cpp;sql
"""
###############################################################

#TODO xxx - must check for embedded quotes in blah !

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

from string import split

###############################################################
# Define some defaults:
targetDirPath = '' #location to search for files to alter

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_VERBOSE = range(3)
logVerbosity = LOG_VERBOSE

extensions = 'sql'
extensions_list = set()

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
parser = OptionParser(usage='%prog <target directory> <template header file> <template footer file> [options]')
parser.add_option('-e', '--extensions', dest='extensions', default='sql;sql',
                   help='only files that match these extensions will be processed (default: sql;sql)')
parser.add_option('-w', '--warnings', dest='warnings', action='store_const',
                   const=LOG_WARNINGS, default=LOG_VERBOSE,
                   help='show only warnings (default: show all output)')
parser.add_option('-y', '--yes', dest='yes_all', action='store_const',
                   const=True, default=False,
                   help='automatically say Yes to allow prompts (default: prompt user)')

(options, args) = parser.parse_args()
if(len(args) != 1):
    usage()
    sys.exit(2)
logVerbosity = options.warnings
extensions = options.extensions
targetDirPath = args[0]
yesAllPrompts = options.yes_all

###############################################################
#copy the args to our variables
extensions_list = extensions.split(';')

###############################################################
#print out summary of the configuration, and prompt user to continue:
print "Configuration:"
print "--------------"

print "targetDirPath: " + targetDirPath + "\n"
print "extensions: "
for ext in extensions_list:
    print ext + " "

print ""

if logVerbosity == LOG_WARNINGS:
    print "Output will show warnings only\n"
elif logVerbosity == LOG_VERBOSE:
    print "Output is verbose\n"
else:
    print "Invalid verbosity level: " + logVerbosity
    sys.exit(1)

print "We will add a header using the template file, to ALL matching existing files at the location " + targetDirPath

print ""

if ask_ok("Do you wish to continue ? (Y/N)"):
    #do nothing
    print "ok"
else:
    print "Exiting"
    sys.exit()
    
print ""

print "Modifying files ...\n"

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
        if (filename.lower().endswith("." + ext.lower())):
            return True
    return False

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
        else:
            subdirlist.append(os.path.join(basedir, filename))
    for subdir in subdirlist:
        search_files(subdir, result_dict)

###############################################################
#search for target files to alter:
printOut ("target files:" + "\n" + "-----------------")
targetFilePaths = dict()
search_files(targetDirPath, targetFilePaths)

numTargetFiles = len(targetFilePaths)

printOut ("")

printOut ("Found " + str(numTargetFiles) + " target files.")

printOut ("")

###############################################################
# make sorted list of filenames,
# just so the user can see the progress:
sortedFileNames = list()
for fileName in targetFilePaths.iterkeys():
    sortedFileNames.append(fileName)
sortedFileNames.sort()

###############################################################
#find a line like this:
#/*============= BEGIN ORIGINAL SQL FILE NAME: blah =============*/
footerLine = "/*============= END ORIGINAL SQL FILE NAME:"
headerLine = "/*============= BEGIN ORIGINAL SQL FILE NAME:"

endOfLine = "=============*/"

def isLineX(line, linePortion):
	return (linePortion in line)

def isLineFooter(line):
	global footerLine
	return isLineX(line, footerLine)

def isLineHeader(line):
	global headerLine
	return isLineX(line, headerLine)

###############################################################
#parse the line, to get the 'message' in the middle
def parseMessageFromLine(line, linePortion):
	parsedLine = line
	parsedLine = parsedLine.replace(linePortion,"")
	parsedLine = parsedLine.replace(endOfLine,"")
	return parsedLine
	
def parseMessageFromHeader(line):
	return parseMessageFromLine(line, headerLine)
	
def parseMessageFromFooter(line):
	return parseMessageFromLine(line, footerLine)
	
###############################################################
def createPrintLine(bIsHeader, message):
	message = message.replace('\n','')
	if (bIsHeader):
		message = "Start of original SQL file: " + message
	else:
		message = "End of original SQL file: " + message
	line = "print ' "+ message +"' "
	line = line + "\n"
	return line

###############################################################
#process a file, adding a header + footer 'print':
def processFile(srcFilePath):
	#backup the file to .orig:
	backupFilePath = srcFilePath + ".orig"
	if exists(backupFilePath):
		raise Exception("!!! Error: Original file already exists! - " + backupFilePath)
	shutil.copy(srcFilePath, backupFilePath)
	
	#read .orig, searching for the header:
	origFile = open(backupFilePath, "r")
	targetFile = open(srcFilePath, "w")
	bFoundHeader = False
	bFoundFooter = False
	for line in origFile:
		if isLineHeader(line):
			if bFoundHeader:
				raise Exception("Already found header! - " + line)
				bFoundHeader = True
			headerMessage = parseMessageFromHeader(line)
			targetFile.write(line)
			#also write the print:
			targetFile.write(createPrintLine(True, headerMessage))
		elif isLineFooter(line):
			if bFoundFooter:
				raise Exception("Already found footer! - " + line)
				bFoundFooter = True
			footerMessage = parseMessageFromFooter(line)
			#write the print:
			targetFile.write(createPrintLine(False, footerMessage))
			targetFile.write(line)
		else:
			targetFile.write(line)
	origFile.close()
	targetFile.close()

###############################################################
# Loop through the files - for each one, add a header using the template
        
numFilesProcessed = 0
for fileName in sortedFileNames:
	srcFilePathSet = targetFilePaths[fileName]
	for srcFilePath in srcFilePathSet:
		printOut ("\nProcessing file " + srcFilePath)
		processFile(srcFilePath)
		numFilesProcessed = numFilesProcessed + 1
	printOut ( "\r" + str((numFilesProcessed * 100) / numTargetFiles) + "%", LOG_WARNINGS, False ) #show some progress, even if low verbosity

###############################################################
#print summary of results        
print ""
print str(numFilesProcessed) + " files were processed"
print str(numWarnings) + " warnings"

print "Press ENTER to finish"
inp = sys.stdin.readline()
