'''
Created on 21.05.2012

@author: christian.winkelmann@plista.com
'''
import unittest
from contest.packages.models.RecommendationList import RecommendationList
from contest.migrations._008_recommendationsList import recommendationListMigration
from contest.migrations.setup_keyspaces import Setup_Keyspaces
from contest.config import config_global


class TestRecommendationsList(unittest.TestCase):


	def setUp(self):
		print "set up"
		
	def setUp_cassandra(self):
		config_global.cassandra_default_keyspace = 'unitTest'
		sK = Setup_Keyspaces() 
		rM = recommendationListMigration()
		

	def tearDown(self):
		pass


	def testSaveRecommendations_redis(self):
		rL = RecommendationList(mode='redis')
		
		testDict = {'b' : 1, 'a' : 5, 'c' : 0}
		
		testDict2 = (('b',1), ('c', 0), ('a', 5))
		
		testDict3 = [('b',1), ('c', 0), ('a', 5)]
		#print unsortedSet[0]
		key = 'user_test_key1'
		N = 3
		rL.save(key, testDict)
		res = rL.get(key, N)
		self.assertEqual(res[0], ('a', 5), "the result is wrong") 
		
		key = 'user_test_key2'
		rL.save(key, testDict2)
		res = rL.get(key, N)
		self.assertEqual(res[0], ('a', 5), "the result is wrong")
		
		key = 'user_test_key3'
		rL.save(key, testDict3)
		res = rL.get(key, N)
		self.assertEqual(res[0], ('a', 5), "the result is wrong")
		
		
	def _testSaveRecommendations_cassandra(self):
		self.setUp_cassandra()
		
		rL = RecommendationList(mode='cassandra')
		
		pass	
	
	def testGetRecommendations(self):
		pass


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()