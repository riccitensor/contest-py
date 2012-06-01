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

		self.redis_con.zincrby(self.userid_location, userid, 1) #

		self.redis_con.zincrby('userid:item' + str(userid), itemid, 1) #
		self.redis_con.expire('userid:' + str(userid), 172800) # two days ttl

		#self.redis_con.rpush(self.userid_location, userid) # just log all user ids

	def save(self, indexid, dimensionValue):

		self.redisConnection.sadd(self.main_key + ":{}:list".format(self.index_Name), indexid )
		self.redisConnection.sadd(self.main_key + ":{}:list".format(self.dimension_Name), dimensionValue )


	def computeKey(self, index, payload):
		key = self.userid_location + ":{}:{}".format(self.index_Name, self.dimension_Name)


if __name__ == '__main__':
	us = UserStats(123, 567)
	print "userstats"
            