import json
from Create_User_Item_Matrix import Create_User_Item_Matrix
from disco.core import result_iterator
from Create_User_Item_Histogramm import Create_User_Item_Histogramm
import disco
__author__ = 'karisu'





if __name__ == "__main__":
    location = "tag://data:contest20"
    #location = "tag://data:contesthundred"
    location = "tag://data:implicit_all"
    #location = "tag://data:bench_700"
    #location = "tag://data:bench_100"

    """
    last = Create_User_Item_Histogramm().run(input=[location],
                              map_reader = disco.worker.classic.func.chain_reader
    ).wait(show=True)"""

    Create_User_Item_Histogramm().run(input=[location],
                                             map_reader = disco.worker.classic.func.chain_reader,
    ).wait(show=True)


    # open up file handle
    #f = open('/tmp/disco_user_item_matrix', 'w')


    """
    for userid, count in result_iterator(last):
        print "userid: {} \t count: {}".format(userid, count)
           #f.write(itemids + '\n')
    """
    print "creating User Item Histogramm"

    import redis
    redis_con = redis.Redis('localhost')

    print redis_con.zrevrangebyscore('userHistogramm', float("infinity"), 1, withscores=True, start=0, num=1000)








