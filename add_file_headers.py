"""
 add_file_headers.py
 Author: Sean Ryan
 Version: 1.0

 Script to add a simple file header to all the given files.
 
 The file header is specified from a template file, in the style of Apache Velocity, where a variable looks like ${this}.

Usage: add_file_headers.py <target directory> <template file> [options]

The options are:
[-e semi-colon separated list of file extensions]
[-h help]
[-w show Warnings only]
[-y say Yes to all prompts (no interaction)]

Example: add_file_headers.py e:\\sean\\SourceRoot\\root\\20100920\\BWAC\\ sql_header.txt -e dll;sql
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
parser = OptionParser(usage='%prog <target directory> <template file> [options]')
parser.add_option('-e', '--extensions', dest='extensions', default='sql;sql',
                   help='only files that match these extensions will be processed (default: sql;sql)')
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
targetDirPath = args[0]
templateFilePath = args[1]
yesAllPrompts = options.yes_all

###############################################################
#copy the args to our variables
extensions_list = extensions.split(';')

###############################################################
#print out summary of the configuration, and prompt user to continue:
print "Configuration:"
print "--------------"

print "templateFilePath: " + templateFilePath + "\n"
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
        if (filename.endswith("." + ext)):
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
for fileName in sortedFileNames.iterkeys():
    sortedFileNames.append(fileName)
sortedFileNames.sort()

###############################################################
#get a shorter version of the file path, just to show what are immediate parents
def getShortenedFilePath(srcFilePath):
	pathParts = srcFilePath.split( os.sep )
	shortenedPath = ""
	iStart = len(pathParts) - 3
	if iStart < 0:
		iStart = 0
	while(iStart < len(pathParts)):
		shortenedPath = os.sep + pathParts[iStart]
	shortenedPath

###############################################################
#get the template variables in style of Apache Velocity, like ${this}
def getHeader(srcFilePath, templateFilePath):
	dictVarToVal = dict()
	dictVarToVal["FilePath"] = getShortenedFilePath(srcFilePath)
	dictVarToVal

###############################################################
#replace any template variables in the given line
def replaceTemplateVariables(line, dictVarToVal)
	for var in dictVarToVal.iterkeys():
		line = line.replace(var, dictVarToVal[var])
	line

###############################################################
#generate the header for given file path, from the given template.
def getHeader(srcFilePath, templateFilePath):
	dictVarToVal = getVariables(srcFilePath, templateFilePath)
	header = ""
	srcFile = open(templateFilePath, "r")
	for line in srcFile:
		line = replaceTemplateVariables(line, dictVarToVal)
		header = header + line + "\n"
	header

###############################################################
#process a file, adding a header:
def processFile(srcFilePath, templateFilePath)
	#backup the file to .orig:
	backupFilePath = srcFilePath + ".orig"
	if exists(backupFilePath):
		raise Exception("!!! Error: Original file already exists! - " + backupFilePath)
	shutil.copy(srcFilePath, backupFilePath)
	#read the header:
	header = getHeader(srcFilePath, templateFilePath)
	#write the header to the file:
	targetFile = open(srcFilePath, "w+")
	for line in header:
		targetFile.write(line)
	#read .orig, and write to the file:
	origFile = open(backupFilePath, "r")
	for line in origFile:
		targetFile.write(line)
	targetFile.close()
###############################################################
# Loop through the files - for each one, add a header using the template
        
numFilesProcessed = 0
for fileName in sortedFileNames:
        srcFilePathSet = sortedFileNames[fileName]
            for srcFilePath in srcFilePathSet:
                printOut ("\nProcessing file " + srcFilePath)
                processFile(srcFilePath, templateFilePath)
                numFilesProcessed = numFilesProcessed + 1
        printOut ( "\r" + str((numFilesProcessed * 100) / numTargetFiles) + "%", LOG_WARNINGS, False ) #show some progress, even if low verbosity

###############################################################
#print summary of results        
print ""
print str(numFilesProcessed) + " files were processed"
print str(numWarnings) + " warnings"

print "Press ENTER to finish"
inp = sys.stdin.readline()
