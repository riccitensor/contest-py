'''
Created on 12.02.2012

@author: karisu
'''
import random
import time

class BitMapIndex(object):
    '''
    model the bitmap index
    '''
    


    def __init__( self ):
        '''
        Constructor
        '''
        #self.index = dict()
        klm = pow(2, 500)
        self.index = list()
        print "building the index"
        for i in xrange(30000000):
            self.index.append( int(random.uniform(0,klm)) )
            #self.index.append( int(random.uniform(0,2)) )
        print "done building the index"
        
        
    def select(self, bitmap):
        #print self.index
        resultSet = list()
        row_key = 0
        for value in self.index:
            
            if ( (bitmap == value) ):
                resultSet.append(row_key)
            row_key =+ 1
        return resultSet
    
    
if __name__ == '__main__':
    
    bmI = BitMapIndex()
    
    start = time.time()
    #print bmI.index
    for k in xrange(1):
        #for i in xrange(1,2):
            bmI.select(1)
            
    end = time.time()
    print end - start 
    
            