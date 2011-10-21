@ECHO OFF
SETLOCAL

SET DIFF_BY_REGEX=diff_by_regex.py
REM SET DIFF_BY_REGEX=..\Testing\FileProcessingTests\shared\diff_by_regex.py

SET TEMPLATE_DIR=test_data\templates

SET SOURCE_FILE=%TEMPLATE_DIR%\file_template__source.sql
SET TEMPLATE_FILE=%TEMPLATE_DIR%\file_template.sql
SET OUTPUT_FILE=temp\process_text_template_from_file.output.sql

ECHO  ================= POPULATE TEMPLATE WITH WHOLE FILE ========================
process_text_template_from_file.py %SOURCE_FILE%	%TEMPLATE_FILE%	IRD_INSERT_POINT %OUTPUT_FILE%
IF %ERRORLEVEL% NEQ 0 GOTO SomeErrorOccurred

ECHO  ================= VERIFY OUTPUT ========================
"%DIFF_BY_REGEX%"		test_data\templates\known_good__process_text_template_from_file.output.sql			%OUTPUT_FILE%			-d
IF %ERRORLEVEL% EQU 0 GOTO TEST_OK
ECHO TEST_Differences_Found
REM This is a deliberate error, to trigger error in any calling script.
TEST_Differences_Found!
:TEST_OK

ECHO  ================= THE END ========================
REM Skip over the error handling and exit
GOTO Done

REM Report the compiler error; then exit.
:SomeErrorOccurred
ECHO SomeErrorOccurred
REM This is a deliberate error, to trigger error in any calling script.
Error_occurred!

:Done
ECHO Finished.
