SETLOCAL

if not exist temp (mkdir temp)

process_text_template_test.py

REM TODO - diff against known good output

SET templateFilePath=test_data\templates\IRD_calculation.template.sql

SET outputFilepath=temp\IRD_calculation.template.processed.sql

SET known_good=test_data\templates\known_good_IRD_calculation.template.processed.sql

diff_by_regex.py	%known_good%		%outputFilepath%			-d
