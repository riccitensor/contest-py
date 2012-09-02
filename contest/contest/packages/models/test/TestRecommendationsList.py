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
	debug = True

	def setUp(self):
		'''
		'''
		
	def setUp_cassandra(self):
		config_global.cassandra_default_keyspace = 'unitTest'
		sK = Setup_Keyspaces() 
		rM = recommendationListMigration()
		

	def tearDown(self):
		pass


	def testSaveRecommendations_redis_ranked(self):
		rL = RecommendationList(mode='redis')
		
		testDict = {'b' : 1, 'a' : 5, 'c' : 0} # just a dictionary
		testDict2 = (('b',1), ('c', 0), ('a', 5)) # an ordered tuple with nested tuples
		testDict3 = [('b',1), ('c', 0), ('a', 5)] # an ordered list with nested tuplse

		key = 'user_test_key1'
		N = 3
		rL.save(key, testDict)
		res = rL.get(key, N)
		self.assertEqual(res[0], ('a', 5), "the result is wrong")
		if self.debug : print res

		key = 'user_test_key2'
		rL.save(key, testDict2)
		res = rL.get(key, N)
		if self.debug : print res
		self.assertEqual(res[0], ('a', 5), "the result is wrong")
		
		key = 'user_test_key3'
		rL.save(key, testDict3)
		res = rL.get(key, N)
		if self.debug : print res
		self.assertEqual(res[0], ('a', 5), "the result is wrong")




	''' this is not necessary because the only unranked case might be the random recommender sofar '''
	'''
	def testSaveRecommendations_redis_unranked(self):
		rL = RecommendationList(mode='redis')

		testList = ['a', 'b', 'c', 'd']

		key = 'user_test_key1'
		N = 3
		rL.save(key, testList)
		res = rL.get(key, N)
		self.assertEqual(res[0], ('a'), "the result is wrong")
		self.assertEqual(res[1], ('b'), "the result is wrong")
	'''

		
	def _testSaveRecommendations_cassandra(self):
		self.setUp_cassandra()
		
		rL = RecommendationList(mode='cassandra')
		
		pass	
	
	def testGetRecommendations(self):
		pass


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()