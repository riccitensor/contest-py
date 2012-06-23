import json

from disco.core import result_iterator
from Create_Filter_Users_below_average import Create_Filter_Users_below_average
import disco
__author__ = 'karisu'





if __name__ == "__main__":
    location = "http://localhost/results20"
    location = "http://localhost/results.out"

    last = Create_Filter_Users_below_average().run(input=[location],
                                                   partitions = 10).wait(show=True)


    # open up file handle
    #f = open('/tmp/disco_user_item_matrix', 'w')



    for userid, count in result_iterator(last):
        print "userid: {} \t count: {}".format(userid, count)















