REM search BWAC log files for special text

REM we search these kinds of files:
REM rar zip log

SETLOCAL

SET _DIR_TO_SEARCH=%1

SET _TEXT_TO_SEARCH=%2

python unzip_and_find_text.py %_DIR_TO_SEARCH% %_TEXT_TO_SEARCH%
IF %ERRORLEVEL% NEQ 0 GOTO SomeErrorOccurred

REM Skip over the error handling and exit
GOTO Done

REM Report the compiler error; then exit
:SomeErrorOccurred
REM Raise an error:
Error occurred!

:Done
ECHO Finished.
