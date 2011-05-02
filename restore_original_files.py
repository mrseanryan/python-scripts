"""
restore_original_files.py
Author: Sean Ryan
Version: 1.4

This script is to provide a way to undo a previous copy operation.

Script to scan a directory,
and move any files from *.original to *

Script will try to COM register any .dll files.

Usage: restore_original_files.py [-d use default settings] [-t targetDirectory]

The default for targetDirectory is 'C:\Program Files\CR2\BWAC'

"""

import getopt
import sys
import re
import os
import shutil
from os.path import exists, join

#pathsep ; on windows  , on unix
from os import pathsep

from string import split
from string import replace


# Define some constants:		
targetDirPath = 'C:\Program Files\CR2\BWAC' #location to copy files FROM and TO

def usage():
    print __doc__

#main()
def main(argv):
    global targetDirPath
    try:
        opts, args = getopt.getopt(argv, "dht:", ["defaults", "help", "target="])
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
        elif opt in ("-d", "--defaults"):
            #using defaults - do nothing
            print ""
        #elif opt == '-b':
        #    global _debug
        #    _debug = 1
        elif opt in ("-t", "--target"):
            print "setting targetDirPath = " + arg + "\n"
            targetDirPath = arg
    
if __name__ == "__main__":
    main(sys.argv[1:])

print "targetDirPath: " + targetDirPath + "\n"

# This method ensures that a directory exists, if it does
# not then it will be created.
def ensure_dir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)
		print "Making dir " + f

#ensure_dir(targetDirPath)

# Target Files paths will be cached in this var:
# map from filename -> set(filepath)
targetFilePaths = dict()

def search_files(dir, result_dict):
    basedir = dir
    #print "Files in ", dir, ": "
    subdirlist = []
    for item in os.listdir(dir):
        if os.path.isfile(os.path.join(basedir,item)):
			if (item.endswith(".original")):
				print "File found: ", item
				filePathSet = set()
				if(item in result_dict):
                                        filePathSet = result_dict[item]
                                else:
                                        result_dict[item] = filePathSet
				filePathSet.add(os.path.join(basedir, item))
        else:
            subdirlist.append(os.path.join(basedir, item))
    for subdir in subdirlist:
        search_files(subdir, result_dict)

search_files(targetDirPath, targetFilePaths)

numTargetFiles = len(targetFilePaths)

print ""

print "Found " + str(numTargetFiles) + " .original files."

print ""

# Loop through all results stored earlier, for each one then
# copy to equivalent target path, if there is one

numfilesCopied = 0
for fileName in targetFilePaths.iterkeys():
        if(fileName.endswith(".original")):
                print "Processing file: " + fileName
                filePathSet = targetFilePaths[fileName]
                for filePath in filePathSet:
			targetFilePath = replace(filePath, ".original", "")
			print "Moving file " + filePath + " -> " + targetFilePath	
			shutil.move(filePath, targetFilePath)
			if targetFilePath.endswith(".dll"):
				print "Attempting to register .dll file - just in case it is a COM dll"
				os.system("regsvr32 /s \"" + targetFilePath + "\"")
		numfilesCopied = numfilesCopied + 1
		print ""
	else:
		print "Warning: skipping a file that is not a .original file: " + fileName
		print ""
	
print "Copied files : " + str(numfilesCopied)
	
print "Press ENTER to finish"
inp = sys.stdin.readline()
