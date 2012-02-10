"""
DeploySQL.py

This script is used to deploy multiple SQL scripts against a database.

The database objects are first backed up, before executing the new scripts.

USAGE:		DeploySQL.py	<SQL Server>	<Database name>	<SQL user>	<SQL password>	<listfile of SQL scripts>		<output file of original database objects>	<path to directory containing NEW SQL scripts> <path to output file for new SQL script results> <path to sqlcmd.exe directory>	[OPTIONS]
"""

#Dependencies:
#
#Python 2.7.x



###############################################################
#TODO
#
# cleanup on fail: drop any SP_NEW stored procedures
# rename original SQL file, if it already exists (to a new unique name) 
#
###############################################################

import getopt
import re
import os
import shutil
import subprocess

from string import split

from deploySQL_common import *


###############################################################
# settings:

sqlServerInstance = ""
sqlDbName = ""
sqlUser = ""
sqlPassword = ""
sqlScriptListfilePath = ""
origOutputFilepath = ""
pathToNewSqlDir = ""
newOutputFilepath = ""

# rem unfortunately, need to use short file paths.  Hint:  to find the short file path, from cmd line, use:				 dir "path to my directory" /X
sqlCmd = "sqlcmd.exe"
#sqlCmdDirPath = "c:\Progra~1\MI6841~1\90\Tools\Binn\\"
sqlCmdDirPath = ""


###############################################################
#usage() - prints out the usage text, from the top of this file :-)
def usage():
    print __doc__

