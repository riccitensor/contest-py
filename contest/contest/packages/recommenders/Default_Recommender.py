'''
Created on 30.05.2012

@author: christian.winkelmann@plista.com

'''

from contest.packages.recommenders.baseRecommender import baseRecommender
from contest.packages.models.RecommendationList import RecommendationList
import redis

class Default_Recommender(baseRecommender):
	
	def __init__(self, message):
		
		# TODO: parse the message
		user_id = 0
		
		super(Default_Recommender, self).__init__()
		self.redis_con = redis.Redis("localhost")
		
		self.user_id = user_id
		self.key = 'default_recommender:{0:d}'.format(user_id)   


	def getRecommendation_unranked(self):
		return (1,2,3,4)




