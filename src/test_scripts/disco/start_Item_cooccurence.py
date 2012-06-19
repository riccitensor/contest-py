import json
from Create_User_Item_Matrix import Create_User_Item_Matrix
from disco.core import result_iterator

__author__ = 'karisu'

import disco



if __name__ == "__main__":
    #location = "tag://data:contest20"
    location = "tag://data:contesthundred"
    #location = "tag://data:implicit_all"

    last = Create_Item_Cooccurence().run(input=[location],
                              map_reader = disco.worker.classic.func.chain_reader
    ).wait(show=False)

    # open up file handle
    f = open('/tmp/disco_user_item_matrix', 'w')

    for userid, itemids in result_iterator(last):
        klm = itemids.keys()
        print klm
        klm = json.dumps(klm)
        f.write(klm + '\n')

    print "creating User Item Matrix"

    #next = Create_User_Item_Matrix().run(input=last).wait(show=False)

