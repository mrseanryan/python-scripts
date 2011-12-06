"""
script to manipulate a square matrix and normalise it

USAGE:  normalise_matrix <matrix data file> <matrix size> [options]

Dependencies:
Python 2.6 or higher

The options are:
[-h help]
[-t test]

Example: normalise_vector.py out.combined.dat 10

"""

# we normalise a matrix, by calculating its determinant, and then dividing each element by the determinant

# the determinant of a matrix, is 
# the product of the elements on the main diagonal top-left to bottom-right
# minus the product of the elements on the diagonal bottom-left to top-right.

from optparse import OptionParser

import sys

###############################################################
#usage() - prints out the usage text, from the top of this file :-)
def usage():
	print __doc__

###############################################################
#optparse - parse the args
parser = OptionParser(usage='%prog <matrix data file> <matrix size> [options]')
parser.add_option('-t', '--test', dest='testModeOn', action='store_const',
	 	 	 	const=True, default=False,
	 	 	 	help='turns on test mode, which does not require a file (default: off)')

matrixFilePath = ''
matrixSize = 0

(options, args) = parser.parse_args()
if(not options.testModeOn):
	if(len(args) != 2):
		usage()
		sys.exit(2)
	else:
		matrixFilePath = args[0]
		matrixSize = int(args[1])

# ================ FUNCTIONS ===============================

def createMatrix(n):
	mat = []
	for i in xrange(n):
		mat.append([])
		for j in xrange(n):
			mat[i].append(i+j)
	return mat

def getDeterminant(mat, n):
	#top-left to bottom-right:
	topLeftProduct = 1
	for i in xrange(n):
		topLeftProduct *= mat[i][i]
		
	bottomLeftProduct = 1
	#import pdb
	#pdb.set_trace()
	for i in xrange(n):
		bottomLeftProduct *= mat[i][n-i-1]

	return topLeftProduct - bottomLeftProduct

def getNormalisedMatrix(mat, n):
	divisor = getDeterminant(mat, n)
	print 'determinant = ' + str(divisor)
	#divide each element by the divisor:
	det = createMatrix(n)
	for i in xrange(n):
		for j in xrange(n):
			det[i][j] = float(mat[i][j]) / float(divisor)
	return det

def loadMatrix(n, matrixFilePath):
	mat = None
	raise('not impl !')

# =============== MAIN ==========================================

n = matrixSize

mat = None
if(options.testModeOn):
	#populate the matrix
	n = 3
	mat = createMatrix(n)
else:
	mat = loadMatrix(n, matrixFilePath)

print 'matrix: '
print mat

norm = getNormalisedMatrix(mat, n)
print 'normalised matrix: '
print norm

