REM summarise the results from the log search

REM dependency:   DOS UNIX utilities  (grep.exe)

REM we grep twice:  1. to select only interesting lines, 2. to remove unwanted lines.

grep -i found         %TEMP%\log_search_result__CustomerLogs.txt				>				%TEMP%\log_search_summary___CustomerLogs.temp
grep -i -v "The text was found"         %TEMP%\log_search_summary___CustomerLogs.temp				>				%TEMP%\log_search_summary___CustomerLogs.txt

grep -i found         %TEMP%\log_search_result___BWAC_3_1_0_Large_Logfiles.txt				>				%TEMP%\log_search_summary___BWAC_3_1_0.temp
grep -i -v "The text was found"         %TEMP%\log_search_summary___BWAC_3_1_0.temp			>		%TEMP%\log_search_summary___BWAC_3_1_0.txt

grep -i found         %TEMP%\log_search_result___BWAC_3_1_1_Large_Logfiles.txt				>				%TEMP%\log_search_summary___BWAC_3_1_1.temp
grep -i -v "The text was found"         %TEMP%\log_search_summary___BWAC_3_1_1.temp			>		%TEMP%\log_search_summary___BWAC_3_1_1.txt

grep -i found         %TEMP%\log_search_result___BWAC_3_1_2_Large_Logfiles.txt				>				%TEMP%\log_search_summary___BWAC_3_1_2.temp
grep -i -v "The text was found"         %TEMP%\log_search_summary___BWAC_3_1_2.temp			>		%TEMP%\log_search_summary___BWAC_3_1_2.txt
