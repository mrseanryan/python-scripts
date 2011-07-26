"""
 operate_on_each_file.py
 Author: Sean Ryan
 Version: 1.0

Script to perform an operation on each file in a directory.

The operation is another script, that inputs and outputs to the same file paths each time.
 
Usage: operate_on_each_file.py [options]

The options are:
[-e semi-colon separated list of file Extensions]
[-s Source directory]
[-t target script to run]
[-i input file path for target]
[-f output file from target]
[-o output directory]
[-w show Warnings only]
[-y Yes to all prompts]

Example: 
operate_on_each_file.py -s "E:\Shared\PRNs\CWA__changes_2011\issues\Angus_CWA_Issues\44036__T_file_parse_fail\T_files\daily_T_files\DOWNLOAD" -t "C:\Decomp\DECOMPRESSMPE.bat"   -i "c:\Decomp\COMPMPE.blk"   -f "c:\Decomp\UNCOMP.TXT"  -e *;  -o "E:\Shared\PRNs\CWA__changes_2011\issues\Angus_CWA_Issues\44036__T_file_parse_fail\T_files\daily_T_files\Decompressed"

"""
###############################################################

import getopt
import os
from os.path import exists, join
import re
import shutil
import subprocess
import sys


#pathsep ; on windows  , on unix
from os import pathsep

from string import split

###############################################################
# Define some constants:
sourceDirPath = '' #location to copy files FROM
targetScriptPath = '' #the location of the script to run for each file
inputFilePath = '' #the path to the file that is INPUT by the target script
outputFilePath = '' #the path to the file that is output by the target script
outputDirPath = '' #the path to where we will put the output files

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_VERBOSE = range(3)
logVerbosity = LOG_VERBOSE

yesToAllPrompts = False

extensions = 'dll;exe;pdb;xml'
extensions_list = set()

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
#ask_ok() - prompts the user to continue
def ask_ok(prompt, retries=3, complaint='Yes or no, please!'):
    if yesToAllPrompts:
        printOut (prompt + " - (yes to all prompts)")
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
#main() - main program entry point
def main(argv):
    global extensions
    global logVerbosity
    global sourceDirPath
    global targetScriptPath
    global inputFilePath
    global outputFilePath
    global outputDirPath
    global yesToAllPrompts
    try:
        opts, args = getopt.getopt(argv, "he:i:f:s:t:o:wy", ["help", "extensions=", "input=", "file=", "source=", "target=", "output=", "warnings", "yes"])
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
        elif opt in ("-e", "--extensions"):
            extensions = arg
        elif opt in ("-i", "--input"):
            inputFilePath = arg
        elif opt in ("-f", "--file"):
            outputFilePath = arg
        elif opt in ("-s", "--source"):
            sourceDirPath = arg
        elif opt in ("-t", "--target"):
            targetScriptPath = arg
        elif opt in ("-o", "--output"):
            #import pdb
            #pdb.set_trace()
            outputDirPath = arg
        elif opt in ("-w", "--warnings"):
            logVerbosity = LOG_WARNINGS
        elif opt in ("-y", "--yes"):
            yesToAllPrompts = True

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
print "targetScriptPath: " + targetScriptPath + "\n"
print  "inputFilePath: " + inputFilePath + "\n"
print  "outputFilePath: " + outputFilePath + "\n"
print  "outputDirPath: " + outputDirPath + "\n"


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
	

print ""

if ask_ok("Do you wish to continue ? (Y/N)"):
    #do nothing
    print "ok"
else:
    print "Exiting"
    sys.exit()
    
print ""

print "Processing files ...\n"

numWarnings = 0

###############################################################

# Source Files paths will be cached in this var:
# map from filename -> filepath
sourceFilePaths = dict()

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

numSourceFiles = len(sourceFilePaths)

printOut ("Found " + str(numSourceFiles) + " source files.")

printOut ("")

###############################################################
# make sorted list of source filenames,
# just so the user can see the progress:
sortedSourceFileNames = list()
for fileName in sourceFilePaths.iterkeys():
    sortedSourceFileNames.append(fileName)
sortedSourceFileNames.sort()

################################################################
# functions

def copyFile(srcFilePath, scriptInputFilePath):
	printOut("Copying file from " + srcFilePath + " to " + scriptInputFilePath)
	shutil.copy(srcFilePath, scriptInputFilePath)

def runOperation(targetScriptPath):
	targetScriptPath = os.path.abspath(targetScriptPath)
	scriptWorkingDir = os.path.dirname(targetScriptPath)
	args = ""
	toExec = targetScriptPath + " " + args
	printOut("Running script " + toExec)
	process = subprocess.Popen(toExec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd = scriptWorkingDir)
	(stdout_cap, stderr_cap) = process.communicate()
	printOut(">>>" + str(stdout_cap))
	if(len(stderr_cap) > 0):
		raise Exception(str(stderr_cap))
	#TODO - catch error return code !

def createOutputFilePath(fileName, outputDirPath):
	return outputDirPath + "\\" + "processed__" + fileName


###############################################################
# Loop through all results stored earlier, for each one then
# run the target script
# we then copy the output file to the output dir

numFilesProcessed = 0
for fileName in sortedSourceFileNames:
	srcFilePathSet = sourceFilePaths[fileName]
	
	for srcFilePath in srcFilePathSet:
		printOut("Processing file " + os.path.basename(srcFilePath))
		copyFile(srcFilePath, inputFilePath)
		runOperation(targetScriptPath)
		uniqueOutputFilePath = createOutputFilePath(fileName, outputDirPath)
		copyFile(outputFilePath, uniqueOutputFilePath)
		numFilesProcessed = numFilesProcessed + 1
		printOut ( "\r" + str((numFilesProcessed * 100) / numSourceFiles) + "%", LOG_WARNINGS, False ) #show some progress, even if low verbosity

###############################################################
#print summary of results		
print ""
print str(numFilesProcessed) + " files were processed"
print str(numWarnings) + " warnings"
