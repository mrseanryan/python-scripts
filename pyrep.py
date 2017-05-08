"""
PYREP = PYthon gREP

usage:

schedule_command.py <path to file to read in> <path to file listing start-of-lines to keep> [options]

The options are:
[-h help]
[-w show Warnings only]
[-y say Yes to all prompts (no interaction)]

Example: pyrep.py myTextFile.txt myListOfStartOfLinesToKeep.txt -w -y

Dependencies:
- Windows XP or later
- Python 2.7
"""

from optparse import OptionParser
import os
import subprocess
import sys
import time

###############################################################
# Define some defaults:

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_ERRORS, LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_INFO, LOG_VERBOSE = range(5)
logVerbosity = LOG_VERBOSE

searchDirPath = ""

archiveDirPath = ""

numArchivesToKeep = 0

startTime = time.time()

###############################################################
#ask_ok() - prompts the user to continue
def ask_ok(prompt, retries=3, complaint='Yes or no, please!'):
	global yesAllPrompts
	if yesAllPrompts:
		print(prompt + " (Y)")
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
		print(complaint)

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
		txt = txt + "\n"
	if verb == LOG_WARNINGS_ONLY:
		if logVerbosity <= LOG_WARNINGS:
			sys.stdout.write(txt)
	elif(logVerbosity >= verb):
		sys.stdout.write(txt)

###############################################################
#usage() - prints out the usage text, from the top of this file :-)
def usage():
	print (__doc__)

###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog <path to file to read in> <path to file listing start-of-lines to keep> [options]')
parser.add_option('-w', '--warnings', dest='warnings', action='store_const',
	 	 	 	const=LOG_WARNINGS, default=LOG_VERBOSE,
	 	 	 	help='show only warnings (default: show all output)')
parser.add_option('-y', '--yes', dest='yes_all', action='store_const',
	 	 	 	const=True, default=True,
	 	 	 	help='automatically say Yes to allow prompts (default: prompt user)')

(options, args) = parser.parse_args()
if(len(args) != 2):
	usage()
	sys.exit(2)
logVerbosity = options.warnings
path_to_in_file = args[0]
path_to_lines_to_keep = args[1]
yesAllPrompts = options.yes_all

###############################################################
#print out summary of the configuration, and prompt user to continue:
print ("Configuration:")
print ("--------------")

print ("path_to_in_file: " + path_to_in_file + "\n")
print ("path_to_lines_to_keep: " + path_to_lines_to_keep + "\n")

print ("")

if logVerbosity == LOG_WARNINGS:
	print "Output will show warnings only\n"
elif logVerbosity == LOG_VERBOSE:
	print "Output is verbose\n"
else:
	print "Invalid verbosity level: " + logVerbosity
	sys.exit(1)

print ""

if(ask_ok("Do you wish to continue ? (Y/N)")):
	#do nothing
	print "ok"
else:
	print "Exiting"
	sys.exit()

print ""

###############################################################
#functions

def process_lines(path_to_in_file, path_to_lines_to_keep):
    in_file = open(path_to_in_file, 'r')
    for line in in_file:
        line_lower = line.lower().strip()
        lines_to_keep_file = open(path_to_lines_to_keep, 'r')
        line_is_ok = False
        for keep_line in lines_to_keep_file:
            if line_lower.find(keep_line.strip().lower()) >= 0:
                line_is_ok = True
                break
        if line_is_ok:
            print _remove_end_line(line)

def _remove_end_line(line):
    return line.replace("\r\n", "").replace("\n", "")

###############################################################
#main

process_lines(path_to_in_file, path_to_lines_to_keep)

print ('[done]')
