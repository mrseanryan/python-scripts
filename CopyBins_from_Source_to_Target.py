"""
 CopyBins_from_Source_to_Target.py
 Author: Sean Ryan
 Version: 1.10

 Script to copy files with matching extensions, from a source directory, to target directory,
 where files with the same name should be replaced, even if they occur in
 different sub-directories from source.

 Useful for updating a BWAC VM from a set of manually built binaries.

 This script will list all the binary files in the source directory.
 For each file, it will try to find matching filename(s) in the target directory.
 If a match is found, then the target file(s) are replaced with the source file.
 The target file(s) are renamed to be .original (if there is no existing .original)

 For .pdb files, if a target .pdb file is not found, then the script will try to find the equivalent .dll or .exe file(s)

 You can undo the operation of this script, by running the script restore_original_files.py
 (assuming you do not use the -r option with this script).

Usage: CopyBins_from_Source_to_Target.py [options]

The options are:
[-d use default settings]
[-e semi-colon separated list of file Extensions]
[-r Replace without creating originals]
[-s Source directory]
[-t Target directory]
[-w show Warnings only]

Example: CopyBins_from_Source_to_Target.py -s "e:\\Sean\\SourceRoot\\root\\20100920\\BWAC\\BWAC\\bin\\Release with Debug Info" -t temp_build -e dll;exe;pdb

The default for -s Source directory is build
The default for -t Target directory is "C:\Program Files\CR2\BWAC"
The default for -e Extensions is dll;exe;pdb;xml

"""
###############################################################

import getopt
import sys
import re
import os
import shutil
from os.path import exists, join

#pathsep ; on windows  , on unix
from os import pathsep

from string import split

###############################################################
# Define some constants:
sourceDirPath = 'build' #location to copy files FROM
targetDirPath = 'C:\Program Files\CR2\BWAC' #location to copy files TO
bCreateOriginals = True

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_VERBOSE = range(3)
logVerbosity = LOG_VERBOSE

extensions = 'dll;exe;pdb;xml'
extensions_list = set()

###############################################################
#ask_ok() - prompts the user to continue
def ask_ok(prompt, retries=3, complaint='Yes or no, please!'):
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
#main() - main program entry point
def main(argv):
    global bCreateOriginals
    global extensions
    global logVerbosity
    global sourceDirPath
    global targetDirPath
    try:
        opts, args = getopt.getopt(argv, "hde:rs:t:w", ["help", "defaults", "extensions=", "replace", "source=", "target=", "warnings"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    if(len(opts) == 0):
        usage()
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        #elif opt == '-b':
        #    global _debug
        #    _debug = 1
        elif opt in ("-d", "--defaults"):
            #using defaults - do nothing
            print ""
        elif opt in ("-e", "--extensions"):
            extensions = arg
        elif opt in ("-r", "--replace"):
            bCreateOriginals = False
        elif opt in ("-s", "--source"):
            sourceDirPath = arg
        elif opt in ("-t", "--target"):
            print "setting targetDirPath = " + arg + "\n"
            targetDirPath = arg
        elif opt in ("-w", "--warnings"):
            logVerbosity = LOG_WARNINGS
    
if __name__ == "__main__":
    main(sys.argv[1:])

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
	
if bCreateOriginals:
    print "Target files will be backed up to .original file (if no existing .original)"
else:
    print "Target files will NOT be backed up to .original file"

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

# Target Files paths will be cached in this var:
# map from filename -> filepath
targetFilePaths = dict()

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
#search for source & target files, that match the extensions given by user
printOut ("Source files:" + "\n" + "-----------------")
search_files(sourceDirPath, sourceFilePaths)

printOut ("")

printOut ("Target files:" + "\n" + "-----------------")
search_files(targetDirPath, targetFilePaths)

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
# Loop through all results stored earlier, for each one then
# copy to equivalent target path(s), if there is one

numfilesCopied = 0
numFilesProcessed = 0
for fileName in sortedSourceFileNames:
        srcFilePathSet = sourceFilePaths[fileName]
        if (len(srcFilePathSet) > 1):
                raise Exception("!!! Error: more than one source file path for the file name: " + fileName)
        srcFilePath = srcFilePathSet.pop() #assuming only be one source file path, for each fileName
        printOut ("Processing file " + srcFilePath)
        bTargetFound = False
        targetFilePathSet = set()
	if (fileName in targetFilePaths):
            bTargetFound = True
            targetFilePathSet = targetFilePaths[fileName]
        else:
            if (fileName.endswith(".pdb")):
                fileNameExe = fileName.replace(".pdb", ".exe")
                fileNameDll = fileName.replace(".pdb", ".dll")
                if (fileNameExe in targetFilePaths):
                    bTargetFound = True
                    targetFilePathExes = targetFilePaths[fileNameExe]
                    targetFilePathSet = set()
                    for tgtFilePathExe in targetFilePathExes:
                        tgtFilePathPdb = tgtFilePathExe.replace(".exe", ".pdb")
                        targetFilePathSet.add(tgtFilePathPdb)
                if (fileNameDll in targetFilePaths):
                    if bTargetFound:
                        raise Exception("!!! Error: .pdb file target is ambiguous: is it " + fileNameExe + " or " + fileNameDll + " ?" )
                    bTargetFound = True
                    targetFilePathDlls = targetFilePaths[fileNameDll]
                    targetFilePathSet = set()
                    for tgtFilePathDll in targetFilePathDlls:
                        tgtFilePathPdb = tgtFilePathDll.replace(".dll", ".pdb")
                        targetFilePathSet.add(tgtFilePathPdb)
        if bTargetFound:
                tgtFilePaths = targetFilePathSet
                for tgtFilePath in tgtFilePaths:
                        if bCreateOriginals:
                            origFilePath = tgtFilePath + ".original"
                            if os.path.exists(tgtFilePath):
                                if not os.path.exists(origFilePath):
                                        printOut ("Backing up file " + tgtFilePath + " -> .original file")
                                        shutil.copy(tgtFilePath, origFilePath)
                            else:
                                if not tgtFilePath.endswith(".pdb"):
                                    raise Exception("!!! Error: the target file is not found.  Bug in this script ?  Cannot create a .original file for this file: " + tgtFilePath)
                        printOut ("Copying file " + srcFilePath + " -> " + tgtFilePath)
                        shutil.copy(srcFilePath, tgtFilePath)
                        if fileName.endswith(".dll"):
                                printOut ("Attempting to register .dll file - just in case it is a COM dll")
                                os.system("regsvr32 /s \"" + tgtFilePath + "\"")
                        printOut ("")
                numfilesCopied = numfilesCopied + 1
                printOut ("")
	else:
		printOut (("!!! Warning: the source file " + fileName + " has no equivalent target file"), True)
		printOut ("")
		numWarnings = numWarnings + 1
	numFilesProcessed = numFilesProcessed + 1
        printOut ( "\r" + str((numFilesProcessed * 100) / numSourceFiles) + "%", LOG_WARNINGS, False ) #show some progress, even if low verbosity

###############################################################
#print summary of results		
print ""
print str(numfilesCopied) + " files were copied"
print str(numWarnings) + " warnings"

print "Press ENTER to finish"
inp = sys.stdin.readline()
