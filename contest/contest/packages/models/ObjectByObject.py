'''
Created on 20.11.2011

@author: christian.winkelmann@plista.com
'''

import redis


class ObjectByObject(object):
    '''
    statistic for impressions

    '''

    redis_con = None
    main_key = "stats_list"

    def __init__(self, indexname, dimensionname):
        self.index_Name = indexname
        self.dimension_Name = dimensionname
        self.redisConnection = redis.Redis('localhost')


    def save(self, indexid, dimensionValue):
        self.redisConnection.sadd(self.main_key + ":{}:list".format(self.index_Name), indexid)
        self.redisConnection.sadd(self.main_key + ":{}:list".format(self.dimension_Name), dimensionValue)
        self.redisConnection.zincrby(self.main_key + ":zset:{}".format(self.index_Name), indexid, 1) #


    def computeKey(self, index, payload):
        key = self.userid_location + ":{}:{}".format(self.index_Name, self.dimension_Name)
        return key


    def get_Top_N(self, dimension_Name, N):
        key = self.main_key + ":zset:{}".format(dimension_Name)
        toplist = self.redisConnection.zrevrangebyscore(key, float("infinity"), 0, 0, num=N, withscores=True)

        return toplist

    def make_plot(self):
        ''' '''


if __name__ == '__main__':
    ''' '''
