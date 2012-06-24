import numpy
from numpy.matrixlib.defmatrix import mat
import scipy.linalg
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve
from numpy.linalg import solve, norm
from numpy.random import rand


v1 = lil_matrix((1, 10)) # create Row-based linked list sparse matrix
v1[0,0] = 1
v1[0,1] = 1
v1_transpose = v1.transpose()

A = v1_transpose * v1
#print "A"
#print A


v2 = lil_matrix((1, 10)) # create Row-based linked list sparse matrix
v2[0,0] = 1
v2[0,1] = 1
v2_transpose = v2.transpose()
B = v2_transpose * v2
#print "B"
#print B

D = lil_matrix((10, 10)) # create Row-based linked list sparse matrix

#print "A + B"
D = D + A
#print D
#print ""
D = D + B
#print D


v3 = lil_matrix((1, 10)) # create Row-based linked list sparse matrix
v3[0,0] = 1
v3[0,1] = 1
v3_transpose = v3.transpose()
C = v3_transpose * v3
print C

import numpy

factor = C.sum(axis=1)
nnzeros = numpy.where(factor > 0)
print nnzeros
print "\n\n"
print type(factor)

#print A[1, :]
