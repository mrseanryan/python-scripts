@echo off

echo test diff against known good output:
diff_by_regex.py test_data\diff_by_regex\file_with_regex.txt  test_data\diff_by_regex\file_to_compare.txt

echo test diff with header:
diff_by_regex.py test_data\diff_by_regex\file_with_regex.txt  test_data\diff_by_regex\file_to_compare.txt -f

echo test diff a file that cannot be parsed by regex:
diff_by_regex.py  test_data\diff_by_regex\bad_regex.txt   test_data\diff_by_regex\bad_regex.txt -d

echo test diff a file that is same, only longer:
diff_by_regex.py  test_data\diff_by_regex\file_to_compare.txt  test_data\diff_by_regex\file_to_compare_longer.txt

echo test diff a file that is same, only shorter: (last line should show as different, because no line ending)
diff_by_regex.py  test_data\diff_by_regex\file_to_compare_longer.txt  test_data\diff_by_regex\file_to_compare.txt

echo test diff a file that is same, only longer: - with -d
diff_by_regex.py  test_data\diff_by_regex\file_to_compare.txt  test_data\diff_by_regex\file_to_compare_longer.txt		-d

echo test diff a file that is same, only shorter: (last line should show as different, because no line ending) - with -d
diff_by_regex.py  test_data\diff_by_regex\file_to_compare_longer.txt  test_data\diff_by_regex\file_to_compare.txt		-d

echo test diff of 2 larger files (same, but second is bigger):
diff_by_regex.py  test_data\diff_by_regex\IRD_calculation.template.processed.sql.appended		test_data\diff_by_regex\known_good_IRD_calculation.template.processed.sql.appended		-d
