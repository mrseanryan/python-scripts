"""
script to manipulate a square matrix and normalise it

USAGE:  normalise_matrix <matrix data file A> <matrix size> <operation> [matrix data file B] [options]

where operation is one of:
norm = normalise A
subtract = perform A - B

Dependencies:
Python 2.6 or higher

The options are:
[-h help]
[-s save filePath = save new matrix to file path]
[-t test]

Example: normalise_vector.py out.combined.dat 10 norm -save combined.norm.dat

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
parser = OptionParser(usage='%prog <matrix data file> <matrix size> <operation> [matrix data file B] [options]')
parser.add_option('-t', '--test', dest='testModeOn', action='store_const',
	 	 	 	const=True, default=False,
	 	 	 	help='turns on test mode, which does not require a file (default: off)')

parser.add_option("-s", "--save", action="store", type="string",
                      dest="saveFilePath", help="Save result to file path")

matrixFilePathA = ''
matrixSize = 0
matrixFilePathB = ''
operation = ''

(options, args) = parser.parse_args()
if(not options.testModeOn):
	operation = args[2]
	
	if operation == 'norm':	
		if(len(args) != 3):
			usage()
			sys.exit(2)
		else:
			matrixFilePathA = args[0]
			matrixSize = int(args[1])
	elif operation == 'subtract':	
		if(len(args) != 4):
			usage()
			sys.exit(2)
		else:
			matrixFilePathA = args[0]
			matrixSize = int(args[1])
			matrixFilePathB = args[3]
	else:
		print 'unknown operation ' + operation
		usage()
		sys.exit(3)
		
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

	delim = ' '
	mat = createMatrix(n)
	matrixFile = open(matrixFilePath, 'r')
	iRow = 0
	for line in matrixFile:
		cells = line.split(delim)
		iCol = 0
		for cell in cells:
			if cell == '\n':
				continue
			mat[iRow][iCol] = float(cell)
			iCol = iCol + 1
		iRow = iRow + 1
	return mat

def saveMatrix(filePath, mat, n):
	matFile = open(filePath, 'w')
	for i in xrange(n):
		line = ''
		for j in xrange(n):
			line += str(mat[i][j]) + ' '
		matFile.write(line)
		matFile.write('\n')

def subtract(matA, matB, n):
	matDiff = createMatrix(n)
	for i in xrange(n):
		for j in xrange(n):
			matDiff[i][j] = matA[i][j] - matB[i][j]
	return matDiff

# =============== MAIN ==========================================

n = matrixSize

#populate the matrix A
matA = None
if(options.testModeOn):
	print 'test mode - setting operation = norm'
	n = 3
	matA = createMatrix(n)
	operation = 'norm'
else:
	matA = loadMatrix(n, matrixFilePathA)

print 'matrix A: '
print matA

matResult = createMatrix(n)

if operation == 'norm':
	norm = getNormalisedMatrix(matA, n)
	print 'normalised matrix: '
	print norm
	matResult= norm
elif operation == 'subtract':
	matB = loadMatrix(n, matrixFilePathB)
	print 'matrix B:'
	print matB
	
	matDiff = subtract(matA, matB, n)
	print 'matrix A - matrix B = '
	print matDiff
	matResult = matDiff
else:
	raise Exception('unknown operation - ' + operation)

if options.saveFilePath is not None and len(options.saveFilePath) > 0:
	print 'saving result to file ' + options.saveFilePath
	saveMatrix(options.saveFilePath, matResult, n)
