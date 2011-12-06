"""
script to manipulate a matrix
and normalise it

"""

# we normalise a matrix, by calculating its determinant, and then dividing each element by the determinant

# the determinant of a matrix, is 
# the product of the elements on the main diagonal top-left to bottom-right
# minus the product of the elements on the diagonal bottom-left to top-right.

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

# =========================================================

#populate the matrix
n = 3
mat = createMatrix(n)

print 'matrix: '
print mat


norm = getNormalisedMatrix(mat, n)
print 'normalised matrix: '
print norm

