'''
Created on 16.11.2011

just the most basic recommender class possible

@author: christian.winkelmann@plista.com
'''
import redis
import logging

class baseRecommender(object):
	'''
	this will be the most naive recommender which just outputs random recommendations
	'''
	#the redis connection
	redis_con = None;
	itemList = "recommendable_items"

	def __init__(self):
		'''
		initial connection to database
		'''
		self.redis_con = redis.Redis("localhost")
		
		
	def get_recommendation(self, N, ignores = ['123', '234'], remove = False ):
		""" fetch a random recommendation 
		@param N number of recommendations
		@param itemids which should be ignored
		"""

		#resultSet = self.redis_con.zrange(self.key, 0, N-1)
		# todo remove the items from the resultest
		return -1
		
	def set_recommendables(self, itemid):
		''' '''
	
	def del_recommendables(self, itemid):
		''' '''

	
if __name__ == '__main__':
	print 'todo'
'''
	fb = fallback_random()
	
	fb.set_recommendables(12345)
	fb.set_recommendables(67890)
	fb.set_recommendables(567)
	fb.set_recommendables( 'bla' )
	
	print fb.get_recommendation(N=2, userid=123)
'''	
	#fb.del_recommendables(12345)
	#fb.del_recommendables(67890)
	
	