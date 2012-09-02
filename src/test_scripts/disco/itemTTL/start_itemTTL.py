import json
from Create_Group_By_id import Create_Group_By_id
from Create_discretize import Create_discretize
from Create_Item_Hit_Count import Create_Item_Hit_Count
from disco.core import result_iterator

import disco
__author__ = 'karisu'





if __name__ == "__main__":
    location = "http://localhost/user_item_time_2"


    group = Create_Group_By_id().run(input=[location]).wait(show=False)

    print "item with their timestamps"
    #for id, timestampList in result_iterator(group):
    #    print "{} \t timestamp: {}".format(id, timestampList)


    """
    last = Create_Item_Hit_Count().run(input=[group],
                                  map_reader = disco.worker.classic.func.chain_reader
    ).wait(show=False)
    print "item hit count"
    for id, timestampList in result_iterator(last):
        print "{} \t: {}".format(id, timestampList)
    """

    discrete = Create_discretize().run(input=[group],
                                       map_reader = disco.worker.classic.func.chain_reader).wait(show=True)

    print "item with their timestamps"
    for id, timestampList in result_iterator(discrete):
        print "{} \t timestamp: {}".format(id, timestampList)




"""
    from scipy.stats.distributions import random
    import numpy as np
    from pandas import *
    import matplotlib.pyplot as plt


    randn = np.random.randn
    #s = Series(data, index=index)
    #s = Series(randn(5), index=['a', 'b', 'c', 'd', 'e'] )

    mydata = { 'h:1' : 3, 'h:2' : 5, 'h:3' : 10, 'h:4' : 14, 'h:5' : 10, 'h:6' : 8, 'h:7' : 6, 'h:8' : 3 }
    s1 = Series(mydata)
    mydata = { 'h:1' : 5, 'h:2' : 6, 'h:3' : 11, 'h:4' : 12, 'h:5' : 11, 'h:6' : 7, 'h:7' : 2, 'h:8' : 1 }
    s2 = Series(mydata)


    x = random(10)
    print x
    d = {'one' : s1,
         'two' : s2}
    df = DataFrame(d)
    df.plot()

    plt.show()
"""