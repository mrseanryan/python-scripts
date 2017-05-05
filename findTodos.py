"""
 findTodos.py
 Author: Sean Ryan
 Version: 1.0

 Script to recursively find sourcecode files, that contain TODO comments.
 This is useful if you are working on a large codebase, and need an overview of the TODOs.

Dependencies: Python 2.7 (3)
 
Usage: findTodos.py <source directory> <semi-colon separated list of extensions> [options]

The options are:
[-h help]
[-i ignore file extensions]
[-s skip directores]
[-w show Warnings only]

Example: search for .NET source code files, in the c:\\sourcecode directory and all child directories, that do not have a copyright notice:
findTodos.py c:\\sourcecode cs;vbs

Example: search ALL files, in the c:\\sourcecode directory and all child directories, that do not have a copyright notice:
findTodos.py c:\\sourcecode *

Example: search for .NET source code files, in the c:\\sourcecode directory and all child directories, that do not have a copyright notice.
Ignore files with extension designer.cs or Test.cs (case in-sensitive).
Skip directories named obj or debug.
findTodos.py c:\\sourcecode cs;vbs -idesigner.cs;Test.cs -sobj;debug
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

#from string import split

###############################################################
# Define some defaults:
sourceDirPath = '' #location to search for files
sizeInBytes = 0

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_VERBOSE = range(3)
logVerbosity = LOG_VERBOSE

extensions_list = set()
extensions_to_ignore_list = set()
directories_to_ignore_list = set()

###############################################################
#ask_ok() - prompts the user to continue
def ask_ok(prompt, retries=3, complaint='Yes or no, please!'):
    global yesAllPrompts
    if yesAllPrompts:
        print (prompt + " (Y)")
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
        print (complaint)

###############################################################
#usage() - prints out the usage text, from the top of this file :-)
def usage():
    print (__doc__)

dateTimeFormat = '%d %m %Y %H:%M'
datetime.datetime.strptime('01 12 2006 12:32', dateTimeFormat)
    
###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog <source directory> <size in bytes> [options]')
parser.add_option('-i', '--ignore', dest='ignoreExtensions', default="",
                   help='ignore file extensions')
parser.add_option('-s', '--skip', dest='skipDirectories', default="",
                   help='skip directories')
parser.add_option('-w', '--warnings', dest='warnings', action='store_const',
                   const=LOG_WARNINGS, default=LOG_VERBOSE,
                   help='show only warnings (default: show all output)')
parser.add_option('-y', '--yes', dest='yes_all', action='store_const',
                   const=True, default=False,
                   help='automatically say Yes to allow prompts (default: prompt user)')

(options, args) = parser.parse_args()
if(len(args) != 2):
    usage()
    sys.exit(2)
logVerbosity = options.warnings
sourceDirPath = args[0]
extensions = args[1]
extensions_to_ignore_list = options.ignoreExtensions.split(';')
directories_to_ignore_list = options.skipDirectories.split(';')
yesAllPrompts = options.yes_all

###############################################################
#copy the args to our variables
extensions_list = extensions.split(';')

###############################################################
#print out summary of the configuration, and prompt user to continue:
print ("Configuration:")
print ("--------------")

print ("sourceDirPath: " + sourceDirPath + "\n")
print ("extensions: ")
for ext in extensions_list:
    print (" " + ext)

print ("extensions to ignore: ")
for ext in extensions_to_ignore_list:
    print (" " + ext)

print ("directories to ignore: ")
for dir in directories_to_ignore_list:
    print (" " + dir)

print ("")

if logVerbosity == LOG_WARNINGS:
    print ("Output will show warnings only\n")
elif logVerbosity == LOG_VERBOSE:
    print ("Output is verbose\n")
else:
    print ("Invalid verbosity level: " + logVerbosity)
    sys.exit(1)

print ("We will recursively search for all matching files, that have TODO comments.")

print ("")

if ask_ok("Do you wish to continue ? (Y/N)"):
    #do nothing
    print ("ok")
else:
    print ("Exiting")
    sys.exit()
    
print ("")

print ("Searching for files ...\n")

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

###############################################################
#IsFileExtensionOk() - does this filename match the list of extensions given by user
def IsFileExtensionOk(filename):
    global extensions_list
    global extensions_to_ignore_list

    isExtensionOk = False
    for ext in extensions_list:
        ext = ext.lower()
        if(ext == '*'):
            isExtensionOk = True
            break
        if (filename.lower().endswith("." + ext)):
            isExtensionOk = True
            break

    if not isExtensionOk:
        return False

    for ext in extensions_to_ignore_list:
        ext = ext.lower()
        if (filename.lower().endswith("." + ext)):
            return False

    return isExtensionOk
    
###############################################################
#IsFileSizeOk() - does this file have the same size given by user
def IsFileSizeOk(filePath):
    global sizeInBytes
    fileSizeInBytes = os.path.getsize(filePath)
    if (sizeInBytes == fileSizeInBytes):
        return True
    else:
        return False

###############################################################
#GetTodoTokens - get list of TODO tokens to search for
def GetTodoTokens():
    todoTokens = []
    commentTokens = ("#", "//", "/*")
    for commentToken in commentTokens:
        todoTokens.append(commentToken + "TODO")
        todoTokens.append(commentToken + " TODO")
        todoTokens.append(commentToken + "\tTODO")
    return todoTokens

###############################################################
#CountTodosInFile - does the file at given path, contain some TODO comments
def CountTodosInFile(filename):
    file = open(filename, 'r')
    token  = "TODO"
    countOfTodosInFile = 0
    todoTokens = GetTodoTokens()
    lineNum = 0
    for line in file:
        lineNum = lineNum + 1
        #sys.stdout.write(line) #xxx
        for todoToken in todoTokens:
            #sys.stdout.write(todoToken) #xxx
            todoToken = todoToken.lower()
            line = line.lower()
            if todoToken in line:
                countOfTodosInFile = countOfTodosInFile + 1
                indexInLine = line.find(todoToken)
                todoText = line[indexInLine : ]
                WriteOutTodo(filename, lineNum, todoText)
    return countOfTodosInFile

def WriteOutTodo(filename, lineNum, todoText):
    line = filename + ", " + str(lineNum) + ", " + todoText
    printOut(line, LOG_WARNINGS)
 
def IsDirectoryOk(dirpath):
    global directories_to_ignore_list
    dirSeparator = '\\' #TODO add support for Unix
    dirname = dirpath.split(dirSeparator)
    dirname = dirname[len(dirname) - 1]
    if(dirname in directories_to_ignore_list):
            return False
    return True

###############################################################
#search_files - recursively search the given directory, and populate the map with files that match our list of extensions
def search_files_by_ext(dir):
    todosFoundLocal = 0
    basedir = dir
    subdirlist = []
    
    printOut("Searching dir: " + dir)

    filesInDir = []
    try:
        filesInDir = os.listdir(dir)
    except WindowsError:
        printOut("Error occurred accessing directory " + dir);
        return 0
    
    totolTodosFound = 0
    for filename in filesInDir:
        filePath = os.path.join(basedir,filename)
        if os.path.isfile(filePath):
            if IsFileExtensionOk(filename):
                countOfTodosInFile = CountTodosInFile(filePath)
                if countOfTodosInFile > 0:
                    todosFoundLocal = todosFoundLocal + countOfTodosInFile
                    printOut ("File found: " + filePath + " with " + str(countOfTodosInFile) + " TODOs", LOG_VERBOSE)
        else:
            subdirlist.append(filePath)
    for subdir in subdirlist:
        if IsDirectoryOk(subdir):
            try:
                todosFoundLocal += search_files_by_ext(subdir)
            except WindowsError:
                printOut("Error occurred accessing directory " + subdir);
    return todosFoundLocal

###############################################################
#search for source files, that match the extensions given by user
printOut ("Summary:" + "\n" + "-----------------")
totalTodosFound = 0
totalTodosFound = search_files_by_ext(sourceDirPath)

###############################################################
#print summary of results        
print ("")
print ("Found " + str(totalTodosFound) + " TODOs in comments.")
print (str(numWarnings) + " warnings")
