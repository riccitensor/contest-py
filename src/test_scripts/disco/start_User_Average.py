import json
from Create_User_Item_Matrix import Create_User_Item_Matrix
from disco.core import result_iterator
from Create_User_Average_Items import Create_User_Average_Item
import disco
__author__ = 'karisu'





if __name__ == "__main__":
    location = "http://localhost/results.out"

    """
    last = Create_User_Item_Histogramm().run(input=[location],
                              map_reader = disco.worker.classic.func.chain_reader
    ).wait(show=True)"""

    last = Create_User_Average_Item().run(input=[location]).wait(show=True)


    # open up file handle
    #f = open('/tmp/disco_user_item_matrix', 'w')



    for userid, count in result_iterator(last):
        print "userid: {} \t count: {}".format(userid, count)















