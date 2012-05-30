'''
Created on 28.05.2012

replay data from a mysql database

@author: christian.winkelmann@plista.com
'''
import _mysql
import time as time2
from datetime import datetime, date, time

from contest.packages.models.HadoopSink import HadoopSink
from contest.packages.helper.getTimestamp import getTimestamp

from contest.config import config_local


if __name__ == '__main__':
	debug = False
	debug2 = True
	""" connect to mysql """
	
	""" select as much ids as you want then enque this as a replay job. 
	Each worker will then fetch the task from the queue and request to 
	the Request handler then """
	
	
	mysql_host = config_local.mysql_host
	user = config_local.mysql_user
	password = config_local.mysql_password
	db=_mysql.connect(host=mysql_host,user=user,
				  passwd=password,db="db_youfilter")
	
	IMPLICIT = True
	SAVE_ITEM_BY_USER = False
	SAVE_HADOOP_SINK = True
	hS = HadoopSink('/tmp/dump') 
	
	cycle_count = 1000000 #number of items to fetch at once
	
	if not IMPLICIT:
		sql = """SELECT userid, itemid, src, date as timestamp FROM db_youfilter.clickfeedback c \
		WHERE 1"""
	
	else :
		sql = """SELECT userid, itemid, date, domainid as timestamp FROM db_archive.implicitratings c \
		WHERE 1"""
		
	db.query(sql)
	r=db.use_result()
	
	replay_time = time2.time()
	
	result = r.fetch_row(maxrows = 100000) # fetch N row maximum
	
	n = 1
	print "start"
	while (result):
		for result_item in result:
			
			the_id = result_item[0]
			userid = int(result_item[0])
			itemid = int(result_item[1])
			timestamp = str(result_item[2])
			domainid = 	int(result_item[3])
				
			current_time = time2.time()

			if( SAVE_HADOOP_SINK ):
				rating = 1
				
				hS.save_mode2(userid, itemid, domainid, date)
			
			n += 1
		
				
		result = r.fetch_row(maxrows = 100000) # fetch N row maximum
		
		if ( n % cycle_count == 0 and debug2):
			print n
					
	db.close() #close the database connection
	replay_time = time2.time() - replay_time
	print "time it took: " + str(replay_time)
	
	