"""
 checkFilepathIsWriteable.py
 Author: Sean Ryan
 Version: 1.0
 
Script to check can we write to the given file path.
If the directories do not exist, then this script tries to create them.
If there is an existing file at the path, we check can the file be written to.

The main use for this script, is where the build script cannot create the ISO file, because:
- the network path is inaccessible
- the existing ISO file is being accessed, and so cannot be over-written

This script is designed to provide better error messages to diagnose problems writing to the ISO file,
and also to fail the build more quickly, which all saves us some time :-)

Dependencies:
Python 2.5 or 2.7 or 3

Usage: checkFilepathIsWriteable.py [OPTIONS] <path to file you will be writing>

OPTIONS:
-w = show warnings only
-h = help
"""

import getopt
import os
import sys

###### SECTION FOR VARIABLES !!! #####
##

path_to_file = ""

#########################################

###### SECTION FOR CONSTANTS #####
##

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_VERBOSE = range(3)
logVerbosity = LOG_VERBOSE

ERROR_PREFIX_FOR_BUILD_FILTER = "error - " #in format which will be picked up by the BuildOutputFilter

###############################################################
#usage() - prints out the usage text, from the top of this file :-)
def usage():
	print(__doc__)

###############################################################
#main() - main program entry point
def main(argv):
	global path_to_file
	global logVerbosity
	try:
		opts, args = getopt.getopt(argv, "hw", ["help", "warnings"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	if(len(args) != 1):
		usage()
		sys.exit(2)	
	#get the args:
	path_to_file = args[0]
	#parse the options:
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-w", "--warnings"):
			logVerbosity = LOG_WARNINGS
	
if __name__ == "__main__":
	main(sys.argv[1:])

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
#test can we create the directory path, if it does not already exist:
try:
	#get the directory path:
	target_dir = os.path.dirname(path_to_file)

	#create the directory if it does not exist:
	if not os.path.exists(target_dir):
		os.mkdir(target_dir)
except:
	printOut (ERROR_PREFIX_FOR_BUILD_FILTER + "cannot access or create directory path '" + target_dir+ "' - is the directory path invalid or inaccessible ?", LOG_WARNINGS)
	printOut (str(sys.exc_info()[0]))
	sys.exit(3)	

###############################################################
#test can we write to the given file path:
try:
	if not os.path.exists(path_to_file):
		#no existing file, so try to create a temp file:
		tempFile = open(path_to_file, 'w')
		tempFile.close()
		os.remove(path_to_file)
	else:
		#existing file:
		#try to get a write lock on the filepath:
		file = open(path_to_file, 'r+')
except:
	printOut (ERROR_PREFIX_FOR_BUILD_FILTER + "cannot write to file '" + path_to_file+ "' - is it locked by some other process?" , LOG_WARNINGS)
	printOut (str(sys.exc_info()[0]))
	sys.exit(4)

###############################################################
#done!
printOut("Can write to ISO file " + path_to_file +" [ok]", LOG_WARNINGS)
