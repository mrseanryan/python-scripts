@ECHO OFF

echo .
echo USAGE
normalise_matrix.py

echo .
echo TEST MODE:
normalise_matrix.py -t

echo .
echo LOAD MATRIX FILE and NORMALISE:
normalise_matrix.py test_data\small_matrix.dat 3 norm

echo .
echo LOAD 2 MATRIX FILES and SUBTRACT:
normalise_matrix.py test_data\small_matrix.dat 3 subtract test_data\small_matrix.2.dat 

echo .
echo LOAD 2 MATRIX FILES and SUBTRACT and SAVE:
if not exist temp (mkdir temp)
if exist temp\matrix.diff.dat (del temp\matrix.diff.dat)
normalise_matrix.py test_data\small_matrix.dat 3 subtract test_data\small_matrix.2.dat -s temp\matrix.diff.dat

echo .
echo LOAD DIFF MATRIX FILE and NORMALISE:
normalise_matrix.py temp\matrix.diff.dat 3 norm
