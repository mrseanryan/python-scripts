"""
diff_by_regex.py

Script to perform a basic line-by-line diff between two files,
where the first file can contain regular expressions to match the second file.

Usage:
diff_by_regex.py <file with regular expressions> <file to compare> [options]

The options are:
[-h Help]
[-f First line is heading]
[-d Disable regex parsing]
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
parser.add_option('-f', '--first line is heading', dest='firstLineIsHeading', action='store_const',
                   const=True, default=False,
                   help='Always output the first line as a heading, if there are differences found. (default: off)')
parser.add_option('-d', '--Disable regex parsing', dest='disableRegex', action='store_const',
                   const=True, default=False,
                   help='Disable the regex parsing of the first file. (default: off)')

(options, args) = parser.parse_args()
if(len(args) != 2):
	usage()
	sys.exit(2)
#logVerbosity = options.warnings
filePathWithRegex = args[0]
filePathToCompare = args[1]

###############################################################
#are_lines_equal
def are_lines_equal(lineWithRegex, lineToCompare, bDisableRegex):
	if bDisableRegex:
		return are_lines_equal_no_regex(lineWithRegex, lineToCompare)
	else:
		return are_lines_equal_regex(lineWithRegex, lineToCompare)

def are_lines_equal_regex(lineWithRegex, lineToCompare):
	mat = re.search(lineWithRegex, lineToCompare)
	if(mat):
		return mat.group(0)
	else:
		return False

def are_lines_equal_no_regex(lineWithRegex, lineToCompare):
	return lineWithRegex == lineToCompare

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

def lineCount(fileObj):
	iLines = 0
	for line in fileObj:
		iLines = iLines + 1
	return iLines

###############################################################
#compare_files
def compare_files(fileWithRegex, fileToCompare):
	heading_line = ""
	diff_lines = list()
	lineNum = 1
	#basic compare, line-by-line:
	
	itRegex = iter(fileWithRegex)
	itCompare = iter(fileToCompare)
	bHaveLineInFirstFile = False
	while True:
		printOut("line: " + str(lineNum), LOG_DEBUG)
		try:
			bHaveLineInFirstFile = False
			valueRegex = itRegex.next() # in Python 2.x
			#value = next(itRegex) # in Python 3.x
			bHaveLineInFirstFile = True
			
			if(valueRegex[0] == '#'):
				continue #skip comment lines
			
			valueCompare = itCompare.next()
		except StopIteration:
			break
		if(len(heading_line)==0):
			heading_line = valueRegex
		if(not are_lines_equal(valueRegex, valueCompare, options.disableRegex)):
			diff_lines.append( (valueRegex, valueCompare, lineNum) );
		lineNum = lineNum + 1
	
	#check are there more lines (the file is same, but longer):
	fileToCompare_lines = lineCount(fileToCompare)
	fileWithRegex_lines = lineCount(fileWithRegex)
	
	if(fileToCompare_lines < fileWithRegex_lines):
		diff_lines.append( ("", "< second file is smaller >", lineNum) )
	if(fileToCompare_lines > fileWithRegex_lines):
		diff_lines.append( ("", "< second file is longer >", lineNum) )
	
	return (heading_line, diff_lines)

###############################################################
#main process:

fileWithRegex = open(filePathWithRegex, 'r')
fileToCompare = open(filePathToCompare, 'r')

(heading_line, diff_lines) = compare_files(fileWithRegex, fileToCompare)

for lineDetails in diff_lines:
	if(options.firstLineIsHeading):
		#import pdb
		#pdb.set_trace()
		heading_line = heading_line.replace('\n','')
		print(heading_line)
		options.firstLineIsHeading = False
	(valueRegex, valueCompare, lineNum) = lineDetails
	print("[" + str(lineNum) + "] - " + valueRegex)
	print("[" + str(lineNum) + "] + " + valueCompare)

#exit with non-zero, if differences were found:
exit(len(diff_lines))
