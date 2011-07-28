REM TEST to try the BAT files, that search BWAC log files for special text

REM we search these kinds of files:
REM rar zip log

SETLOCAL

REM for clearer output, we search for 1 text item at a time

REM TEXT 1 ========================================

SET _TEXT_TO_SEARCH="Error: COM exception"

SET _DIR_TO_SEARCH="test_data"

SET _RESULT_FILE="%TEMP%\log_search_result_1.txt"

CALL run_search_log_files_for_text.bat   %_DIR_TO_SEARCH%   %_TEXT_TO_SEARCH% %_RESULT_FILE%
IF %ERRORLEVEL% NEQ 0 GOTO SomeErrorOccurred

REM Skip over the error handling and exit
GOTO Done

REM Report the compiler error; then exit
:SomeErrorOccurred
REM Raise an error:
Error occurred!

:Done
ECHO Finished.
