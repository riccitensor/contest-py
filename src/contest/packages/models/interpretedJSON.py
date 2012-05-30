'''
Created on 19.01.2011
test implementation of an item model. It offers save and get methods

@FIXME this is incomplete 


@author: christian.winkelmann@plista.com
'''
from contest.config import config_local, config_global
import cql
from cql.cassandra import Cassandra
from baseModel import baseModel
from contest.packages.helper.getTimestamp import getTimestamp

class interpretedJsonModel(baseModel):
	
	queued = False
	debug = False
	def __init__(self, id, data = None, mode = 'redis'):
		""" init """
		if (mode == 'redis'):
			""" @todo redis implementation """
			
		elif (mode == 'cassandra'):
		
			super(interpretedJsonModel, self).__init__(mode)
			self.column_family = config_global.dbname_interpretedJson
		
			self.timestamp = getTimestamp.gettimeStampInMicroseconds() 
			""" wrong place for this """
			
			self.obligatoryData = dict(column_family = self.column_family, id = id)
			self.data = data
		
			try:
				self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
							
			except cql.ProgrammingError as programmingError:
				print programmingError
		
	
	def save(self):
		""" save the json string as it is
		@todo: refactor for interpretedJSON
		"""
		if ( self.queued == False):
			""" save it instantly """
			
			insert_query = ""
			 
			d = {}
			for key, value in self.data.items():
					insert_query += key + ","
					d[key] = value
			
			
			keys = self.data.keys()
			
			def my_function(x):
				r = x[0] + " = :" + x[0]
				return r
			
			
			
			#print ','.join( map( my_function, keys ) )
			insert_query = ','.join( map( my_function, self.data.items() ) )
			cql_query = "UPDATE :column_family USING CONSISTENCY ANY SET " + insert_query + " WHERE id = :id "
			if (self.debug):
				print insert_query
				print cql_query
				print self.data	
			
			d = dict(self.data.items() + self.obligatoryData.items())
			
			#import time
			#done = False
			#while ( done == False):
			try:
				self.conn.cursor.execute( cql_query, d )
				
			except cql.InternalError as internalError:
				print "the process of saving failed and should be tried again"
				#time.sleep(0.1)
				

		else:
			""" put the work in the queue """
					
	
	def get(self):
		try:
			cql_query = "SELECT * FROM :column_family WHERE incomingTime = :timestamp"
			d = dict( column_family = self.column_family, 
				  timestamp = self.timestamp )
		
			self.conn.cursor.execute(cql_query, d)
			return self.conn.cursor.fetchone()
			
		except cql.ProgrammingError as programmingError:
			print programmingError
		
		
	
	
if __name__ == '__main__':
	pass
	
	