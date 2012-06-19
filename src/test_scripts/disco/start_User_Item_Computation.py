import json
from Create_User_Item_Matrix import Create_User_Item_Matrix
from disco.core import result_iterator
from Create_Item_Coocurrence import Create_Item_Coocurrence

__author__ = 'karisu'

import disco



if __name__ == "__main__":
    #location = "tag://data:contest20"
    location = "tag://data:contesthundred"
    #location = "tag://data:implicit_all"

    last = Create_User_Item_Matrix().run(input=[location],
                              map_reader = disco.worker.classic.func.chain_reader
    ).wait(show=False)

    # open up file handle
    f = open('/tmp/disco_user_item_matrix', 'w')


    """
        for userid, itemids in result_iterator(last):
        f.write(itemids + '\n')
    """
    print "creating User Item Matrix"


    next = Create_Item_Coocurrence().run(input=last,
                map_reader = disco.worker.classic.func.chain_reader).wait(show=False)

    for word, count in result_iterator(next):
        print word, count

    print "done with second stage"

    #next = Create_User_Item_Matrix().run(input=last).wait(show=False)

