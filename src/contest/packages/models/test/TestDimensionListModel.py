'''
Created on 31.01.2012

@author: karisu
'''
import unittest
from config import config_global
from config import config_local
import cql
from cql.cassandra import Cassandra
from packages.helper.getTimestamp import getTimestamp
import time
from packages.models.DimensionListModel import DimensionListModel
from migrations.setup_keyspaces import Setup_Keyspaces
from migrations._007_dimensionLists import dimensionListsMigration
from random import uniform


class TestDimensionListModel(unittest.TestCase):



    def setUp(self):
        print "setting up database"
        config_global.cassandra_default_keyspace = 'unitTest'
        
        sK = Setup_Keyspaces()
        dM = dimensionListsMigration()
        
        try:
            self.dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port ) 
            self.cursor = self.dbconn.cursor()
    
        except:
            print "not able to create a database connection"
    
        self.cursor.execute("USE " + config_global.cassandra_default_keyspace)
    
        #config_global.dbname_dimensionList_rowKeys[0]
        #dL = DimensionListModel(config_global.dbname_dimensionList_rowKeys[0])
        
        print "setting up database done"
    



    def tearDown(self):
        pass


    def _testSaveDimensionListBySeconds(self):
        """ test if the stream of information is written as wished
        """
        dimension = 'user_ids'
        self.dL = DimensionListModel( dimension )

        
        timestamp = 4000 # this equals hour 2
        for i in xrange(5):
            curr_timestamp = timestamp + i
            #r = int(uniform(0,1000))
            r = 2
            for user_id in xrange(r):    
                self.dL.save( user_id, curr_timestamp )
            
            print i
        print timestamp
        mylist = self.dL.getByTime(timestamp)
        
        
        self.assertEqual(mylist['dimension_name'], u'user_ids_by_seconds_4000', "the entries are not equal")    
        self.assertEqual(mylist[0], 0 , "the entries are not equal")
        self.assertEqual(len( mylist ), 3, "the list has the wrong length")
    

    def _testSaveDimensionListByMinutes(self):
        """ test if the we can save impressions by minute
        """
        dimension = 'user_ids'
        self.dL = DimensionListModel( dimension )

        
        timestamp = 0 # this equals hour 2
        for i in xrange(5):
            curr_timestamp = timestamp + i
            #r = int(uniform(0,1000))
            r = 2
            for user_id in xrange(r):    
                self.dL.save( user_id, curr_timestamp, 'minutes' )
            
            print i
        print timestamp
        mylist = self.dL.getByTime(timestamp)
        
#        print mylist
        
        self.assertEqual(mylist['dimension_name'], u'user_ids_by_seconds_4000', "the entries are not equal")    
        self.assertEqual(mylist[0], 0 , "the entries are not equal")
        self.assertEqual(len( mylist ), 3, "the list has the wrong length")
        
        #dL.save_bin(1, 'hours', binId)




    def _testSaveDimensionListRangeBySeconds(self):
        """ test if the stream of information is written as wished
        """
        dimension = 'user_ids'
        self.dL = DimensionListModel( dimension )

        
        timestamp = 4000 # this equals hour 2
        for i in xrange(5):
            curr_timestamp = timestamp + i
            #r = int(uniform(0,1000))
            r = 2
            for user_id in xrange(r):    
                self.dL.save( user_id, curr_timestamp )
            
            print i
        print timestamp
        mylist = self.dL.getByTime(timestamp+1, timestamp+2)
        
