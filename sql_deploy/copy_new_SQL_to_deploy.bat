@ECHO OFF

REM script to copy new SQL to a temp DEPLOY directory, to make it easy to deploy SQL

REM TODO - replace this with a proper installer (InnoSetup) that reads from the database_scripts directory

SETLOCAL

SET DEST_DIR=%PATH_TO_COMREG%\temp.deploy.me

IF NOT EXIST %DEST_DIR% (MKDIR %DEST_DIR%)

SET DEST_DIR_PARENT=%DEST_DIR%

SET DEST_DIR=%DEST_DIR%\sql

IF NOT EXIST %DEST_DIR% (MKDIR %DEST_DIR%)

del /Q %DEST_DIR%\*.*

REM TODO make a nice py script to read from a CSV file instead

SET SCRIPT_SRC=%PATH_TO_COMREG%\LING\sql\scripts
SET SCRIPT_SRC_SQL=%PATH_TO_COMREG%\LING\sql\database_scripts

echo .
echo Copying deploy scripts ...
xcopy /Y		%SCRIPT_SRC%\list_of_SQL_scripts_to_deploy.csv					%DEST_DIR%\
IF %ERRORLEVEL% NEQ 0 (GOTO ERROR_LABEL)

xcopy /Y		%SCRIPT_SRC%\*.py													%DEST_DIR%\
IF %ERRORLEVEL% NEQ 0 (GOTO ERROR_LABEL)

xcopy /Y		%SCRIPT_SRC%\run_deploySQL.bat											%DEST_DIR%\
IF %ERRORLEVEL% NEQ 0 (GOTO ERROR_LABEL)

echo .
echo Copying SQL scripts ...

CopySQLtoDeploy.py list_of_SQL_scripts_to_deploy.csv          %SCRIPT_SRC_SQL%\     %DEST_DIR%\

REM *** ADD YOUR MODIFIED SQL SCRIPTS TO THE CSV FILE ***

echo .
echo Listing the files to deploy:
tree /f %DEST_DIR_PARENT%
IF %ERRORLEVEL% NEQ 0 (GOTO ERROR_LABEL)

explorer %DEST_DIR_PARENT%
REM IF %ERRORLEVEL% NEQ 0 (GOTO ERROR_LABEL)

GOTO DONE

:ERROR_LABEL
error_occurred!

:DONE
REM pause
