pushd test_data\find_and_insert
del *.sql
rename *.orig *.sql
popd

python find_and_insert.py  test_data\find_and_insert    -y