#        print mylist
        
        self.assertEqual(mylist[u'user_ids_by_seconds_4001'][0], 0, "the entries are not equal")    

        self.assertEqual( len( mylist[u'user_ids_by_seconds_4001'] ), 2, "the list has the wrong length")
        
        #dL.save_bin(1, 'hours', binId)
        


    def testGetDimensionListRangeByMinutes(self):
        """ test if the stream of information is written as wished
        """
        dimension = 'user_ids'
        self.dL = DimensionListModel( dimension )

        self.dL.save( dimension_id = 1, timestamp = 59 )
        self.dL.save( dimension_id = 2, timestamp = 59 )
        self.dL.save( dimension_id = 3, timestamp = 59 )
        self.dL.save( dimension_id = 1, timestamp = 61 )
        
        self.dL.save( dimension_id = 1, timestamp = 3000)
        self.dL.save( dimension_id = 2, timestamp = 3000)
        self.dL.save( dimension_id = 3, timestamp = 3000)
        self.dL.save( dimension_id = 4, timestamp = 3000)
        
        
        mylist = self.dL.getByTime(0, 1, binSize = 'minutes')
        self.assertEquals(3, len(mylist[u'user_ids_by_minutes_0']), "wrong length")
        
        mylist = self.dL.getByTime(1, 2, binSize = 'minutes')
        self.assertEquals(1, len(mylist[u'user_ids_by_minutes_1']), "wrong length")
        
        mylist = self.dL.getByTime(0, 2, binSize = 'minutes')
        #print mylist
        self.assertEquals(1, len(mylist[u'user_ids_by_minutes_1']), "wrong length")
        self.assertEquals(3, len(mylist[u'user_ids_by_minutes_0']), "wrong length")
        
        
        mylist = self.dL.getByTime(0, 1, binSize = 'hours')
        #print mylist
        self.assertEquals(4, len(mylist[u'user_ids_by_hours_0']), "wrong length")
        
        self.dL.save( dimension_id = 4, timestamp = 4000)
        mylist = self.dL.getByTime(1, 2, binSize = 'hours', renew=True)
        #print mylist
        self.assertEquals(1, len(mylist[u'user_ids_by_hours_1']), "wrong length")
        
        self.dL.save( dimension_id = 3, timestamp = 4000)
        mylist = self.dL.getByTime(1, 2, binSize = 'hours', renew=True)
        #print mylist
        self.assertEquals(2, len(mylist[u'user_ids_by_hours_1']), "wrong length")
        
        #mylist = self.dL.getByTime(0, 2, binSize = 'days')
        #print mylist
        #self.assertEquals(4, len(mylist[u'user_ids_by_days_0']), "wrong length")
        
        #print mylist
        #self.assertEquals(5, len(mylist), "wrong length")
        #print mylist


    def _testSetComputedIds(self):
        dimension = 'user_ids'
        dL = DimensionListModel( dimension )
        rangeStart = 0
        rangeEnd = 10
        binSize = 'minutes'
        dL.setComputedIds(dimension, rangeStart, rangeEnd, binSize)

        r = dL.getComputedIds(dimension, rangeStart, rangeEnd, binSize)
        print r
        
        rangeStart = 0
        rangeEnd = 10
        binSize = 'hours'
        dL.setComputedIds(dimension, rangeStart, rangeEnd, binSize)
        r = dL.getComputedIds(dimension, rangeStart, rangeEnd, binSize)
        print r
        

            
        
    def _testGetHourFromTimeStamp(self):
        """ @todo: move this into a seperate unit Test for the getTimestamp Class but for now it is perfect here
        """
        timestamp = 4000
        binId = getTimestamp.gettimeStampIn_Hours( timestamp )
        self.assertEqual(binId, 1, "the conversion from timestamp to hour is wrong")
        
    def _testGetTimestampFromHour(self):
        hour = 1
        timestamp = getTimestamp.getTimeStampFromHours(hour)
        self.assertEqual(timestamp, 3601, "the conversion from timestamp to hour is wrong")
    
    
    
    def _testBinify(self):
        """ this function has a stupid name, but will get data from one dimensionList an will aggregate it
        """
        self.dL = DimensionListModel('user_ids')
        timestamp = 1
   
    
        for i in xrange( 58, 61 ):
            for user_id in xrange( int( uniform(1,6)) ):
            
            
                curr_timestamp = i
                self.dL.save( user_id, curr_timestamp )
        
        
        list = self.dL.getByTime(45, 75, 'seconds')
        #self.dL.getByTime(timestampStart, timestampEnd, binSize)

        print list
        """ save the data """
        self.dL.binify('minutes', 0, 1)
        self.dL.binify('minutes', 1, 2)
        
        
        
    
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()