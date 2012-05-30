'''
Created on 18.10.2011

for categorization this is needed.


@author: karisu
'''
from algorithm.gensimpy.Query import Query
import numpy

class K_Nearest_Neighbour():
    
    def __init__(self):
        '''
        constructor
        '''
                
    def knn(self, k, data, dataClass, inputs):
        ''' This knn implementation will only check for k nearest neighbours and their classes
        and sets the queries document to the most found class
        
        The implementation is derived from "Machine Learning; Stephen, Marsland,
         
        @param document_id: the id of the document   
        @param k: the amount of neighbours    
        '''
        from numpy import *
        nInputs = shape(inputs)[0]
        closest = zeros(nInputs)
        
        for n in range(nInputs):
            # compute Distances
            distances = sum((data-inputs[n,:])**2, axis=1)
            
        indices = argsort(distances, axis=0)
        classes = unique(dataClass[indices[:k]])
        if len( classes ) == 1:
            closest[n] = unique(classes)
        else:
            counts = zeros(max(classes)+1)
            
            for i in range(k):
                counts[dataClass[indices[i]]] += 1
                closest[n] = max(counts)

        return closest                
        
        
        
    def thirdPartyKnn(self):
        ''' bla '''

if __name__ == '__main__':
    db_location = '../linguisticModel/'
    q = Query(5, db_location)

    print q.queryById( 'doc2' ) 
    print  '\n'
    