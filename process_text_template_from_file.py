"""
Script to populate a template file, by inserting the WHOLE contents of another file

USAGE:
process_text_template_from_file.py <source filepath>	<template filepath>	<template variable>	<output filepath>	[options]
"""

from process_text_template import *

from optparse import OptionParser

import sys


###############################################################
# Define some defaults:

#LOG_WARNINGS_ONLY - this means, only output if the verbosity is LOG_WARNINGS
LOG_ERRORS, LOG_WARNINGS, LOG_WARNINGS_ONLY, LOG_INFO, LOG_VERBOSE, LOG_DEBUG = range(6)
logVerbosity = LOG_VERBOSE

#debug:
#logVerbosity = LOG_DEBUG


###############################################################
#usage() - prints out the usage text, from the top of this file :-)
def usage():
	print __doc__

###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog  <source filepath>	<template filepath>	<template variable>	<output filepath> [options]')
#parser.add_option('-f', '--first line is heading', dest='firstLineIsHeading', action='store_const',
#                   const=True, default=False,
#                   help='Always output the first line as a heading, if there are differences found. (default: off)')

(options, args) = parser.parse_args()
if(len(args) != 4):
	usage()
	sys.exit(2)
#logVerbosity = options.warnings

source_filepath = args[0]
template_filepath = args[1]
template_variable =  args[2]
output_filepath = args[3]

## ============================ BEGIN FUNCTIONS ===================================

## ============================ END FUNCTIONS ===================================

## ============================ BEGIN MAIN ===================================
source_file = open(source_filepath, 'r')
source_text = ""
for source_line in source_file:
	source_text = source_text + source_line

#populate the template variable:
varToValue = dict()
varToValue[template_variable] = source_text

#process the template, to create the output file:
processTemplate(template_filepath, varToValue, output_filepath)

## ============================ END MAIN ===================================
