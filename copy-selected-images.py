# python 3
"""
copy-non-selected-images.py

Copies any image file-sets that ARE named like x.y.jpg.

The files (JPEG and any matching raw files) are copied to a subdirectory 'selected'.

USAGE: copy-selected-images.py <path to directory>
"""
from optparse import OptionParser
import os
from pathlib import Path
import shutil
import sys


###############################################################
# usage() - prints out the usage text, from the top of this file :-)
def usage():
    print(__doc__)


###############################################################
# optparse - parse the args
parser = OptionParser(usage='%prog <directory> [options]')
parser.add_option('-d', '--dryrun', dest='is_dry_run', action="store_true",
                  default=False,
                  help='Dry run - no files will be copied')

(options, args) = parser.parse_args()
if(len(args) != 1):
    usage()
    sys.exit(2)
sourceDirPath = args[0]


def has_multiple_dots(filename):
    return filename.count('.') > 1


def copy_file_do(filepath, target_dir_path):
    if options.is_dry_run:
        print(f"[dry run] Copying file {filepath} -> {target_dir_path}")
        return
    print(f"Copying file {filepath} -> {target_dir_path}")
    Path(target_dir_path).mkdir(parents=True, exist_ok=True)
    filename = os.path.basename(filepath)
    target_file_path = os.path.join(target_dir_path, filename)
    shutil.copy2(filepath, target_file_path)


def copy_file(filename, dir_path):
    source_file_path = os.path.join(dir_path, filename)
    if os.path.isfile(source_file_path):
        copy_file_do(source_file_path, os.path.join(dir_path, "selected"))

def get_stem(filename):
    filename_with_dots = Path(filename).stem
    first_dot_pos = filename_with_dots.find(".")
    return filename_with_dots[0:first_dot_pos]

def copy_files(dir_path):
    filenames = os.listdir(dir_path)

    # files_txt = [i for i in files if i.endswith('.txt')]
    filenames = list(filter(lambda f: (f.endswith(".JPG") or f.endswith(
        ".jpg") or f.endswith(".jpeg")) and has_multiple_dots(f), filenames))

    for filename in filenames:
        copy_file(filename, dir_path)
        # Sony, RAW, Panasonic
        raw_file_extensions = ['.ARW', '.RAW', '.RW2']
        stem = get_stem(filename)
        for raw_ext in raw_file_extensions:
            raw_file_path = stem + raw_ext
            copy_file(raw_file_path, dir_path)
    print(f"{len(filenames)} file sets found (JPG + raw file(s))")


copy_files(sourceDirPath)
