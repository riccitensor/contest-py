'''
Created on 18.05.2012

Recommender which is recommends depending on the message the best item

@author: christian.winkelmann@plista.com
'''
from contest.packages.recommenders.fallback_random import fallback_random

class GeneralRecommender(object):


    def __init__(self, message):
        '''
        Constructor
        '''
        ## TODO parse the message
        
    def recomend(self):
        random_recommender = fallback_random()
        list1 = random_recommender.getRecommendation()
        
        if ( len(list1) < 5 ):
            random_recommender.train() 
        
    
    
        
        
    
    