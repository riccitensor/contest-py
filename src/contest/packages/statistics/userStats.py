'''
Created on 20.11.2011

@author: christian.winkelmann@plista.com
'''

import redis


class UserStats(object):
	'''
statistic for impressions

'''


	redis_con = None
	main_key = "stats_list"

	def __init__(self, indexname, dimensionname):
		self.index_Name = indexname
		self.dimension_Name = dimensionname

		self.redisConnection = redis.Redis('localhost')



		#self.redisConnection.zincrby('userid:item' + str(userid), itemid, 1) #
		#self.redisConnection.expire('userid:' + str(userid), 172800) # two days ttl

		#self.redis_con.rpush(self.userid_location, userid) # just log all user ids

	def save(self, indexid, dimensionValue):

		self.redisConnection.sadd(self.main_key + ":{}:list".format(self.index_Name), indexid )
		self.redisConnection.sadd(self.main_key + ":{}:list".format(self.dimension_Name), dimensionValue )

		#self.redisConnection.zadd(self.main_key + ":{}:zset".format(self.dimension_Name), )
		self.redisConnection.zincrby(self.main_key + ":zset:".format(self.index_Name) , indexid, 1) #


	def computeKey(self, index, payload):
		key = self.userid_location + ":{}:{}".format(self.index_Name, self.dimension_Name)


	def get_Top_N(self, dimension_Name, N):
		key = self.main_key + ":{}:list".format(dimension_Name)
		#toplist = self.redisConnection.zrevrangebyscore(key, float("infinity"), 0, 0, num=N, withscores = True)
		#self.redisConnection.zrangebyscore(key, start=1, )
		self.redisConnection.zrevrangebyscore("bla", 4, 1, start=0, num=3, withscores=True)
		#self.redis_con.zrevrangebyscore(config_global.dbname_rawJson + ":zset", float("infinity"), 0, 0, N, withscores = False)
		return toplist



if __name__ == '__main__':
	us = UserStats('userid', 'itemid')
	us.save(1,2)
	us.save(1,3)

	print us.get_Top_N('userid', 3)
            