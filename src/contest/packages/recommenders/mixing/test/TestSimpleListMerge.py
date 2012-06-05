from contest.packages.recommenders.mixing.SimpleListMerge import SimpleListMerge

__author__ = 'cw'

import unittest
import redis

from contest.packages.recommenders.Random_Recommender import Random_Recommender


class TestSimpleListMerge(unittest.TestCase):

	debug = True

	def setUp(self):
		self.redis_con = redis.Redis("localhost")
		self.redis_con.flushall()

		userid = 123
		N = 3
		fb = Random_Recommender( )
		additional_filter_1 = { 'domainid' : 'domain1' }
		self.insertRecommendables(additional_filter_1, 0, 10)

		fb.train( userid, additional_filter_1 ) # train for the specific user and the filter



	def insertRecommendables(self, additional_filter, N1, N2):
		fb = Random_Recommender()


		for item_id in xrange(N1,N2):
			fb.set_recommendables( itemid = item_id, additional_filter = additional_filter )

	def testSimpleMergeList(self):

		fb = Random_Recommender( )
		additional_filter_1 = { 'domainid' : 'domain1' }
		userid = 123
		N = 3

		resultSet_1 = fb.get_recommendation( userid, additional_filter_1, N=N, remove = False, ranked = True )
		if self.debug: print resultSet_1

		resultSet_2 = fb.get_recommendation( userid, additional_filter_1, N=N, remove = False, ranked = True )
		if self.debug: print resultSet_2


		slm = SimpleListMerge()
		slm.add('a', resultSet_1)
		slm.add('b', resultSet_2)
		unchanged_list = slm.merge_naive( {'a':0.5, 'b' : 0.5} )

		self.assertEqual(unchanged_list, resultSet_1, "merging two same lists results the same list")




#		resultSet_1 = fb.get_recommendation( userid, additional_filter_1, N=N, remove = True, ranked = True )
#		if self.debug: print resultSet_1
#
#		resultSet_2 = fb.get_recommendation( userid, additional_filter_1, N=N, remove = True, ranked = True )
#		if self.debug: print resultSet_2
#
#
#		slm = SimpleListMerge()
#		slm.add('a', resultSet_1)
#		slm.add('b', resultSet_2)
#		print slm.merge_naive( {'a':0.5, 'b' : 0.5} )


