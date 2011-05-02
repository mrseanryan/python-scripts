"""
 CopyBins_from_Build_to_Source.py
 Author: Sean Ryan
 Version: 1.2

 Script to copy files with matching extensions, from a directory containing VS solution, to a staging directory.
 ALL existing files in staging directory are wiped.
 If there are multiple source binaries with the same name, then:
 - we pick the newest binary
 If two or more binaries have the same date and time, then we check their sizes.
 - if the files are of equal size, we pick the first file
 - if the files are different sizes, then we have an error - cannot decide which binary to copy.
 
 Useful for copying binary files into a staging directory, so they can afterwards be copied to a VM.

Usage: CopyBins_from_Build_to_Source.py <source directory> <target directory> <datetime> [options]

The options are:
[-d datetime stamp - we only copy files that are newer than this datetime.  example: "01 12 2005 13:33"]
[-e semi-colon separated list of file extensions]
[-h help]
[-w show Warnings only]
[-y say Yes to all prompts (no interaction)]

Example: CopyBins_from_Build_to_Source.py e:\\sean\\SourceRoot\\root\\20100920\\BWAC\\ temp_build "31 12 2009 17:00" -e dll;exe;pdb
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
sourceDirPath = '' #location to copy files FROM
targetDirPath = '' #location to copy files TO
dateTimeStamp = '' #we only copy files, that are newer than this datetime stamp

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_VERBOSE = range(3)
logVerbosity = LOG_VERBOSE

extensions = 'dll;exe;pdb;xml'
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

dateTimeFormat = '%d %m %Y %H:%M'
datetime.datetime.strptime('01 12 2006 12:32', dateTimeFormat)
    
###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog <source directory> <target directory> <datetime> [options]')
parser.add_option('-e', '--extensions', dest='extensions', default='dll;exe;pdb;xml',
                   help='only files that match these extensions will be processed (default: dll;exe;pdb;xml)')
parser.add_option('-w', '--warnings', dest='warnings', action='store_const',
                   const=LOG_WARNINGS, default=LOG_VERBOSE,
                   help='show only warnings (default: show all output)')
parser.add_option('-y', '--yes', dest='yes_all', action='store_const',
                   const=True, default=False,
                   help='automatically say Yes to allow prompts (default: prompt user)')

(options, args) = parser.parse_args()
if(len(args) != 3):
    usage()
    sys.exit(2)
logVerbosity = options.warnings
extensions = options.extensions
sourceDirPath = args[0]
targetDirPath = args[1]
dateTimeStamp = datetime.datetime.strptime(args[2], dateTimeFormat)
yesAllPrompts = options.yes_all

###############################################################
#copy the args to our variables
extensions_list = extensions.split(';')

###############################################################
#print out summary of the configuration, and prompt user to continue:
print "Configuration:"
print "--------------"

print "sourceDirPath: " + sourceDirPath + "\n"
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

print "We will copy all matching files, that have a modified timestamp greater than " + str(dateTimeStamp)

print "We will delete ALL existing files at the location " + targetDirPath

print ""

if ask_ok("Do you wish to continue ? (Y/N)"):
    #do nothing
    print "ok"
else:
    print "Exiting"
    sys.exit()
    
print ""

print "Copying files ...\n"

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

# Source Files paths will be cached in this var:
# map from filename -> filepath
sourceFilePaths = dict()

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
#search for files in the staging dir, that will be deleted
printOut ("old staging files:" + "\n" + "-----------------")
oldTargetFilePaths = dict()
search_files(targetDirPath, oldTargetFilePaths)

numOldTargetFiles = len(oldTargetFilePaths)

printOut ("")

printOut (str(numOldTargetFiles) + " old target files will be deleted.", LOG_WARNINGS)

if ask_ok("Do you wish to delete these files ? (Y/N)"):
    #do nothing
    print "ok"
else:
    print "Exiting"
    sys.exit()

printOut ("Deleting files...")
for oldFilePathSet in oldTargetFilePaths.itervalues():
    for oldFilePath in oldFilePathSet:
        os.remove(oldFilePath)

printOut ("")

        
###############################################################
#search for source files, that match the extensions given by user
printOut ("Source files:" + "\n" + "-----------------")
search_files(sourceDirPath, sourceFilePaths)

numSourceFiles = len(sourceFilePaths)

printOut ("")

printOut ("Found " + str(numSourceFiles) + " source files.")

printOut ("")

###############################################################
# make sorted list of source filenames,
# just so the user can see the progress:
sortedSourceFileNames = list()
for fileName in sourceFilePaths.iterkeys():
    sortedSourceFileNames.append(fileName)
sortedSourceFileNames.sort()

###############################################################
# Function to get the datetime on which the given file was last modified.
def getFileModTime(filePath):
    tm = os.path.getmtime(filePath)
    return datetime.datetime.fromtimestamp(tm)

###############################################################
class NewerFile:
    """holds details about a file which is newer than the given datetime stamp"""
    def __init__(self, filePath):
        self.dateTimeStamp = getFileModTime(filePath)
        self.filePath = filePath
        self.fileSize = os.path.getsize(filePath)

###############################################################
# Loop through all results stored earlier, for each one then
# copy to the target directory
        
numfilesCopied = 0
numFilesProcessed = 0
for fileName in sortedSourceFileNames:
        srcFilePathSet = sourceFilePaths[fileName]
        if len(srcFilePathSet) > 0:
            newerSrcFiles_list = set()
            for srcFilePath in srcFilePathSet:
                #check the modified timestamp, is greater than our given timestamp:
                modTime = getFileModTime(srcFilePath)
                if(modTime >= dateTimeStamp):
                    #print str(modTime) + " > " + str(dateTimeStamp)
                    newFile = NewerFile(srcFilePath)
                    newerSrcFiles_list.add(newFile)
            srcFileToCopy = None
            if(len(newerSrcFiles_list) > 0):
                srcFileToCopy = newerSrcFiles_list.pop()
                if(len(newerSrcFiles_list) > 1): #if more than one file has same newest timestamp, then we check are sizes the same:
                    for newerFile in newerSrcFiles_list:
                        if newerFile.dateTimeStamp > srcFileToCopy.dateTimeStamp:
                            srcFileToCopy = newerFile
                        elif newerFile.dateTimeStamp == srcFileToCopy.dateTimeStamp:
                            if newerFile.fileSize != srcFileToCopy.fileSize:
                                raise Exception("!!! Error: more than one source file path has newest file, but sizes are different.  File name: " + fileName)        
            if srcFileToCopy != None:
                printOut ("\nCopying file " + srcFileToCopy.filePath)
                #copy file to the target directory:
                shutil.copy(srcFileToCopy.filePath, targetDirPath)
                numfilesCopied = numfilesCopied + 1
        numFilesProcessed = numFilesProcessed + 1
        printOut ( "\r" + str((numFilesProcessed * 100) / numSourceFiles) + "%", LOG_WARNINGS, False ) #show some progress, even if low verbosity

###############################################################
#print summary of results        
print ""
print str(numfilesCopied) + " files were copied"
print str(numWarnings) + " warnings"

print "Press ENTER to finish"
inp = sys.stdin.readline()
