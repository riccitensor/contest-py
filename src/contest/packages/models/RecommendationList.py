'''
Created on 21.01.2012

This is a mixture of cassandra and redis

@author: christian.winkelmann@plista.com
'''

from contest.config import config_global
from contest.config import config_local
import cql
import redis
from cql.cassandra import Cassandra
from baseModel import baseModel
from contest.packages.helper.getTimestamp import getTimestamp
#import time
#from sets import Set


class RecommendationList(baseModel):
	
	mode = None # either redis, cassandra
	redis_con = None
	
	def __init__(self, mode='cassandra'):
		"""
		@param key: identifier 
		@param mode: switch between different storage methods...
		"""
		super(RecommendationList, self).__init__(mode)
		self.mode = mode
		
		if (self.mode == 'cassandra'):
			self.get = self.get_cassandra 
			self.save = self.save_cassandra
		
		elif(self.mode == 'redis'):
			self.get = self.get_redis
			self.save = self.save_redis
		elif(self.mode == 'hybrid'):
			''' @todo: uses both or more storages '''
				
		 
		
		self.list = dict() # the dictionary which holds
		   
		
	
	def save_cassandra(self, key, sortedSet):		
		""" add ids to the columnfamily """
	
		self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)			
		
		if (type(sortedSet) == type(())) or (type(sortedSet) == type([])):
			for item in sortedSet:
				self.__save_cassandra(item[0], item[1])
		elif (type(sortedSet) == type({})):		 
			for value, score in sortedSet.items():
				self.__save_cassandra(value, score)
				
			
	
	def __save_cassandra(self, itemid, score ):
		try:		
				self.conn.cursor.execute("""UPDATE :table SET :id = :score WHERE user_id = :key """,
												dict(table=config_global.dbname_recommendationsList,
													 key=key,
													 id=itemid,
													 score=score												
													 ) 
											   )
				 
						
		except cql.ProgrammingError as programmingError:
			print programmingError
		
					
	def save_redis(self, key, sortedSet):
	
		if (type(sortedSet) == type(())) or (type(sortedSet) == type([])):
			for item in sortedSet:
				self.conn.zadd(key, item[0], item[1])
		elif (type(sortedSet) == type({})):		 
			for value, score in sortedSet.items():
				self.conn.zadd(key, value, score)
		
	

	def get_cassandra(self, key, N, remove=False):
		'''
		@param key: unique identifier
		@param N: number of results max
		@param remove: if set then remove the result from the set afterwards
		'''	 	
		self.conn.cursor.execute("""SELECT FIRST :N REVERSED * FROM :table WHERE user_id = :key""",
								   dict(table=config_global.dbname_recommendationsList,
									N=N,
									key=key
										) 
								  )

		""" interpret the result since the format suck """
		self.dict = {}
		r = self.conn.cursor.fetchone()
		d = self.conn.cursor.description

		'''dict[ r[0] ] = []
		for i in xrange(1, len(r)):
				self.dict[ r[0] ].append( d[i][0] )
'''
			
		# return self.dict
		# print r
		# print d
		return r
		
				
	def get_redis(self, key, N, remove=False):
		""" redis get Function to grab the recommendations
		@param key: unique identifier
		@param N: number of results max
		@param remove: if set then remove the result from the set afterwards
		"""
		recList = self.conn.zrevrange(key, 0, N - 1, withscores=True)

		return recList

				
					
	
if __name__ == '__main__':
	""" just try to get a full list from the given dimension """
	 
	'''try:
		dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port ) 
		cursor = dbconn.cursor()
	
	except:
		print "not able to create a database connection"
	   ''' 
	key = 'recommendations_user2'
	rL = RecommendationList(key)
	# (id, score)
	sortedSet = {77:9, 99:19, 44:1000}
	rL.save(key, sortedSet)
	print rL.get(key, 3)
	
