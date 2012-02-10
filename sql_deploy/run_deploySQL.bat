@ECHO OFF

SETLOCAL


REM TODO - would need to change this in ComReg
REM it should point to the 'sql' directory of the installation
SET PATH_TO_NEW_SQL_DIR=%PATH_TO_COMREG%\LING\sql\database_scripts\

SET PATH_TO_DUMP_OUT=%PATH_TO_NEW_SQL_DIR%originalSqlObjects.sql
SET PATH_TO_NEW_RESULTS=%PATH_TO_NEW_SQL_DIR%newSQLresults.txt

REM WinXP + SQL SERVER 2005:
SET PATH_TO_SQLCMD_DIR=c:\Progra~1\MI6841~1\90\Tools\Binn\\

REM for ComReg DEV box:
REM SET PATH_TO_SQLCMD_DIR=c:\Progra~1\MI6841~1\100\Tools\Binn\\

REM for Windows7 + SQLSERVER2008:
REM SET PATH_TO_SQLCMD_DIR=c:\Progra~1\MICROS~4\100\Tools\Binn\\

echo deploying SQL scripts:
DeploySQL.py  (local) licensing_dev licensing skyandsing3 list_of_SQL_scripts_to_deploy.csv   %PATH_TO_DUMP_OUT%		%PATH_TO_NEW_SQL_DIR%		%PATH_TO_NEW_RESULTS%		%PATH_TO_SQLCMD_DIR%
IF %ERRORLEVEL% NEQ 0 (GOTO ERROR_LABEL)

ECHO Original SQL objects have been backed up to %PATH_TO_DUMP_OUT%
REM echo backup of original SQL:
REM type %PATH_TO_DUMP_OUT%
REM IF %ERRORLEVEL% NEQ 0 (GOTO ERROR_LABEL)

GOTO DONE

:ERROR_LABEL
error occurred!

REM type %PATH_TO_DUMP_OUT%

:DONE
