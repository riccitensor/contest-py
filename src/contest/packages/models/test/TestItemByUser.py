'''
Created on 05.02.2012

@author: christian.winkelmann@plista.com
'''
import unittest
from contest.packages.models.ItemByUser import ItemsByUser
from migrations.setup_keyspaces import Setup_Keyspaces
from contest.config import config_global
from contest.migrations._004_itemsByUserId import ItemByUserId

class TestItemByUser(unittest.TestCase):


    def setUp(self):
        print "setting up database"
        config_global.cassandra_default_keyspace = 'unitTest'
        sK = Setup_Keyspaces() 
        iBI_Model = ItemByUserId()
        


    def tearDown(self):
        pass


    def _testSave(self):
        
        self.saveSome()
        
    def testGet(self):
        self.saveSome()
        
        iBU = ItemsByUser(user_id = 10)
        iBUList = iBU.get()
        
        print iBUList
        
        for key, values in iBUList.items():
            self.assertEquals(values[0], 1, 'wrong entries')
            self.assertEquals(values[1], 2, 'wrong entries')
        
        
    def saveSome(self):
        iBU = ItemsByUser(user_id = 10, timeStamp = 1)                    
        iBU.save( item_id = 1 )
        
        iBU = ItemsByUser(user_id = 10, timeStamp = 1)                    
        iBU.save( item_id = 2 )
        
        iBU = ItemsByUser(user_id = 10, timeStamp = 1)                    
        iBU.save( item_id = 3 )
        
        iBU = ItemsByUser(user_id = 10, timeStamp = 2)                    
        iBU.save( item_id = 4 )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()