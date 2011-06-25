REM test the py script    find_files_by_size.py

REM find files of size 29 bytes in current dir, and sub-dirs:
python find_files_by_size.py -e * "c:\System Volume Information" 29  -y

