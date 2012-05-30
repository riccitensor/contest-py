'''
Created on 16.11.2011

quite basic recommender which bases recommendeing random items, but exclude items alredy seen

@author: karisu
'''
import redis
import logging
import time
import random

from contest.packages.recommenders.fallback_random import fallback_random

class random_prefer_base( fallback_random ):
    '''
    a random recommender which prefers newer items
    '''
    #the redis connection
    redis_con = None;
    z_itemList = "z_recommendable_items_with_timestamp"
    maximum_item_age = 0

    def __init__(self, preference=0, maximum_age = 259200 ):
        '''
        initial connection to database
        '''
        self.redis_con = redis.Redis("localhost")
        
        """ depending on the preference use a function for preferring newer or older items """
        if (preference == 0): 
            self.closure = self.mylambda_newer
        elif (preference == 1):
            self.closure = self.mylambda_older
        else: return -1
            
        self.maximum_item_age = maximum_age    
        
    def mylambda_newer(self, r):
        return r[0], (self.maximum_item_age - (self.currenttime - r[1] )) / self.maximum_item_age           
    
    def mylambda_older(self, r):
        diff = self.currenttime - r[1]
        return r[0],  ( ( 1.0 / self.maximum_item_age) * diff ) 
    
        
    def get_recommendation(self, N, userid, ignores = ['123', '234'], hours = 48 ):
        """ fetch a random recommendation 
        @param N number of recommendations
        @param itemids which should be ignored
        @param hours: time to look back in the past 
        """
        """ @TODO this is mega inefficient algorithm wise. DO this in redis itself """
        " get the ignorelist "
        self.currenttime = time.time() # sets the current time statically, lets hope
        
        ignores = self.redis_con.zrangebyscore('userid:item' + str(userid), 1, float("infinity"), withscores=False)
        list_ = []
        list = {} 
        """ the recommendation process is a little different. First we are picking N random items and then we 
        are giving them a random score. Then we will add our bias from for the older/newer preference """
        
        i = 0
        if ( self.redis_con.scard(self.itemList) >= len(ignores)+N ):
     
            list_ = self.redis_con.smembers(self.itemList)
            # list exclusion. our item has to be in the list but not in the ignores
            list_ = [val for val in list_ if val not in ignores]
            
            for i in list_ : 
                list[i] = random.uniform(0,1)
            
            
        else:
            for i in xrange(N):
                recommendable_item = self.redis_con.srandmember( self.itemList )
                list[recommendable_item] = random.uniform(0,1)
               
               
        ## 1. get items sorted by age 
        
        recommendables = self.redis_con.zrangebyscore(self.z_itemList, self.currenttime-self.maximum_item_age, self.currenttime, withscores=True) ## this could download alot of items
        
        for i in ignores:
            try: 
                del recommendables[i]
            except:
                pass        
               
            
        """ normalize item in the list by the item
        and newer/younger items will get a higher weight """       
        
        weightedItems = {}
        """ @todo: the scoring is only needed for already selected items """
        for r in recommendables:
            k,i = self.closure(r)
            weightedItems[k] = i
        

        # now we have to transfrom the preselected items towards new items
        #print list
        
        for k, i in list.items():
            list[k] = weightedItems[k] + i
        
        
               
        """
        self.redis_con.execute_command("MULTI" )
        self.redis_con.execute_command("SADD", "test1", "bla" )
        self.redis_con.execute_command("SADD", "test1", "la" )
        self.redis_con.execute_command("SADD", "test2", "la" )        
        self.redis_con.execute_command("SDIFF", "test1", "test2" )    
        k = self.redis_con.execute_command("EXEC" )
        """
        
        ## print k[-1]    
            
        #print list
        logging.debug('getting :' + str(N) + " recommendation, which are: " + str(list) )
        return list
        
    def set_recommendables(self, itemid, timestamp = None):
        """ set a recommendable item """
        logging.debug('fallback_random: saving a recommendable item' + str(itemid))
        self.redis_con.sadd( self.itemList, itemid )
        
        
        
        if ( self.redis_con.zscore(self.z_itemList, itemid) ):
            """ if the item is already in the database then we don't need to save it again """
            pass
        else:
            """ if the item is new then add it to the database """ 
            if ( timestamp ): self.redis_con.zadd( self.z_itemList, itemid, timestamp )
            else: self.redis_con.zadd( self.z_itemList, itemid, time.time() )
        

    def del_recommendables(self, itemid):
        """ del an recommendable item again """
        self.redis_con.srem( self.itemList, itemid )


    
if __name__ == '__main__':
    import time
    
    fb = random_prefer_base(0)
    
    
    fb.set_recommendables("old1", timestamp = time.time() - 2)
    fb.set_recommendables("not_so_old", timestamp = time.time() - 1)
    
    fb.set_recommendables("young", timestamp = time.time())
    
    for i in xrange(100):
        print fb.get_recommendation(N=3, userid=123)
    
    #fb.del_recommendables(12345)
    #fb.del_recommendables(67890)
    
    