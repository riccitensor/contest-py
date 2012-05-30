'''
Created on 20.11.2011

@author: karisu
'''

import redis


class UserStats(object):
    '''
    statistic for impressions
     
    '''
    redis_con = None
    userid_location = "userids"

    def __init__(self, userid, itemid):
        '''
        Constructor
        @param userid the user id
        @param itemid the item id
        '''        
        self.redis_con = redis.Redis("localhost")
        #self.redis_con.rpush(self.userid_location, userid) # just log all user ids
        self.redis_con.zincrby(self.userid_location, userid, 1 ) #
        self.redis_con.zincrby('userid:item' + str(userid), itemid, 1) # 
        self.redis_con.expire('userid:' + str(userid), 172800) # two days ttl
        
    
if __name__ == '__main__':
    
    us = UserStats(123, 567)
    print "userstats"
            