'''
Created on 04.12.2011

@author: christian.winkelmann@plista.com
'''
import unittest
from contest.config import config_local
from contest.packages.statistics.histogramm import histogramm
import random

import sys
import os
#sys.path.append(config_local.)


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
    print "location"
    #print LOCATE #
    print os.getcwd()+ '/' #

    print sys.argv[0] #

    #import sys;sys.argv = ['', 'Test.testName']
   # unittest.main()