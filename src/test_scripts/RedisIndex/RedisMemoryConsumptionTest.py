'''
Created on 09.02.2012

testing memory consumption of redis

just in case do a "redis-cli flushall beforehand

@author: cw@plista.com
'''
import unittest
from random import random


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testFillRedis(self):
        """ test how much redis SETS consume with its memory
        redis-cli info | grep used_memory
        """
        import redis
        import random
        
        redis_con = redis.Redis("localhost")

        prefix = "fdid:"
        id_count = 200 # number of sets
        index_entry_length = 200 # number of values in each set

        print "writing {0:2d} sets with {1:4d} values each into redis".format(id_count, index_entry_length)
        for id in xrange(id_count):
            for i in xrange(index_entry_length):
                value = int(i) ## define the payload
                primary_key = str(prefix + str(id))
                redis_con.sadd(primary_key, value)
                
        print "done, writing {0:4d} values at all into redis.".format(id_count * index_entry_length)        
        
        #print redis_con.scard(primary_key)
        self.assertEqual(redis_con.scard(primary_key), index_entry_length, "wrong amount of values in the set")
        self.assertEqual(redis_con.scard(str(prefix + str(5))), index_entry_length, "wrong amount of values in the set")


if __name__ == "__main__":
    unittest.main()
