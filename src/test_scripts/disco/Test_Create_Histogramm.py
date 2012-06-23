__author__ = 'karisu'

import unittest
import redis
from Create_User_Item_Histogramm import Create_User_Item_Histogramm
from Create_User_Item_Histogramm_combiner import Create_User_Item_Histogramm_combiner
import disco

from test_scripts.disco.Create_User_Item_Matrix import Create_User_Item_Matrix


class Test_Create_User_Item(unittest.TestCase):

    redis_con = None

    def setUp(self):

        self.redis_con = redis.Redis('localhost')
        self.redis_con.flushall()


    def tearDown(self):
        pass


    def test_Histogramm(self):

        # location = "tag://data:contesthundred"
        location = "tag://data:contest20"
        #location = "tag://data:implicit_all"

        Create_User_Item_Histogramm().run(input=[location],
                                          map_reader = disco.worker.classic.func.chain_reader,
                                          ).wait(show=True)

        result = self.redis_con.zrevrangebyscore('userHistogramm', float("infinity"), 1, withscores=True, start=0, num=1000)
        print result
        expected = [('604365853', 12.0), ('510716406', 3.0), ('257502743', 2.0), ('604577944', 1.0), ('455735683', 1.0), ('194628326', 1.0)]
        print expected
        self.assertEqual(result, expected)
        print "bla"


    def test_Histogramm_combiner(self):

        location = "tag://data:contesthundred"
        #location = "tag://data:contest20"
        #location = "tag://data:bench_700"
        #location = "tag://data:implicit_all"

        Create_User_Item_Histogramm_combiner().run(input=[location],
                                          map_reader = disco.worker.classic.func.chain_reader,
                                          ).wait(show=True)

        result = self.redis_con.zrevrangebyscore('userHistogramm', float("infinity"), 1, withscores=True, start=0, num=1000)
        print result
        expected = [('604365853', 12.0), ('510716406', 3.0), ('257502743', 2.0), ('604577944', 1.0), ('455735683', 1.0), ('194628326', 1.0)]
        print expected
        #self.assertEqual(result, expected)
        print "bla"





    def test_Histogramm_combiner_partition(self):

        #location = "tag://data:contesthundred"
        #location = "tag://data:contest20"
        #location = "tag://data:bench_700"
        location = "tag://data:implicit_all"

        def my_partition(key, nrp, params):
            #print "partion"
            #print key
            #print nrp
            return int(key) % int(nrp)



        Create_User_Item_Histogramm_combiner().run(input=[location],
                                                   map_reader = disco.worker.classic.func.chain_reader,
                                                   partitions = 26,
                                                   partition = my_partition
                                                   ).wait(show=True)

        result = self.redis_con.zrevrangebyscore('userHistogramm', float("infinity"), 1, withscores=True, start=0, num=1000)
        print result
        expected = [('604365853', 12.0), ('510716406', 3.0), ('257502743', 2.0), ('604577944', 1.0), ('455735683', 1.0), ('194628326', 1.0)]
        print expected
        #self.assertEqual(result, expected)
        print "bla"






