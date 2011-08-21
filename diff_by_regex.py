"""
diff_by_regex.py

Script to perform a basic line-by-line diff between two files,
where the first file can contain regular expressions to match the second file.

Usage:
diff_by_regex.py <file with regular expressions> <file to compare> [options]

The options are:
[-h help]
"""

from optparse import OptionParser

import re
import sys
import time

###############################################################
# Define some defaults:

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_ERRORS, LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_INFO, LOG_VERBOSE, LOG_DEBUG = range(6)
logVerbosity = LOG_VERBOSE

#debug:
#logVerbosity = LOG_DEBUG

filePathWithRegex = ""
filePathToCompare = ""

startTime = time.time()

###############################################################
#usage() - prints out the usage text, from the top of this file :-)
def usage():
	print __doc__

###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog <file with regular expressions> <file to compare> [options]')

(options, args) = parser.parse_args()
if(len(args) != 2):
	usage()
	sys.exit(2)
#logVerbosity = options.warnings
filePathWithRegex = args[0]
filePathToCompare = args[1]

###############################################################
#are_lines_equal
def are_lines_equal(lineWithRegex, lineToCompare):
	mat = re.search(lineWithRegex, lineToCompare)
	if(mat):
		return mat.group(0)
	else:
		return False

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
		txt = str(txt) + "\n"
	if verb == LOG_WARNINGS_ONLY:
		if logVerbosity <= LOG_WARNINGS:
			sys.stdout.write(txt)
	elif(logVerbosity >= verb):
		sys.stdout.write(txt)

###############################################################
#compare_files
def compare_files(fileWithRegex, fileToCompare):
	diff_lines = list()
	lineNum = 1
	#basic compare, line-by-line:
	
	itRegex = iter(fileWithRegex)
	itCompare = iter(fileToCompare)
	while True:
		printOut("line: " + str(lineNum), LOG_DEBUG)
		try:
			valueRegex = itRegex.next() # in Python 2.x
			#value = next(itRegex) # in Python 3.x
			valueCompare = itCompare.next()
		except StopIteration:
			break
		if(not are_lines_equal(valueRegex, valueCompare)):
			diff_lines.append( (valueRegex, valueCompare, lineNum) );
		lineNum = lineNum + 1
	
	return diff_lines

###############################################################
#main process:

fileWithRegex = open(filePathWithRegex, 'r')
fileToCompare = open(filePathToCompare, 'r')

diff_lines = compare_files(fileWithRegex, fileToCompare)

for lineDetails in diff_lines:
	(valueRegex, valueCompare, lineNum) = lineDetails
	print("[" + str(lineNum) + "] - " + valueRegex)
	print("[" + str(lineNum) + "] + " + valueCompare)

#exit with non-zero, if differences were found:
exit(len(diff_lines))