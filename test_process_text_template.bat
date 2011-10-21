@ECHO OFF
SETLOCAL

SET DIFF_BY_REGEX=diff_by_regex.py
REM SET DIFF_BY_REGEX=..\Testing\FileProcessingTests\shared\diff_by_regex.py

if not exist temp (mkdir temp)

process_text_template_test.py

REM TODO - diff against known good output

SET templateFilePath=test_data\templates\IRD_calculation.template.sql


SET outputFilepath=temp\IRD_calculation.template.processed.sql

SET known_good=test_data\templates\known_good_IRD_calculation.template.processed.sql

echo Diff of known good template VS the actual template output:
%DIFF_BY_REGEX%	%known_good%		%outputFilepath%			-d


echo Diff of known good template VS the actual template output: - APPENDED file
%DIFF_BY_REGEX%	%known_good%.appended		%outputFilepath%.appended			-d
