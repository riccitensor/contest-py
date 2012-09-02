'''
Created on 24.11.2011

@author: christian.winkelmann@plista.com
'''

import packages.test.testGensimHttpApi
from packages.test.testGensimHttpApi import IndexingOverRest
from packages.recommenders.baseRecommender import baseRecommender
import redis
from packages.queues import enque_new_semantic_item

class semantic_similarity(baseRecommender):
    '''
    this class will work as a cache for a any kind of semantic similarity 
    '''
    gensim = 0;
    other = 1;
    algorithm = gensim; # this means gensim
    baseurl = "localhost:5002"

    h_redis_index_semantic_items = "index_semantic_items"
    z_redis_item_to_item_similarity = "item_to_item_similarity"

    training_id = 5

    def __init__(self):
        '''
        set up a connection to the similarity server
        '''
        super(semantic_similarity, self).__init__()
        self.redis_con = redis.Redis("localhost")


    def set_recommendables( self, item_id, document_text ):
        """ check if item is already indexed and ready to be queryied        
        """
        if ( self.redis_con.hexists(self.h_redis_index_semantic_items, str(item_id)) ):
            return True

        else:
            """ it is not in the index, we have to add """
            enque_new_semantic_item(item_id, document_text)
            return False
            # this would have been great, but we need to do that asynchrounesly
            #ior = IndexingOverRest()
            #ior.fillIndexingSet(document_text, item_id)
            #ior.indexIndexingSet()

        return None


    def get_recommendation(self, N, item_id ):
        """     
        if our item was already computed then its great, otherwise we can't do anything
        """
        result = self.redis_con.zrange(self.z_redis_item_to_item_similarity + ":" + str(item_id), 0, -1, desc=True,
            withscores=True)

        print result

        return None

if __name__ == '__main__':
    ss = semantic_similarity()

    ss.redis_con.zadd(ss.z_redis_item_to_item_similarity + ":123", 345, 0.7)
    ss.redis_con.zadd(ss.z_redis_item_to_item_similarity + ":123", 456, 0.2)
    ss.redis_con.zadd(ss.z_redis_item_to_item_similarity + ":123", 789, 0.5)
    ss.get_recommendation(5, 123)
    
    
    
    
            