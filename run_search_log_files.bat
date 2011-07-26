REM search BWAC log files for special text

REM we search these kinds of files:
REM rar zip log

SETLOCAL

python unzip_and_find_text.py xxxxx 

REM for clearer output, we search for 1 text item at a time

REM TEXT 1 ========================================

SET _TEXT_TO_SEARCH="CDatabase::GetpRst"

SET _DIR_TO_SEARCH="\\iefiles4\Groups\Customer Logs"
CALL run_search_log_files_for_text.bat   %_DIR_TO_SEARCH%   %_TEXT_TO_SEARCH%
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

SET _DIR_TO_SEARCH="\\iefiles4\Groups\QA\BWAC_3_1_0_Large_Logfiles"
CALL run_search_log_files_for_text.bat   %_DIR_TO_SEARCH%   %_TEXT_TO_SEARCH%
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

SET _DIR_TO_SEARCH="\\iefiles4\Groups\QA\BWAC_3_1_1_Large_Logfiles"
CALL run_search_log_files_for_text.bat   %_DIR_TO_SEARCH%   %_TEXT_TO_SEARCH%
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

SET _DIR_TO_SEARCH="\\iefiles4\Groups\QA\BWAC_3_1_2_Large_Logfiles"
CALL run_search_log_files_for_text.bat   %_DIR_TO_SEARCH%   %_TEXT_TO_SEARCH%
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

REM TEXT 2 ========================================

SET _TEXT_TO_SEARCH=�Error: COM exception�

SET _DIR_TO_SEARCH="\\iefiles4\Groups\Customer Logs"
CALL run_search_log_files_for_text.bat   %_DIR_TO_SEARCH%   %_TEXT_TO_SEARCH%
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

SET _DIR_TO_SEARCH="\\iefiles4\Groups\QA\BWAC_3_1_0_Large_Logfiles"
CALL run_search_log_files_for_text.bat   %_DIR_TO_SEARCH%   %_TEXT_TO_SEARCH%
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

SET _DIR_TO_SEARCH="\\iefiles4\Groups\QA\BWAC_3_1_1_Large_Logfiles"
CALL run_search_log_files_for_text.bat   %_DIR_TO_SEARCH%   %_TEXT_TO_SEARCH%
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

SET _DIR_TO_SEARCH="\\iefiles4\Groups\QA\BWAC_3_1_2_Large_Logfiles"
CALL run_search_log_files_for_text.bat   %_DIR_TO_SEARCH%   %_TEXT_TO_SEARCH%
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

REM Skip over the error handling and exit
GOTO Done

REM Report the compiler error; then exit
:SomeErrorOccurred
ECHO Error occurred!

:Done
ECHO Finished.