'''
Created on 23.05.2012

quite basic recommender which bases recommending random items, but exclude items alredy seen and is therefore 
individual for each user. For unknown users other dimensions can be taken like their browser or publisher

@author: christian.winkelmann@plista.com
'''
import logging
from contest.packages.recommenders.baseRecommender import baseRecommender
from contest.packages.models.RecommendationList import RecommendationList
import redis
import random

class fallback_random(baseRecommender):
	'''
	this will be the most naive recommender which just outputs random recommendations
	'''
	key = None
	itemList = "recommendable_items"
	userid = None

	def __init__(self, user_id):
		super(fallback_random, self).__init__()
		self.redis_con = redis.Redis("localhost")
		
		self.user_id = user_id
		self.key = 'fallback_random:userid:{0:d}'.format(user_id)   
		
	def getRecommendation(self, userid):
		'''
		@param userid: even though the recommendations are random we have to exclude items we already presented '''
		# todo grab the items and create a random list
		
		# @todo first get all recommendable items
		
		# @todo get the items the user has seen already seen, or other excluding factors
		
		# @todo compute the list of recommendations
		self.userid
		
		recList = RecommendationList(self.key, mode='redis')
		recList = recList.get()
		return recList
		
		
	def train(self, userid, N, ignores=[]):
		""" fetch a random recommendation 
		@param N number of recommendations
		@param itemids which should be ignored
		"""
		#ignores = self.redis_con.zrangebyscore('userid:item' + str(userid), 1, float("infinity"), withscores=False)

		recList = []
		i = 0
		if (self.redis_con.scard( self.itemList ) >= len(ignores) + N): #we have more items then we have to ignore + we need
			while (i < N):	 
				recommendable_item = self.redis_con.srandmember(self.itemList)
				if (recommendable_item in ignores):
					pass
				elif (recommendable_item in recList):
					pass
				else: 
					recList.append(recommendable_item) # now compose the list of recommendable items
					i += 1
		else:
			for i in xrange(N):
				recommendable_item = self.redis_con.srandmember(self.itemrecList)
				recList.append(recommendable_item)
				
		#print recList
		logging.debug('getting :' + str(N) + " recommendation, which are: " + str(recList))
		
		for value in recList:
			self.redis_con.zadd(self.key, value, random.random())
		
		return recList
		
		
		#recommendationList = RecommendationList('userid:item' + str(userid), mode = 'redis')

		
	def set_recommendables(self, itemid):
		""" set a recommendable item """
		logging.debug('fallback_random: saving a recommendable item' + str(itemid))
		''' @todo: move this to the writeback methods since the recommender has nothing to do with saving the data '''
		self.redis_con.sadd(self.itemList, itemid)

	def del_recommendables(self, itemid):
		""" delete an recommendable item again """
		''' @todo: move this to the writeback methods since the recommender has nothing to do with managing the data '''
		self.redis_con.srem(self.itemList, itemid)


	
if __name__ == '__main__':
	'''
	'''
	
	
