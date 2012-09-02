'''
Created on 16.12.2011
Implemenation of a simple list of all JSON message received


@author: christian.winkelmann@plista.com

'''
from contest.config import config_local, config_global
import cql
import redis
from baseModel import baseModel

from contest.packages.helper.getTimestamp import getTimestamp

class rawJsonModel(baseModel):
	
	queued = False
	
	def __init__(self, json_string=None, mode='cassandra', incomingTime = None):
		super(rawJsonModel, self).__init__(mode)
		
		self.mode = mode
		if incomingTime == None:
			self.timestamp = getTimestamp.gettimeStampInMicroseconds()
		else:
			self.timestamp = incomingTime
		self.json_string = json_string
		
		if (mode == 'redis'):
			self.redis_con = redis.Redis("localhost")
			
			
		if (mode == 'cassandra'):
			self.column_family = config_global.dbname_rawJson
				
			try:
				self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
								
			except cql.ProgrammingError as programmingError:
				print programmingError
				
		if (mode == 'sqlite'):
					import sqlite3
					self.conn = sqlite3.connect('/home/karisu/database/sqlite_storage') 
					''' @todo: change the path '''
			
        
	
	
	def save(self):
		""" save the json string as it is
		"""
		if ( self.mode == 'cassandra' ):
			""" save it instantly """
			self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
			d = dict(column_family=self.column_family, incomingTime=self.timestamp, json=self.json_string)
			cql_query = """INSERT INTO :column_family (incomingTime, jsonString) VALUES (:incomingTime, :json )
			USING CONSISTENCY ANY  """
			self.conn.cursor.execute(cql_query, d)
		
		if ( self.mode == 'redis' ):
			return self.writeToRedis(self.timestamp, self.json_string)
			
		if (self.mode == 'sqlite'):
			self.saveToFile(self.timestamp, self.json_string)
		
		
			
	

		
	
	def get(self):
		try:
			cql_query = "SELECT * FROM :column_family WHERE incomingTime = :timestamp"
			d = dict(column_family=self.column_family,
				  timestamp=self.timestamp)
		
			self.conn.cursor.execute(cql_query, d)
			return self.conn.cursor.fetchone()
			
		except cql.ProgrammingError as programmingError:
			print programmingError
			
	def getN(self, N):
		if (self.mode == 'redis'):
			return self.redis_con.zrevrangebyscore(config_global.dbname_rawJson + ":zset", float("infinity"), 0, 0, N, withscores = False)
			
			
		if (self.mode == 'cassandra'):
		
			try:
				cql_query = "SELECT * FROM :column_family LIMIT :N"
				d = dict(column_family=self.column_family, 
						N = N)
			
				self.conn.cursor.execute(cql_query, d)
				return self.conn.cursor.fetchall()
				
			except cql.ProgrammingError as programmingError:
				print programmingError
				
		if (self.mode == 'sqlite'):
			self.fetchN_fromFile(N)
				
	def getAll(self):
		if (self.mode == 'redis'):
			return self.redis_con.hgetall(config_global.dbname_rawJson + ":hash")
			
		if (self.mode == 'cassandra'):
		
			try:
				cql_query = "SELECT * FROM :column_family"
				d = dict(column_family=self.column_family)
			
				self.conn.cursor.execute(cql_query, d)
				return self.conn.cursor.fetchall()
				
			except cql.ProgrammingError as programmingError:
				print programmingError
				
		if (self.mode == 'sqlite'):
			''' @todo: build this '''
		
		
		
	def saveToFile(self, timestamp, text):
		c = self.conn.cursor()
		
		try:
			# Create table
			c.execute('''create table rawJsonDump
			(timestamp real, json_string text)''')
		except:
			""" table already exists """
				
				
		# Insert a row of data
		c.execute("insert into rawJsonDump values (:timestamp, :json_string)", 
				  {"timestamp" : timestamp, "json_string" : text})
		
		# Save (commit) the changes
		self.conn.commit()
		
		# We can also close the cursor if we are done with it
		c.close()
		
	def writeToRedis(self, timestamp, body):
		# for ease of use we will write dump to redis at the beginning
		self.redis_con.hset(config_global.dbname_rawJson + ":hash", timestamp, body)
		
		#self.redis_con.hse
		self.redis_con.zadd(config_global.dbname_rawJson + ":zset", body, timestamp)


	
		
	def fetchN_fromFile(self, N):
		""" now we are getting only n results in a sync way """
		import sqlite3
		conn = sqlite3.connect('/home/karisu/database/sqlite_storage')
		
		c = conn.cursor()
		
		c.execute('select * from rawJsonDump order by timestamp LIMIT :lim', {"lim" : N} )
		
		return c.fetchall()

		
	
	
if __name__ == '__main__':
	message = "{\"msg\":\"impression\",\"id\":2,\"client\":{\"id\":1},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"1234\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"

	raw = rawJsonModel(json_string = message, mode='redis')
	raw.save()
	raw.getN(3)



