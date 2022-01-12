# python 3
"""
move-non-selected-images.py

Moves any image files that are not named like x.y.extension.

The files are moved to a subdirectory 'not-selected'.

USAGE: move-non-selected-images.py <path to directory>
"""
from optparse import OptionParser
from os import walk
import os
from pathlib import Path
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
                  help='Dry run - no files will be moved')

(options, args) = parser.parse_args()
if(len(args) != 1):
    usage()
    sys.exit(2)
sourceDirPath = args[0]


def has_multiple_dots(filename):
    return filename.count('.') > 1


def move_file_do(filepath, target_dir_path):
    if options.is_dry_run:
        print(f"[dry run] Moving file {filepath} -> {target_dir_path}")
        return
    print(f"Moving file {filepath} -> {target_dir_path}")
    Path(target_dir_path).mkdir(parents=True, exist_ok=True)
    filename = os.path.basename(filepath)
    target_file_path = os.path.join(target_dir_path, filename)
    os.rename(filepath, target_file_path)


def move_file(filename, dir_path):
    source_file_path = os.path.join(dir_path, filename)
    if os.path.isfile(source_file_path):
        move_file_do(source_file_path, os.path.join(dir_path, "not-selected"))


def move_files(dir_path):
    filenames = os.listdir(dir_path)

    # files_txt = [i for i in files if i.endswith('.txt')]
    filenames = list(filter(lambda f: (f.endswith(".JPG") or f.endswith(
        ".jpg") or f.endswith(".jpeg")) and not has_multiple_dots(f), filenames))

    for filename in filenames:
        move_file(filename, dir_path)
        raw_file_sony = Path(filename).stem + '.ARW'
        move_file(raw_file_sony, dir_path)
        raw_file = Path(filename).stem + '.RAW'
        move_file(raw_file, dir_path)
    print(f"{len(filenames)} file sets found (JPG + raw file(s))")


move_files(sourceDirPath)
