"""
Script to schedule given command to run, after X minutes.

note: the command must NOT have any arguments.

usage:

schedule_command.py <command to run> <minutes to wait before running> [options]


The options are:
[-h help]
[-w show Warnings only]
[-y say Yes to all prompts (no interaction)]

Example: schedule_command.py c:\myLovelyCommand.exe 5 -w -y

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
	print __doc__

###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog <command to run> <minutes to wait> [options]')
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
commandToRun = args[0]
minutesToWait = int(args[1])
yesAllPrompts = options.yes_all

###############################################################
#print out summary of the configuration, and prompt user to continue:
print "Configuration:"
print "--------------"

print "commandToRun: " + commandToRun + "\n"
print "minutesToWait: " + str(minutesToWait) + "\n"

print ""

if logVerbosity == LOG_WARNINGS:
	print "Output will show warnings only\n"
elif logVerbosity == LOG_VERBOSE:
	print "Output is verbose\n"
else:
	print "Invalid verbosity level: " + logVerbosity
	sys.exit(1)

print "We will schedule the command " + commandToRun + " to run in " + str(minutesToWait) + " minutes time."

print ""

if ask_ok("Do you wish to continue ? (Y/N)"):
	#do nothing
	print "ok"
else:
	print "Exiting"
	sys.exit()
	
print ""

###############################################################

def runExe(targetScriptPath, args):
	scriptWorkingDir = os.path.dirname(targetScriptPath)
	if(len(scriptWorkingDir) == 0):
		scriptWorkingDir = os.getenv('TEMP')
	toExec = targetScriptPath + " " + args
	printOut("Running exe " + toExec)
	process = subprocess.Popen(toExec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd = scriptWorkingDir)
	#TODO - optionally send some text<ENTER> to skip password protected archvies OR look at archvie first
	(stdout_cap, stderr_cap) = process.communicate()
	if(len(stderr_cap) > 0):
		raise Exception(str(stderr_cap))
		#TODO - try to process contents of archive anyway (can have a partially successful extraction)
	printOut(" >> " + str(stdout_cap));
	if(process.returncode != 0):
		raise Exception("Process returned error code:" + str(process.returncode))
		
###############################################################

#returns:  now + minutesToWait, in format 'HHMM'
def getExecutionTime(minutesToWait):
	timeToRunMinutes = time.time() + (60 * minutesToWait)
	timeToRun = time.localtime( timeToRunMinutes )
	dateTimeFormat = '%H:%M'
	timeHHMM = (time.strftime(dateTimeFormat, timeToRun))
	return timeHHMM

# Implementation note
#
#at 15:41 e:\Sean\SourceRoot\bitbucket\python-scripts\at_test_command.bat
#
#note - on Win XP, the at command cleans up after itself if the command ran successfully !
#
def runAt(commandToRun, timeHHMM):
	exe = "at "
	args = timeHHMM + " " + os.path.abspath(commandToRun)
	runExe(exe, args)

###############################################################
#main

timeHHMM = getExecutionTime(minutesToWait)

runAt(commandToRun, timeHHMM)

print 'Command ' + commandToRun + ' is scheduled to run in ' + str(minutesToWait) + ' minutes.'
print '[done]'
