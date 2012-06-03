'''
Created on 31.01.2012

@author: christian.winkelmann@plista.com
'''
import unittest
import cql
from random import uniform

from contest.config import config_global
from contest.config import config_local
from contest.packages.models.DimensionListModel import DimensionListModel
from contest.migrations.setup_keyspaces import Setup_Keyspaces
from contest.migrations._007_dimensionLists import dimensionListsMigration



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


        print "setting up database done"



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

        self.dL.save(dimension_id=1, timestamp=59)
        self.dL.save(dimension_id=2, timestamp=59)
        self.dL.save(dimension_id=3, timestamp=59)
        self.dL.save(dimension_id=1, timestamp=61)
        self.dL.save(dimension_id=4, timestamp=3000)

        id_stats = self.dL.getByTime(0, 1, binSize='minutes')
        self.assertEquals(3, len(id_stats[u'user_ids_by_minutes_0']), "wrong length")

        id_stats = self.dL.getByTime(1, 2, binSize='minutes')
        self.assertEquals(1, len(id_stats[u'user_ids_by_minutes_1']), "wrong length")

        id_stats = self.dL.getByTime(0, 2, binSize='minutes')

        self.assertEquals(1, len(id_stats[u'user_ids_by_minutes_1']), "wrong length")
        self.assertEquals(3, len(id_stats[u'user_ids_by_minutes_0']), "wrong length")


    def testGetDimensionListRangeByHours(self):
        """ test if the stream of information is written as wished
        """
        dimension = 'user_ids'
        self.dL = DimensionListModel(dimension, 'cassandra')

        self.dL.save(dimension_id=1, timestamp=59)
        self.dL.save(dimension_id=2, timestamp=59)
        self.dL.save(dimension_id=3, timestamp=59)
        self.dL.save(dimension_id=1, timestamp=61)
        self.dL.save(dimension_id=4, timestamp=3000)


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


    def testGetDimensionListRangeByDay(self):
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




    def test_Binify_Minutes(self):
        """ this function has a stupid name, but will get data from one dimensionList an will aggregate it
        """
        self.dL = DimensionListModel('user_ids', mode='cassandra')
        binSize = 'minutes'

        start_seconds = 58
        end_seconds = 61
        for i in xrange(start_seconds, end_seconds):
            for user_id in xrange(int(uniform(1, 6))):
                curr_timestamp = i
                self.dL.save(user_id, curr_timestamp)

        list = self.dL.getByTime(45, 75, 'seconds')
        #self.dL.getByTime(timestampStart, timestampEnd, binSize)

        #print list
        """ save the data """
        binified = self.dL.binify(binSize, 0, 1)
        print binified
        self.assertIn(u'user_ids_by_seconds_58', binified)
        self.assertIn(u'user_ids_by_seconds_59', binified)
        self.assertNotIn(u'user_ids_by_seconds_60', binified)

        binified = self.dL.binify(binSize, 1, 2)
        self.assertNotIn(u'user_ids_by_seconds_58', binified)
        self.assertNotIn(u'user_ids_by_seconds_59', binified)
        self.assertIn(u'user_ids_by_seconds_60', binified)
        print binified

    def test_Binify_Hours(self):
        """ this function has a stupid name, but will get data from one dimensionList an will aggregate it
        """
        self.dL = DimensionListModel('user_ids', mode='cassandra')
        binSize = 'hours'

        start_seconds = 58
        end_seconds = 61
        for i in xrange(start_seconds, end_seconds):
            for user_id in xrange(int(uniform(1, 6))):
                curr_timestamp = i
                self.dL.save(user_id, curr_timestamp)

        start_seconds = 3600
        end_seconds = start_seconds + 1
        for i in xrange(start_seconds, end_seconds):
            for user_id in xrange(int(uniform(1, 6))):
                curr_timestamp = i
                self.dL.save(user_id, curr_timestamp)


        binified = self.dL.binify(binSize, 1, 2)
        self.assertIn(u'user_ids_by_seconds_3600', binified)


        binified = self.dL.binify(binSize, 0, 1)
        print binified
        self.assertIn(u'user_ids_by_seconds_58', binified)
        self.assertIn(u'user_ids_by_seconds_59', binified)
        self.assertIn(u'user_ids_by_seconds_60', binified)
        self.assertNotIn(u'user_ids_by_seconds_3600', binified)



    def test_Binify_Days(self):
        """ this function has a stupid name, but will get data from one dimensionList an will aggregate it
        """
        self.dL = DimensionListModel('user_ids', mode='cassandra')
        binSize = 'days'

        start_seconds = 58
        end_seconds = 61
        for i in xrange(start_seconds, end_seconds):
            for user_id in xrange(int(uniform(1, 6))):
                curr_timestamp = i
                self.dL.save(user_id, curr_timestamp)

        start_seconds = 86400
        end_seconds = start_seconds + 1
        for i in xrange(start_seconds, end_seconds):
            for user_id in xrange(int(uniform(1, 6))):
                curr_timestamp = i
                self.dL.save(user_id, curr_timestamp)

        """ save the data """
        binified = self.dL.binify(binSize, 0, 1)
        print binified
        self.assertIn(u'user_ids_by_seconds_58', binified)
        self.assertIn(u'user_ids_by_seconds_59', binified)
        self.assertIn(u'user_ids_by_seconds_60', binified)
        self.assertNotIn(u'user_ids_by_seconds_86400', binified)

        binified = self.dL.binify(binSize, 1, 2)
        self.assertIn(u'user_ids_by_seconds_86400', binified)


        binified = self.dL.binify(binSize, 0, 2)
        print binified
        self.assertIn(u'user_ids_by_seconds_58', binified)
        self.assertIn(u'user_ids_by_seconds_59', binified)
        self.assertIn(u'user_ids_by_seconds_60', binified)
        self.assertIn(u'user_ids_by_seconds_86400', binified)


    def _test_Binify_Performance(self):
        """ this function has a stupid name, but will get data from one dimensionList an will aggregate it
        """
        self.dL = DimensionListModel('user_ids', mode='cassandra')
        binSize = 'days'

        start_seconds = 58
        end_seconds = 90000
        for i in xrange(start_seconds, end_seconds):
            for user_id in xrange(int(uniform(1, 6))):
                curr_timestamp = i
                self.dL.save(user_id, curr_timestamp)


        """ save the data """
        binified = self.dL.binify(binSize, 0, 1)
        print binified
        self.assertIn(u'user_ids_by_seconds_58', binified)
        self.assertIn(u'user_ids_by_seconds_59', binified)
        self.assertIn(u'user_ids_by_seconds_60', binified)
        self.assertNotIn(u'user_ids_by_seconds_86400', binified)

        binified = self.dL.binify(binSize, 1, 2)
        self.assertIn(u'user_ids_by_seconds_86400', binified)




if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()