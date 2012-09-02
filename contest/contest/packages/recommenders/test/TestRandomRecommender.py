'''
Created on 23.05.2012

@author: christian.winkelmann@plista.com
'''
import unittest
import redis

from contest.packages.recommenders.Random_Recommender import Random_Recommender


class TestRandomRecommender(unittest.TestCase):

	debug = True

	def setUp(self):
		self.redis_con = redis.Redis("localhost")
		self.redis_con.flushall()



	def tearDown(self):
		pass


	def insertRecommendables(self, additional_filter, N1, N2):
		fb = Random_Recommender()


		for item_id in xrange(N1,N2):
			fb.set_recommendables( itemid = item_id, additional_filter = additional_filter )

	def test_get_recommendable_item(self):
		fb = Random_Recommender()

		# inserting two items for domain1
		fb.set_recommendables( 1, { 'domainid' : 'domain1' } )
		fb.set_recommendables( 2, { 'domainid' : 'domain1' } )
		g = fb.get_recommendable_item( { 'domainid' : 'domain1' } )

		self.assertIn(int(g), (1,2), "fetched wrong recommendable item")

		# for this domain there is no way of recommending anything, because we don't have any items
		g = fb.get_recommendable_item( { 'domainid' : 'domain2' } )
		self.assertIsNone(g, "fetched wrong recommendable item")


	def test_Get_Recommendation_with_constraint(self):
		userid = 123
		N = 3
		fb = Random_Recommender( )
		additional_filter_1 = { 'domainid' : 'domain1' }
		self.insertRecommendables(additional_filter_1, 0, 10)

		additional_filter_2 = { 'domainid' : 'domain2' }
		self.insertRecommendables(additional_filter_2, 20, 30)

		self.insertRecommendables({}, 20, 30)

		fb.train( userid, additional_filter_1 ) # train for the specific user and the filter

		resultSet_1 = fb.get_recommendation( userid, additional_filter_1, N=N, remove = False )
		if self.debug: print resultSet_1
		self.assertEqual(len(resultSet_1), N, 'the resulting recommendation have the wrong number')


		resultSet_2 = fb.get_recommendation( userid, additional_filter_2, N=N, remove = False )
		self.assertEqual(len(resultSet_2), 0, 'the resulting recommendation have the wrong number')

		resultSet_new = fb.get_recommendation( userid, {}, N=N, remove = True )
		self.assertEqual(len(resultSet_new), 0, 'the resulting recommendation have the wrong number')

		fb.train( userid, {} ) # train for the specific user but with no constraint, meaning we can recommend everything
		resultSet_new = fb.get_recommendation( userid, {}, N=N, remove = True, ranked=True )
		if self.debug: print resultSet_new
		self.assertEqual(len(resultSet_new), N, 'the resulting recommendation have the wrong number')


		resultSet_new_1 = fb.get_recommendation( userid, {}, N=N, remove = True, ranked=True )
		if self.debug: print resultSet_new_1
		self.assertEqual(len(resultSet_new_1), N, 'the resulting recommendation have the wrong number')

		self.assertNotEqual(resultSet_new_1,resultSet_new, 'items were not removed from the recommendation Set')



	def test_Get_Recommendation_Ranked(self):
		userid = 123
		N = 3
		fb = Random_Recommender( )
		additional_filter_1 = { 'domainid' : 'domain1' }
		self.insertRecommendables(additional_filter_1, 0, 10)

		additional_filter_2 = { 'domainid' : 'domain2' }
		self.insertRecommendables(additional_filter_2, 20, 30)

		self.insertRecommendables({}, 20, 30)

		fb.train( userid, additional_filter_1 ) # train for the specific user and the filter

		resultSet_1 = fb.get_recommendation( userid, additional_filter_1, N=N, remove = False, ranked = True )
		if self.debug: print resultSet_1
		self.assertEqual(len(resultSet_1), N, 'the resulting recommendation have the wrong number')




	def test_Get_Recommendation_with_multiple_constraints(self):
		userid = 123
		N = 3
		fb = Random_Recommender( )
		additional_filter_1 = { 'domainid' : 'domain1', 'channelid' : 'channel1' }
		self.insertRecommendables(additional_filter_1, 0, 10)

		fb.train( userid, additional_filter_1 ) # train for the specific user and the filter

		resultSet_1 = fb.get_recommendation(userid, additional_filter_1, N=N, remove = False )
		if self.debug: print resultSet_1
		self.assertEqual(len(resultSet_1), N, 'the resulting recommendation have the wrong number')


	def test_Get_Recommendation_userid_disctinction(self):

		N = 3
		fb = Random_Recommender( )
		additional_filter_1 = { 'domainid' : 'domain1' }

		userid1 = 123
		self.insertRecommendables(additional_filter_1, 0, 10)
		fb.train( userid1, additional_filter_1 ) # train for the specific user and the filter
		userid2 = 456
		self.insertRecommendables(additional_filter_1, 0, 10)
		fb.train( userid2, additional_filter_1 ) # train for the specific user and the filter

		resultSet_1 = fb.get_recommendation( userid1, additional_filter_1, N=N, remove = False )
		if self.debug: print resultSet_1
		self.assertEqual(len(resultSet_1), N, 'the resulting recommendation have the wrong number')
		resultSet_2 = fb.get_recommendation( userid2, additional_filter_1, N=N, remove = False )
		if self.debug: print resultSet_2
		self.assertEqual(len(resultSet_2), N, 'the resulting recommendation have the wrong number')


	def test_compute_key(self):

		additional_filter = { }
		fb = Random_Recommender()

		full_key = fb.compute_key( additional_filter )

		self.assertEqual(fb.itemList , full_key, "the key constraints are wrong")

		a = 'domainid'
		b = 'domain2'
		additional_filter = { a : b }
		fb = Random_Recommender()

		full_key = fb.compute_key( additional_filter )

		self.assertEqual(fb.itemList + ':' + a + ':' + b, full_key, "the key constraints are wrong")


		a = 'domainid'
		b = 'domain2'
		c = 'categoryid'
		d = 'category1'
		additional_filter = { a : b, c : d }
		fb = Random_Recommender()

		full_key = fb.compute_key( additional_filter )


		self.assertEqual(fb.itemList + ':' + a + ':' + b  + ':' + c + ':' + d, full_key, "the key constraints are wrong")





if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()