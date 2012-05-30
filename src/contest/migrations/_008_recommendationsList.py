'''
Created on 21.05.2012

list of recommendations

@author: christian.winkelmann@plista.com


'''
import time

import cql
import random
import datetime
from contest.packages.helper.getTimestamp import getTimestamp
from contest.config import config_global, config_local	


class recommendationListMigration(object):
	
	def __init__(self):
	
		dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port) 
		cursor = dbconn.cursor()
		
		try:
			cursor.execute(""" USE :keyspace """, dict(keyspace = config_global.cassandra_default_keyspace))
		except cql.ProgrammingError as programmingError:
			print programmingError
		
		try:	
			cursor.execute(""" DROP COLUMNFAMILY :columnfamily; """, dict(columnfamily = config_global.dbname_recommendationsList))
			pass
		except cql.ProgrammingError as programmingError:
			print programmingError
		try:
			cursor.execute("""
			CREATE COLUMNFAMILY :columnfamily 
			(
			user_id text PRIMARY KEY 
			)
			WITH comparator = int AND default_validation = int;
		""", 
				dict(columnfamily = config_global.dbname_recommendationsList))
		except cql.ProgrammingError as programmingError:
			print programmingError
		
	
		""" lets insert row keys """
		
		for user_id in xrange(5):
			for item_id in xrange(5):
				try: 
					cursor.execute("""INSERT INTO :table ( user_id, :item_id ) VALUES 
						( :user_id, :score ) USING TTL 10 """, 
											dict(table = config_global.dbname_recommendationsList,
												user_id = user_id,
												item_id = item_id,
												score = 5 - item_id ) 
										   )
						
				except cql.ProgrammingError as programmingError:
					print programmingError

			 
		try:

			cursor.execute("""SELECT FIRST 3 REVERSED * FROM :table WHERE user_id = 2""", 
									   dict(table=config_global.dbname_recommendationsList
											) 
									  )
			print cursor.fetchone()
				
		except cql.ProgrammingError as programmingError:
			print programmingError
				
			

if __name__ == '__main__':
	
	dL = recommendationListMigration()
	
	
	