'''
Created on 23.05.2012

@author: christian.winkelmann@plista.com
'''
import unittest
from contest.packages.recommenders.fallback_random import fallback_random


class TestRandomRecommender(unittest.TestCase):


	def setUp(self):
		self.insertData()


	def tearDown(self):
		pass

	def insertData(self):
		''' '''

	def testName(self):
		userid = 123
		fb = fallback_random( userid )
	
		## todo replace this with a writeback utility	
		fb.set_recommendables( itemid = 6 )
		fb.set_recommendables( itemid = 7 )
		fb.set_recommendables( itemid = 8 )
		fb.set_recommendables( itemid = 9 )
		fb.set_recommendables( itemid = 10 )
		fb.set_recommendables( itemid = 11 )
		fb.set_recommendables( itemid = 12 )
		fb.set_recommendables( itemid = 13 )
		
		fb.train( userid, 5 )
		
		resultSet = fb.get_recommendation( N=3 )
		print 'result'
		print resultSet
		#fb.del_recommendables(12345)
		#fb.del_recommendables(67890)


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()