'''
Created on 02.12.2011

@author: christian.winkelmann@plista.com
'''

import math
import random

class histogramm(object):
    
    def __init__(self, binnum = 5, min = 0, max = 2 ):
        self.binnum = binnum
        self.minx = min
        self.maxx = max
        self.histogram = {}
        
    
    
    def binify_real(self, list):
        diff = self.maxx - self.minx
        self.binsize = float(diff) / float(self.binnum)
        for i in xrange(self.binnum): self.histogram[i] = 0

        for l in list:
            binindex = math.floor( (l / self.binsize))
            self.histogram[binindex] += 1

    
    def binify_categorial(self, dict):
        """@param dict: dictionary of categorial data """ 
        for k,i in dict.items():
            try :
                self.histogram[k] += i
            except KeyError:
                self.histogram[k] = i   
        
        
    def get_histogramm(self, sorted = False):
        
        for k, i in self.histogram.items():
            self.histogram[k] = round(i,3)
        
        if ( sorted == False ) :return self.histogram
        else: return self.sortedDictValues2( self.histogram )
        
    # a further slight speed-up on my box
    # is to map a bound-method:
    def sortedDictValues3(self, adict):
        keys = adict.keys()
        keys.sort()
        return map(adict.get, keys)    
    
    
    # an alternative implementation, which
    # happens to run a bit faster for large
    # dictionaries on my machine:
    def sortedDictValues2(self, adict):
        keys = adict.keys()
        keys.sort()
        return [dict[key] for key in keys]

if __name__ == '__main__':
    """
    """