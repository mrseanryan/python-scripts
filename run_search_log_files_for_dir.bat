REM search BWAC log files for special text

REM we search these kinds of files:
REM rar zip log

REM usage:
REM run_search_log_files_for_dir.bat <path to search for files>

SETLOCAL

SET _SRC_DIR=%1

mkdir "%TEMP%\log_processor"

REM we run the process for each kind of file extension:
SET _SCRIPT_TO_RUN=run__unzip_and_find_text__in_ZIP.bat
operate_on_each_file.py -s "%_SRC_DIR%" -t "%_SCRIPT_TO_RUN%"   -i "%TEMP%\_log_archive.zip"   -f "%TEMP%\log_file_search_result.txt"  -e zip;  -o "%TEMP%\log_processor" -y
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

SET _SCRIPT_TO_RUN=run__unzip_and_find_text__in_RAR.bat
operate_on_each_file.py -s "%_SRC_DIR%" -t "%_SCRIPT_TO_RUN%"   -i "%TEMP%\_log_archive.rar"   -f "%TEMP%\log_file_search_result.txt"  -e rar;  -o "%TEMP%\log_processor" -y
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

SET _SCRIPT_TO_RUN=run__unzip_and_find_text__in_LOG.bat
operate_on_each_file.py -s "%_SRC_DIR%" -t "%_SCRIPT_TO_RUN%"   -i "%TEMP%\_log_archive.log"   -f "%TEMP%\log_file_search_result.txt"  -e log;  -o "%TEMP%\log_processor" -y
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

REM Skip over the error handling and exit
GOTO Done

REM Report the compiler error; then exit
:SomeErrorOccurred
ECHO Error occurred!

:Done
ECHO Finished.
