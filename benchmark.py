"""
Script for creating a benchmarking log file,
by simply outputting the time elapsed since the last execution.

The output can be dumped to a logfile, to build up a record of benchmarks.

usage:

benchmark.py <benchmark identifier> [options]


The options are:
[-f Finish this benchmark]
[-h help]
[-w show Warnings only]

Example: 
benchmark.py buildTask1
benchmark.py buildSubTask1
benchmark.py buildSubTask1 -f
benchmark.py buildSubTask2
benchmark.py buildSubTask2 -f
benchmark.py buildTask1 -f

Dependencies:
- Windows XP or later
- Python 2.7 or 3.x
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

dictBenchmarks = dict()

startTime = time.time()

benchmarkId = ""
bIsFinish= False

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
parser = OptionParser(usage='%prog <benchmark identifier> [options]')
parser.add_option('-f', '--finish', dest='is_finish', action='store_const',
	 	 	 	const=True, default=False,
				help='Specifies that this is the FINISH of the particular benchmark'
parser.add_option('-w', '--warnings', dest='warnings', action='store_const',
	 	 	 	const=LOG_WARNINGS, default=LOG_VERBOSE,
	 	 	 	help='show only warnings (default: show all output)')

(options, args) = parser.parse_args()
if(len(args) != 1):
	usage()
	sys.exit(2)
logVerbosity = options.warnings
benchmarkId = args[0]
yesAllPrompts = options.yes_all
bIsFinish = options.is_finish

###############################################################

#returns:  now + minutesToWait, in format 'HHMM'
def getExecutionTime(minutesToWait):
	timeToRunMinutes = time.time() + (60 * minutesToWait)
	timeToRun = time.localtime( timeToRunMinutes )
	dateTimeFormat = '%H:%M'
	timeHHMM = (time.strftime(dateTimeFormat, timeToRun))
	return timeHHMM

###############################################################
#main

readBenchmarks()
updateBenchmark(benchmarkId, startTime, bIsFinish)
writeBenchmarks()
