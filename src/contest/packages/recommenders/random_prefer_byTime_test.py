'''
Created on 02.12.2011

@author: karisu
'''
import unittest
import time

from contest.packages.recommenders.random_prefer_base import random_prefer_base
from contest.packages.statistics import histogramm

class random_prefer_base_test(unittest.TestCase):


    def setUp(self):
        random_prefer_newer_recommender = random_prefer_base(preference=0, maximum_age = 259200)
        timestamp = time.time()
        
        #random_prefer_newer_recommender.set_recommendables("newest3", timestamp-10)
        for i in xrange(2*24): #4 days and two new items per hour
            # the higher the index the older the item
            random_prefer_newer_recommender.set_recommendables(i, timestamp-i*1000)
            pass
        

    def tearDown(self):
        pass


    def test_random_prefer_newer(self):
        random_prefer_newer_recommender = random_prefer_base(preference=0, maximum_age = 259200 )
        ignores = []
        h = histogramm.histogramm()
        for i in xrange(10000):
            recs = random_prefer_newer_recommender.get_recommendation(4, 123, ignores)
            h.binify_categorial( recs )
        recs = h.get_histogramm()
        print "histogram of recommended items. a newer item should have a much higher score then an older one \n"
        print recs
    
    def test_random_prefer_older(self):    
        random_prefer_older_recommender = random_prefer_base(1)
        ignores = []
        h = histogramm.histogramm()
        for i in xrange(10000):
            recs = random_prefer_older_recommender.get_recommendation(4, 123, ignores)
            h.binify_categorial( recs )
        recs = h.get_histogramm()
        print "histogram of recommended items. an older item should have a much higher score then an older one \n"
        print recs
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()