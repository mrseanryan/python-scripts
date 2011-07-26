REM search BWAC log files for special text

REM we search these kinds of files:
REM rar zip log

REM usage:
REM run_search_log_files_for_dir.bat <path to search for files>

SETLOCAL

SET _SRC_DIR=%1

mkdir "%TEMP%\log_processor"

SET _SCRIPT_TO_RUN=unzip_and_find_text.py

REM we run the process for each kind of file extension:
operate_on_each_file.py -s "%_SRC_DIR%" -t "%_SCRIPT_TO_RUN%"   -i "%TEMP%\_log_archive.zip"   -f "%TEMP%\_log_processed.txt"  -e zip;  -o "%TEMP%\log_processor"
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

operate_on_each_file.py -s "%_SRC_DIR%" -t "%_SCRIPT_TO_RUN%"   -i "%TEMP%\_log_archive.rar"   -f "%TEMP%\_log_processed.txt"  -e rar;  -o "%TEMP%\log_processor"
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

operate_on_each_file.py -s "%_SRC_DIR%" -t "%_SCRIPT_TO_RUN%"   -i "%TEMP%\_log_archive.log"   -f "%TEMP%\_log_processed.txt"  -e log;  -o "%TEMP%\log_processor"
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

REM Skip over the error handling and exit
GOTO Done

REM Report the compiler error; then exit
:SomeErrorOccurred
ECHO Error occurred!

:Done
ECHO Finished.