###############################################################
#main() - main program entry point
#args = <SQL Server>	<SQL user>	<SQL password>	<listfile of SQL scripts>		<output file of original database objects>
def main(argv):
	
	global sqlServerInstance, sqlDbName, sqlUser, sqlPassword, sqlScriptListfilePath, origOutputFilepath, pathToNewSqlDir, newOutputFilepath, sqlCmdDirPath

	try:
		opts, args = getopt.getopt(argv, "hw", ["help", "warnings"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	if(len(args) != 9):
		usage()
		sys.exit(3)
	#assign the args to variables:
	sqlServerInstance = args[0]
	sqlDbName = args[1]
	sqlUser = args[2]
	sqlPassword = args[3]
	sqlScriptListfilePath = args[4]
	origOutputFilepath = args[5]
	pathToNewSqlDir = args[6]
	newOutputFilepath = args[7]
	sqlCmdDirPath = args[8]
	
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-w", "--warnings"):
			setLogVerbosity(LOG_WARNINGS)

if __name__ == "__main__":
    main(sys.argv[1:])

###############################################################
#FUNCTIONS

def createSqlDumpScript(dbObjects, pathToSqlDumpScript):
	global sqlDbName
	if os.path.exists(pathToSqlDumpScript):
		os.remove(pathToSqlDumpScript)
	sqlDumpScriptFile = open(pathToSqlDumpScript, 'w+')
	sqlDumpScriptFile.write('use ' + sqlDbName + getEndline())
	sqlDumpScriptFile.write(getEndline())
	sqlDumpScriptFile.write("declare @currentObjectName varchar(200)" + getEndline())
	sqlDumpScriptFile.write("select @currentObjectName = 'unknown'" + getEndline())
	sqlDumpScriptFile.write(getEndline())
	
	for dbObject in dbObjects:
		#printOut("dbObjectType = " + dbObject.dbObjectType + " sqlScriptName = " + dbObject.sqlScriptName + " sqlObjectName = " + dbObject.sqlObjectName)
		if len(dbObject.sqlObjectName) > 0:
			printOut("backing up database object " + dbObject.sqlObjectName)
			sqlExec = "exec sp_helptext '"+dbObject.sqlObjectName+"'" + getEndline()
			sqlDumpScriptFile.write(getSqlExists(dbObject.dbObjectType, dbObject.sqlObjectName, sqlExec))
		else:
			if dbObject.dbObjectType != 'SP_NEW':
				addWarning("Cannot backup a SQL object for SQL script " + dbObject.sqlScriptName + " as the object name is not known")
	#add 'goto' for handling errors:
	sqlErrorGoto = "goto OK" + getEndline()
	sqlErrorGoto = sqlErrorGoto + "ERROR_CANNOT_BACKUP:" + getEndline()
	sqlErrorGoto = sqlErrorGoto + "RAISERROR (N'Cannot backup object %s, as it does not exist', 11 /*Severity*/, 1 /*State*/, @currentObjectName )" + getEndline()
	sqlErrorGoto = sqlErrorGoto + "OK:" + getEndline() #label to allow OK run to skip the error label
	sqlDumpScriptFile.write(sqlErrorGoto)
	sqlDumpScriptFile.write("GO" + getEndline())

def backupOriginalObjects(sqlScriptListfilePath, outputFilepath):
	global sqlServerInstance, sqlCmdPath
	dbObjects = readListfile(sqlScriptListfilePath)
	#create the SQL file which will dump out the required database objects:
	pathToSqlDumpScript = "temp.dumpSQLobjects.sql"
	createSqlDumpScript(dbObjects, pathToSqlDumpScript)
	#exec the dump script:
	execSqlScript(pathToSqlDumpScript, outputFilepath)
	return dbObjects

def execSqlScript(pathToSqlScript, outputFilepath):
	global sqlServerInstance, sqlUser, sqlPassword, sqlCmd, sqlCmdDirPath
	#sqlcmd.exe - ref:   http://msdn.microsoft.com/en-us/library/ms162773.aspx
	
	#sqlcmd -S (local) -U <user> -P <password>   -i dumpDatabaseObject.sql  -o originalSQL.sql
	pathToSqlScript = os.path.abspath(pathToSqlScript)
	outputFilepath = os.path.abspath(outputFilepath)
	args = "-S " + sqlServerInstance + " -U " + sqlUser + " -P " + sqlPassword + " -i " + pathToSqlScript + " -o " + outputFilepath + " -r 0 -b -m -1"    #-b is to exit on SQL error
	runExe(sqlCmd, sqlCmdDirPath, args)

def getEndline():
	return "\r\n" #OK for Windows

#get some SQL which checks if the given database object exists (if not, then we cannot back it up, and its a SQL error via a 'goto')
def getSqlExists(dbObjectType, sqlObjectName, sqlExec):
	if not dbObjectType == "SP":
		raise Exception("not implemented: check for existence of database object type " + dbObjectType)
	sqlExists = "IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'"+sqlObjectName+"') AND type in (N'P', N'PC'))" + getEndline()
	sqlExists = sqlExists + "BEGIN" + getEndline()
	sqlExists = sqlExists + sqlExec + getEndline()
	sqlExists = sqlExists + "END" + getEndline()
	#add Else as an error (since if it does not exist, then we cannot backup!)
	sqlExists = sqlExists + "ELSE" + getEndline()
	sqlExists = sqlExists + "BEGIN" + getEndline()
	sqlExists = sqlExists + "select @currentObjectName = '" + sqlObjectName + "'"+ getEndline()
	sqlExists = sqlExists + "goto ERROR_CANNOT_BACKUP" + getEndline()
	sqlExists = sqlExists + "END" + getEndline()
	return sqlExists

def getTempDir():
	return os.environ['TEMP'] + '\\'

def outputSummary(dbObjects):
	printOut( str(getNumWarnings()) + " warnings occurred" )
	printOut( str(len(dbObjects)) + " scripts were processed")
	#TODO - add more summary info

def runExe(targetScriptName, targetScriptDirPath, args):
	scriptWorkingDir = targetScriptDirPath #os.path.dirname(targetScriptPath)
	toExec = targetScriptDirPath + targetScriptName + " " + args
	printOut("Running exe " + toExec)
	printOut("working dir = " + scriptWorkingDir)
	process = subprocess.Popen(toExec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd = scriptWorkingDir)
	(stdout_cap, stderr_cap) = process.communicate()
	if(len(stderr_cap) > 0):
		raise Exception(str(stderr_cap))
	printOut(" >> " + str(stdout_cap));
	if(process.returncode != 0):
		raise Exception("Process returned error code:" + str(process.returncode))

def runNewSQLscripts(dbObjects, pathToNewSqlDir, outputFilepath):
	global sqlDbName, dictDbObjectTypeToSubDir
	for dbObject in dbObjects:
		#we need to specify the database name, so we copy the script, and prefix a 'use' clause
		sqlScriptCopy = getTempDir() + dbObject.sqlScriptName
		
		printOut("Executing SQL script " + dbObject.sqlScriptName)
		subDir = dictDbObjectTypeToSubDir[dbObject.dbObjectType]
		pathToSqlScript = pathToNewSqlDir + subDir + dbObject.sqlScriptName
		
		#add the 'use' clause:
		sqlOrigFile = open(pathToSqlScript, 'r')
		sqlCopyFile = open(sqlScriptCopy, 'w')
		
		sqlCopyFile.write('use ' + sqlDbName + getEndline())
		sqlCopyFile.write(getEndline())

		#now just append the rest of the original file:
		for origLine in sqlOrigFile:
			sqlCopyFile.write(origLine)
		
		sqlOrigFile.close()
		sqlCopyFile.close()
		#exec the copy of the original SQL script:
		execSqlScript(sqlScriptCopy, outputFilepath)

		
def validateArgs(sqlScriptListfilePath, origOutputFilepath):
	if not os.path.exists(sqlScriptListfilePath):
		raise Exception("The listfile of SQL scripts could not be found: " + sqlScriptListfilePath)
	if os.path.exists(origOutputFilepath):
		raise Exception("The output file of original objects, already exists: " + origOutputFilepath)


###############################################################
#main
validateArgs(sqlScriptListfilePath, origOutputFilepath)
dbObjects = backupOriginalObjects(sqlScriptListfilePath, origOutputFilepath)

#import pdb
#pdb.set_trace()
runNewSQLscripts(dbObjects, pathToNewSqlDir, newOutputFilepath)
outputSummary(dbObjects)

###############################################################

