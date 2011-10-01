echo test diff against known good output:
diff_by_regex.py test_data\diff_by_regex\file_with_regex.txt  test_data\diff_by_regex\file_to_compare.txt

echo test diff with header:
diff_by_regex.py test_data\diff_by_regex\file_with_regex.txt  test_data\diff_by_regex\file_to_compare.txt -f
