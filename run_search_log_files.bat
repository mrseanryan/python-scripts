REM search BWAC log files for special text

REM we search these kinds of files:
REM rar zip log

mkdir "%TEMP%\log_processor"

CALL run_search_log_files_for_dir.bat  "\\iefiles4\Groups\Customer Logs"
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

CALL run_search_log_files_for_dir.bat  "\\iefiles4\Groups\QA\BWAC_3_1_0_Large_Logfiles"
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

CALL run_search_log_files_for_dir.bat  "\\iefiles4\Groups\QA\BWAC_3_1_1_Large_Logfiles"
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

CALL run_search_log_files_for_dir.bat  "\\iefiles4\Groups\QA\BWAC_3_1_2_Large_Logfiles"
IF ERRORLEVEL NEQ 0 GOTO SomeErrorOccurred

REM Skip over the error handling and exit
GOTO Done

REM Report the compiler error; then exit
:SomeErrorOccurred
ECHO Error occurred!

:Done
ECHO Finished.
