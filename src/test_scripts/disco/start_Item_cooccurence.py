import json
from Create_Item_Based_CF import Create_Item_Based_CF
from disco.core import result_iterator

__author__ = 'karisu'

import disco





if __name__ == "__main__":
    from scipy.sparse import lil_matrix
    from scipy.sparse.linalg import spsolve
    from numpy.linalg import solve, norm
    from numpy.random import rand


    i = { 1 : 1, 2 : 1, 4 : 1 }

    A = lil_matrix((1000, 1000))
    # A[0, :100] = rand(100)
    # A[1, 100:200] = A[0, :100]
    # A.setdiag(rand(1000))

    A = A.tocsr()
    print A
    b = rand(1000)
    print b
    x = spsolve(A, b)
    print x

    x_ = solve(A.todense(), b)


    err = norm(x-x_)
    err < 1e-10



    """
    location = "/var/www/user_item_matrix"
    last = Create_Item_Based_CF().run(
        input=[location]
    ).wait(show=False)

    # open up file handle
    #f = open('/var/www/', 'r')

    for userid, itemids in result_iterator(last):
        klm = itemids.keys()
        print klm
        klm = json.dumps(klm)
        f.write(klm + '\n')

    print "creating User Item Matrix"

    #next = Create_User_Item_Matrix().run(input=last).wait(show=False)

    """