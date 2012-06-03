'''
Created on 31.01.2012

@author: christian.winkelmann@plista.com
'''
import unittest
from contest.config import config_global
from contest.config import config_local
import cql
from cql.cassandra import Cassandra
from contest.packages.helper.getTimestamp import getTimestamp
import time
from contest.packages.models.DimensionListModel import DimensionListModel
from contest.migrations.setup_keyspaces import Setup_Keyspaces
from contest.migrations._007_dimensionLists import dimensionListsMigration
from random import uniform


class TestDimensionListModel(unittest.TestCase):
    def setUp(self):
        print "setting up database"
        config_global.cassandra_default_keyspace = 'unitTest'

        sK = Setup_Keyspaces()
        dM = dimensionListsMigration()

        try:
            self.dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port)
            self.cursor = self.dbconn.cursor()

        except:
            print "not able to create a database connection"

        self.cursor.execute("USE " + config_global.cassandra_default_keyspace)

        #config_global.dbname_dimensionList_rowKeys[0]
        #dL = DimensionListModel(config_global.dbname_dimensionList_rowKeys[0])

        print "setting up database done"


    def tearDown(self):
        pass


    def testSaveDimensionListBySeconds(self):
        """ test if the stream of information is written as wished
        """
        dimension = 'user_ids'
        self.dL = DimensionListModel(dimension, 'cassandra')

        timestamp = 4000 # this equals hour 2
        for i in xrange(5):
            curr_timestamp = timestamp + i
            #r = int(uniform(0,1000))
            r = 2
            for user_id in xrange(r):
                self.dL.save(user_id, curr_timestamp)

            print i
        print timestamp
        mylist = self.dL.getByTime(timestamp)

        print "mylist: "
        print mylist
        self.assertEqual(mylist[dimension], u'user_ids_by_seconds_4000', "the entries are not equal")
        self.assertEqual(mylist[0], 0, "the entries are not equal")
        self.assertEqual(len(mylist), 3, "the list has the wrong length")


    def testSaveDimensionListByMinutes(self):
        """ test if the we can save impressions by minute
        """
        dimension = 'user_ids'
        self.dL = DimensionListModel(dimension, 'cassandra')

        timestamp = 0 # this equals hour 2
        for i in xrange(5):
            curr_timestamp = timestamp + i
            #r = int(uniform(0,1000))
            r = 2
            for user_id in xrange(r):
                self.dL.save(user_id, curr_timestamp, 'minutes')

            print i
        print timestamp
        mylist = self.dL.getByTime(timestamp)

        print mylist

        self.assertEqual(mylist['dimension_name'], u'user_ids_by_seconds_4000', "the entries are not equal")
        self.assertEqual(mylist[0], 0, "the entries are not equal")
        self.assertEqual(len(mylist), 3, "the list has the wrong length")

        #dL.save_bin(1, 'hours', binId)



    def save_test_data(self, timestamp_start = 4000, time_stamp_range = 5, id_range = 2):
        """ save some sample data """
        for i in xrange(time_stamp_range):
            curr_timestamp = timestamp_start + i
            for user_id in xrange(id_range):
                self.dL.save(user_id, curr_timestamp)






    def testSaveDimensionListRangeBySeconds(self):
        """ test if the stream of information is written as wished
        """
        dimension = 'user_ids' # save user ids
        self.dL = DimensionListModel(dimension, 'cassandra') # create the model

        timestamp_start = 4000
        time_stamp_range = 50
        id_range = 98

        self.save_test_data(timestamp_start, time_stamp_range, id_range)

        id_stats = self.dL.getByTime(timestamp_start + 1, timestamp_start + 2)
        self.assertEqual(id_stats[u'user_ids_by_seconds_4001'][0], 0, "the entries are not equal")
        self.assertEqual(len(id_stats[u'user_ids_by_seconds_4001']), id_range, "the list has the wrong length")

        desired_length = 5
        id_stats = self.dL.getByTime(timestamp_start, timestamp_start + desired_length)

        self.assertEqual(len(id_stats), desired_length, "the requested list has not {} entries".format(desired_length))





    def testGetDimensionListRangeByMinutes(self):
        """ test if the stream of information is written as wished
        """
        dimension = 'user_ids'
        self.dL = DimensionListModel(dimension, 'cassandra')


        #self.save_test_data(timestamp_start, time_stamp_range, id_range)
        self.dL.save(dimension_id=1, timestamp=59)
        self.dL.save(dimension_id=2, timestamp=59)
        self.dL.save(dimension_id=3, timestamp=59)
        self.dL.save(dimension_id=1, timestamp=61)

        #self.dL.save(dimension_id=1, timestamp=3000)
        #self.dL.save(dimension_id=2, timestamp=3000)
        #self.dL.save(dimension_id=3, timestamp=3000)
        self.dL.save(dimension_id=4, timestamp=3000)

        id_stats = self.dL.getByTime(0, 1, binSize='minutes')
        self.assertEquals(3, len(id_stats[u'user_ids_by_minutes_0']), "wrong length")

        id_stats = self.dL.getByTime(1, 2, binSize='minutes')
        self.assertEquals(1, len(id_stats[u'user_ids_by_minutes_1']), "wrong length")

        id_stats = self.dL.getByTime(0, 2, binSize='minutes')

        self.assertEquals(1, len(id_stats[u'user_ids_by_minutes_1']), "wrong length")
        self.assertEquals(3, len(id_stats[u'user_ids_by_minutes_0']), "wrong length")




        #### hours ####
        id_stats = self.dL.getByTime(0, 1, binSize='hours')
        self.assertEquals(4, len(id_stats[u'user_ids_by_hours_0']), "wrong length")

        self.dL.save(dimension_id=4, timestamp=4000)
        id_stats = self.dL.getByTime(1, 2, binSize='hours', renew=True)
        #print mylist
        self.assertEquals(1, len(id_stats[u'user_ids_by_hours_1']), "wrong length")

        self.dL.save(dimension_id=3, timestamp=4000)
        id_stats = self.dL.getByTime(1, 2, binSize='hours', renew=True)

        self.assertEquals(2, len(id_stats[u'user_ids_by_hours_1']), "wrong length")




        ####### days
        #id_stats = self.dL.getByTime(0, 2, binSize = 'days')
        #print id_stats
        #self.assertEquals(4, len(id_stats[u'user_ids_by_days_0']), "wrong length")

        #print id_stats
        #self.assertEquals(1, len(id_stats), "wrong length")



        # save second based data for hour one
        timestamp_start = 86401
        timestamp_start = 90000
        time_stamp_range = 5
        id_range = 10
        self.save_test_data(timestamp_start, time_stamp_range, id_range)

        id_stats = self.dL.getByTime(0, 2, binSize = 'days')
        self.assertEquals(2, len(id_stats), "wrong length")
        # self.assertEquals(id_range, len(id_stats[u'user_ids_by_days_1']), "wrong length")

        id_stats = self.dL.getByTime(1, 2, binSize = 'days')
        self.assertEquals(1, len(id_stats), "wrong length")
        print id_stats
        #self.assertEquals(id_range, len(id_stats[u'user_ids_by_days_1']), "wrong length")


    def testSetComputedIds(self):
        dimension = 'user_ids'
        dL = DimensionListModel(dimension, mode = 'cassandra')
        rangeStart = 0
        rangeEnd = 10
        binSize = 'minutes'
        dL.setComputedIds(dimension, rangeStart, rangeEnd, binSize)

        r = dL.getComputedIds(dimension, rangeStart, rangeEnd, binSize)
        print r
        self.assertEqual(rangeEnd, len(r) )


        rangeEnd = 5
        binSize = 'hours'
        r = dL.getComputedIds(dimension, rangeStart, rangeEnd, binSize)
        """ nothing is yet computed for hours """
        self.assertEqual(0, len(r) )

        dL.setComputedIds(dimension, rangeStart, rangeEnd, binSize)
        r = dL.getComputedIds(dimension, rangeStart, rangeEnd, binSize)
        print r
        self.assertEqual(rangeEnd, len(r) )




    def testBinify(self):
        """ this function has a stupid name, but will get data from one dimensionList an will aggregate it
        """
        self.dL = DimensionListModel('user_ids', mode='cassandra')
        timestamp = 1

        for i in xrange(58, 61):
            for user_id in xrange(int(uniform(1, 6))):
                curr_timestamp = i
                self.dL.save(user_id, curr_timestamp)

        list = self.dL.getByTime(45, 75, 'seconds')
        #self.dL.getByTime(timestampStart, timestampEnd, binSize)

        #print list
        """ save the data """
        binified = self.dL.binify('minutes', 0, 1)
        print binified
        binified = self.dL.binify('minutes', 1, 2)
        print binified


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()