SETLOCAL

process_text_template_test.py

REM TODO - diff against known good output

SET templateFilePath=test_data\templates\IRD_calculation.template.sql

SET outputFilepath=temp\IRD_calculation.template.processed.sql

diff_by_regex.py	%templateFilePath%		%outputFilepath%
