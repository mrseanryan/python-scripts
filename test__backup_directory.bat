REM test the backup_directory script

SETLOCAL

REM create some files to test they are NOT deleted:

SET _ARCHIVE_DIR=temp

SET _OTHER_FILE_1=%_ARCHIVE_DIR%\my_other_file.txt
IF NOT EXIST %_OTHER_FILE_1% (echo "some other file" > %_OTHER_FILE_1%)

SET _OTHER_FILE_2=%_ARCHIVE_DIR%\my_other_file_auto_.txt
IF NOT EXIST %_OTHER_FILE_2% (echo "some other file 2" > %_OTHER_FILE_2%)

python backup_directory.py test_data %_ARCHIVE_DIR% 5  -y
IF %ERRORLEVEL% NEQ 0 GOTO SomeErrorOccurred

type %_OTHER_FILE_1%
IF %ERRORLEVEL% NEQ 0 GOTO SomeErrorOccurred

type %_OTHER_FILE_2%
IF %ERRORLEVEL% NEQ 0 GOTO SomeErrorOccurred


REM Skip over the error handling and exit
GOTO Done

REM Report the compiler error; then exit
:SomeErrorOccurred
ECHO Error occurred!

:Done
ECHO Finished.
