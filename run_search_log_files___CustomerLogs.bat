REM search BWAC log files for special text

REM we search these kinds of files:
REM rar zip log

SETLOCAL

REM for clearer output, we search for 1 text item at a time

REM TEXT 1 ========================================

SET _TEXT_TO_SEARCH="CDatabase::GetpRst"

SET _RESULT_FILE="%TEMP%\log_search_result__CustomerLogs.txt"
SET _DIR_TO_SEARCH="\\iefiles4\Groups\Customer Logs"
CALL run_search_log_files_for_text.bat   %_DIR_TO_SEARCH%   %_TEXT_TO_SEARCH% %_RESULT_FILE%
IF %ERRORLEVEL% NEQ 0 ECHO "Some Error Occurred!"

REM TEXT 2 ========================================

SET _TEXT_TO_SEARCH="Error: COM exception"

SET _RESULT_FILE="%TEMP%\log_search_result__CustomerLogs.txt"
SET _DIR_TO_SEARCH="\\iefiles4\Groups\Customer Logs"
CALL run_search_log_files_for_text.bat   %_DIR_TO_SEARCH%   %_TEXT_TO_SEARCH% %_RESULT_FILE%
IF %ERRORLEVEL% NEQ 0 GOTO SomeErrorOccurred

REM Skip over the error handling and exit
GOTO Done

REM Report the compiler error; then exit
:SomeErrorOccurred
REM raise an error:
Error occurred!

:Done
ECHO Finished.
