import unittest
import redis
from contest.packages.recommenders.Random_Recommender import Random_Recommender


class TestRandomRecommenderWorker(unittest.TestCase):



    def setUp(self):
        pass
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







if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
