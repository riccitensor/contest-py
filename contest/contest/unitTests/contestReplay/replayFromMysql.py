'''
Created on 08.01.2012

this is an integration test, which will benchmark the whole system regarding the raw write performance


@author: christian.winkelmann@plista.com

'''
from contest.config import config_local
from contest.controller import http_connector

from contest.packages.helper.getTimestamp import getTimestamp
import _mysql
import time as time2
from contest.packages.message_parsers.FullContestMessageParser import FullContestMessageParser
from contest.packages.models.ItemByUser import ItemsByUser
from contest.packages.models.distributedCounters import distributedCounters
from contest.packages.models.DimensionListModel import DimensionListModel
from datetime import datetime
from contest.packages.models.HadoopSink import HadoopSink


if __name__ == '__main__':
	debug = False
	debug2 = True
	""" connect to mysql """
	
	""" select as much ids as you want then enque this as a replay job. 
	Each worker will then fetch the task from the queue and request to 
	the Request handler then """
	
	""" grab the messages and send them as a post to the contest request handler """
	
	
	db=_mysql.connect(host="localhost",user="root",
				  passwd=config_local.mysql_password,db="contest")
	
	SAVE_ITEM_BY_USER = False
	SAVE_DIMENSION_LIST = False
	SAVE_DISTRIBUTED_COUNTER = False
	SAVE_HADOOP_SINK = False
	hS = HadoopSink()
	
	#db.query("""SELECT * FROM contest.contest_messages c LIMIT 0,1000""")
	#db.query("""SELECT id, type, timestamp, json, response_time, response_id FROM contest.contest_messages c \
	#WHERE type = 'impression' AND id > 1500004 LIMIT 5""")
	db.query("""SELECT id, type, timestamp, json, response_time, response_id FROM contest.contest_messages c \
	WHERE ( type = 'impression' ) AND id > 1000000 LIMIT 10 """)
	r=db.use_result()
	
	""" what happens if there is a timestamp collison? It doesn't matter if we don't try to count with the timestamp
	""" 
	
	replay_time = time2.time()
	
	result = r.fetch_row()
	
	print result
	
	n = 0
	while (result):
		if (debug): 
			print "============================================================================================"
		#time.sleep(0.05)
		"just grab the json"
		json_string = result[0][3]
		the_id = result[0][0]
		# print the_id
		#print result
	
		current_time = time2.time()
		""" instead of using the current time we will just use the timestamp given by the contest as a timestamp """
		contest_timestamp = result[0][2]
		
		print contest_timestamp
		
		#2011-09-29 16:44:44
		contest_timestamp = datetime.strptime(contest_timestamp, "%Y-%m-%d %H:%M:%S")
		#contest_timestamp.
		timestamp_sec = getTimestamp.getTimeStampFromPythonDateTime(contest_timestamp)
		 
		#print timestamp_sec
		
		
		if ( not debug2 ):
			""" this step should simulate the normal process of the contest """
			http_conn = http_connector('localhost:5001')
			http_conn.send('/contest/incoming_message', json_string)
		else:
			""" this step is for debugging """
			#print json_string
			#rjm = rawJsonModel( json_string )
			#rjm.save()
			
			
			parser = FullContestMessageParser()
			flattenedJson = parser.parse(json_string)
			
			print flattenedJson
			
			""" lets save the data, each field a column """
			if ( flattenedJson ):
				#iJson = interpretedJsonModel(the_id, flattenedJson)
				#iJson.save()
				if (SAVE_ITEM_BY_USER):
					try:
						timeStamp = timestamp_sec
						iBU = ItemsByUser(user_id = flattenedJson['client_id'], timeStamp = timeStamp )
						
						iBU.save( item_id = flattenedJson['item_id'] )
						
						if(debug):
							print "item_id:\t " + str( flattenedJson['item_id'] )
							print "user_id:\t" + str(flattenedJson['client_id'])
						
					except:
						print "ItemsByUser: no item given"
				
				try:
					#uBI = UserByItem(item_id = flattenedJson['item_id'])
					#uBI.save( user_id = flattenedJson['client_id'] )
					pass
				except:
					print "UsersByItem: no user given"
					
				
				if (SAVE_DISTRIBUTED_COUNTER):
					try:
						dC = distributedCounters(flattenedJson, timestamp_sec)
						dC.increment_by_collumn()
						
	
						""" now we are doing some general statistics: 
						most important users
						most important items
						
						"""
					except:
						if(debug): 
							print flattenedJson
						print "problem with distributed counters"
				
				"""
				dimList = ['client_id', 'item_id']
				for dim in dimList:
					dL = DimensionListModel(dim)
					try: 
						dL.save( flattenedJson[dim] )
					except:
						print "problem DimensionListModel: " + dim + "	item_id:	" + the_id
						
			   
				dL = DimensionListModel('hours')
				try: 
					dL.save( getTimestamp.gettimeStampIn_Hours( flattenedJson['item_created'] ) )
				except:
					print "DimensionListModel: no time given at"
				
				
				dL = DimensionListModel('days')
				try: 
					dL.save( getTimestamp.gettimeStampIn_Days( flattenedJson['item_created'] ) )
				except:
					print "DimensionListModel: no time given at"
				"""
				
				
				""" now we want a log for each user and each item with the corresponding seen items or users respectiveley """	

				if (SAVE_DIMENSION_LIST):
					dimension = 'user_ids'
					dL = DimensionListModel( dimension, mode = 'redis' )
					if(debug):
						print "userid:\t" + str(flattenedJson['client_id'])
					dL.save( dimension_id = flattenedJson['client_id'], timestamp = timestamp_sec )
		
				if( SAVE_HADOOP_SINK ):
					
					if ( ('item_id' in flattenedJson) and ('client_id' in flattenedJson)  ):
						if ( 519516260 == int(flattenedJson['client_id']) ):
							print ""
							#print int(flattenedJson['item_id'])
						hS.save_mode1(int(flattenedJson['client_id']), int(flattenedJson['item_id']), 1)
		
		

		#_mysql.connection.query()
		#import logging
		#logging.basicConfig(filename='output.log',level=logging.DEBUG)
			   
		#logging.debug('"POST message\n "')
		
		result = r.fetch_row()
		
	db.close()
	replay_time = time2.time() - replay_time
	print "time it took: " + str(replay_time)
	
	