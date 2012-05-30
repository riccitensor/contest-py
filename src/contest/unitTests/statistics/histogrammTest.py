'''
Created on 04.12.2011

@author: karisu
'''
import unittest
from contest.packages.statistics.histogramm import histogramm
import random

class histogrammTest(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testNominalHistogramm(self):
        h = histogramm()
        r = []
        for i in xrange(20000):
            r_ = random.gauss(1,0.1)
            while ( h.maxx < r_ or h.minx > r_ ):
                r_ = random.gauss(1,1)
            # r.append( random.uniform(0,1) )
            r.append( r_ )
        
        h.binify_real(r)
        
        print h.get_histogramm()
    
    def testcategorialHistogramm(self):
        k = histogramm()
        for i in xrange(100000):
            dict = {"c1" : random.uniform(0,1.1), "c2" : random.uniform(0,1), "c3" : random.uniform(0,1), "c4" : random.uniform(0,1)  }
            k.binify_categorial(dict)
            
        catHistogram = k.get_histogramm(sorted = False)
        print catHistogram

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()