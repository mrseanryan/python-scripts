pushd test_data\add_file_headers
del *.sql
rename *.orig *.sql
popd

python add_file_headers.py  test_data\add_file_headers    test_data\add_file_headers\sql_header.txt    test_data\add_file_headers\sql_footer.txt    -y
