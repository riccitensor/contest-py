'''
Created on 05.02.2012

test the counters

@author: christian.winkelmann@plista.com
'''
import unittest
from contest.packages.models.distributedCounters import distributedCounters
from contest.migrations.setup_keyspaces import Setup_Keyspaces
from contest.config import config_global
import contest.migrations
from contest.migrations._006_distributedCountersMigration import DistributedCountersMigration


class TestdistributedCounters(unittest.TestCase):


    def setUp(self):
        print "setting up database"
        config_global.cassandra_default_keyspace = 'unitTest'
        sK = Setup_Keyspaces() 
        dM = DistributedCountersMigration()
        
        flattenedJson =  {'item_url': u'http://www.ksta.de/html/fotolines/1317623400963/rahmen.shtml?1', 
 'item_recommendable': True, 'item_title': u'Die Hoch\xadzeit der Herzogin von Alba', 'item_created': 
 1318402695, 'impression_id': 100001, 'item_id': u'51079963', 'config_recommend': True, 'client_id': 
 49217133, 'msg': u'impression', 'domain_id': u'418'}
        
        self.dC = distributedCounters( flattenedJson, timestamp = 1 )
        

    def tearDown(self):
        pass


    def testGetMostImportant(self):
        flattenedJson =  {'item_created': 
 1318402695, 'impression_id': 100001, 'item_id': u'1', 'config_recommend': True, 'client_id': 
 10, 'msg': u'impression' }
        dC = distributedCounters(flattenedJson, 1)
        dC.increment_by_collumn()
           
        """ user id 1 """                     
        flattenedJson =  {'item_created': 
 1318402696, 'impression_id': 100002, 'item_id': u'2', 'config_recommend': True, 'client_id': 
 10, 'msg': u'impression' }
        dC = distributedCounters(flattenedJson, 2)
        dC.increment_by_collumn()
        
        
        """ user id 2 """
        flattenedJson =  {'item_created': 
 1318402697, 'impression_id': 100002, 'item_id': u'2', 'config_recommend': True, 'client_id': 
 20, 'msg': u'impression' }
        dC = distributedCounters(flattenedJson, 2)
        dC.increment_by_collumn()
        
        flattenedJson =  {'item_created': 
 1318402698, 'impression_id': 100002, 'item_id': u'2', 'config_recommend': True, 'client_id': 
 20, 'msg': u'impression'}
        dC = distributedCounters(flattenedJson, 2)
        dC.increment_by_collumn()
        
        flattenedJson =  {'item_created': 
 1318402698, 'impression_id': 100002, 'item_id': u'2', 'config_recommend': True, 'client_id': 
 20, 'msg': u'impression'}
        dC = distributedCounters(flattenedJson, 2)
        dC.increment_by_collumn()
        
        flattenedJson =  {'item_created': 
 1318402698, 'impression_id': 100002, 'item_id': u'2', 'config_recommend': True, 'client_id': 
 30, 'msg': u'impression'}
        dC = distributedCounters(flattenedJson, 2)
        dC.increment_by_collumn()
        
        
        
        flattenedJson =  {'item_created': 
 1318402696, 'impression_id': 100002, 'item_id': u'2', 'config_recommend': True, 'client_id': 
 2, 'msg': u'impression', 'domain_id': u'418'}
        dC = distributedCounters(flattenedJson, 4000)
        dC.increment_by_collumn()
        
        
        
        dimension = 'user_ids'
        binSize = 'minutes'
        timestampFrom = 0
        #print "most important"
        #print self.dC.getMostImportant(dimension, binSize, timestampFrom)
        
        dimension = 'user_ids'
        binSize = 'minutes'
        timestampFrom = 0
        timestampTo = 5
        print "most important"
        print self.dC.getMostImportant(dimension, binSize, timestampFrom, timestampTo)
        
        
        dimension = 'user_ids'
        binSize = 'hours'
        timestampFrom = 0
        print "most important"
        print self.dC.getMostImportant(dimension, binSize, timestampFrom)
        
        
        dimension = 'user_ids'
        binSize = 'hours'
        timestampFrom = 0
        timestampTo = 2
        print "most important"
        print self.dC.getMostImportant(dimension, binSize, timestampFrom, timestampTo)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()