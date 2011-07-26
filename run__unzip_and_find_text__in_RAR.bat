
REM script with NO arguments, that runs the python to unzip and find text in a single archive file.

REM note that the file names here, must agree with whatever was passed in to operate_on_each_file.py

python unzip_and_find_text.py "%TEMP%\_log_archive.rar" "CDatabase::GetpRst"

python unzip_and_find_text.py "%TEMP%\_log_archive.rar" "Error: COM exception"
