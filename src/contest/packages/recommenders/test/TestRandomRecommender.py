'''
Created on 23.05.2012

@author: christian.winkelmann@plista.com
'''
import unittest
from contest.packages.recommenders.Random_Recommender import Random_Recommender


class TestRandomRecommender(unittest.TestCase):


	def setUp(self):
		self.insertData()


	def tearDown(self):
		pass

	def insertData(self):
		''' '''

	def test_Get_Recommendation(self):
		userid = 123
		N = 3
		fb = Random_Recommender( userid )
	
		## todo replace this with a writeback utility	
		for item_id in xrange(15):
			fb.set_recommendables( itemid = item_id )
		
		
		fb.train( )
		
		resultSet_old = fb.get_recommendation( N=N, remove = False )
		print resultSet_old
		self.assertEqual(len(resultSet_old), N, 'the resulting recommendation have the wrong number')
		
		resultSet_new = fb.get_recommendation( N=N, remove = True )
		print resultSet_new
		self.assertEqual(len(resultSet_new), N, 'the resulting recommendation have the wrong number')
		self.assertEqual( resultSet_new, resultSet_old, 'the resultsets are not the same')
		
		resultSet_newest = fb.get_recommendation( N=N, remove = True )
		print resultSet_newest
		self.assertEqual( len(resultSet_newest), N, 'the resulting recommendation have the wrong number')
		self.assertNotEqual( resultSet_newest, resultSet_new, 'the resultsets are the same')



if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()