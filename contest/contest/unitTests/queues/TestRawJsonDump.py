'''
Created on 30.12.2011

@author: christian.winkelmann@plista.com
'''
import unittest
from contest.packages.rabbitMQ.algorithm.storage import rawJsonDump
import time
import random


class TestRawJsonDump(unittest.TestCase):

    def setUp(self):
        """ @todo: instead of flushing all databased it would be better to simply overwrite the database location
        """
        from contest.config import config_local
        import redis
        redis_con = redis.Redis(config_local.config_redis_server_basic)
        redis_con.flushall()


    def tearDown(self):
        pass


    def testEnqueSavingADump(self):
        raw = rawJsonDump.rawJsonDump()
        msg = "_body"
        return_msg = raw.enqueue(msg) # enqeuing the task and allowing to compute the result remotely
        self.assertEqual(msg, return_msg, "something went wrong in testEnqueSavingADump")
    
    def testEnqueSavingAndRetrievingADump(self):
        
        
        raw = rawJsonDump.rawJsonDump()
        msg = "_body"
        raw.enqueue(msg) # enqeuing the task and allowing to compute the result remoteley
        
        time.sleep(0.5) # half a second should be enough to finish the work
        return_msg = raw.fetchAll()
        
        self.assertEqual(type(return_msg), type(dict()), "the return message is not a dictionary")
        self.assertEqual(len(return_msg), 1, "the return message is longer then expected")
        
        msg = "blakeks"
        raw.enqueue(msg) # enqeuing the task and allowing to compute the result remoteley
        time.sleep(0.5) # half a second should be enough to finish the work
        return_msg = raw.fetchAll()
        self.assertEqual(len(return_msg), 2, "the return message is longer or shorter then expected")
        
        return_msg = raw.fetchN(1)
        #print return_msg
        self.assertEqual(len(return_msg), 1, "the return message is longer or shorter then expected")

        return_msg = raw.fetchN(2)
        #print return_msg
        self.assertEqual(len(return_msg), 2, "the return message is longer or shorter then expected")

    def testEnqueNImpressions(self):
        raw = rawJsonDump.rawJsonDump()
        for i in xrange(300):
            msg = random.uniform(0,1000000000000000000000000000000)
            msg = str(msg)
            raw.enqueue(msg) # enqeuing the task and allowing to compute the result remoteley
        
        time.sleep(0.5)
        
        return_msg = raw.fetchN(100)
        #self.assertEqual(len(return_msg), 100, "the return message is longer or shorter then expected and is: " + str(len(return_msg)))
        
        
    def testFetchFromFile(self):
        raw = rawJsonDump.rawJsonDump()
        raw.flush_log()
        
        msg = "message 1"
        raw.enqueue(msg) # enqeuing the task and allowing to compute the result remoteley
        
        msg = "message 2"
        raw.enqueue(msg) # enqeuing the task and allowing to compute the result remoteley
        # raw.saveToFile(12345, "bla")
        time.sleep(0.5) # half a second should be enough to finish the work
        #raw.saveToFile()
        return_msg = raw.fetchN_fromFile(4)
        print return_msg
        
        # self.assertEqual(len(return_msg), 2, "the return message is longer or shorter then expected")

        #raw.flush_log()
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    
    
    