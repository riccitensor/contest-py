'''
Created on 28.05.2012

replay data from a mysql database

@author: christian.winkelmann@plista.com
'''
import _mysql
import time as time2
from datetime import date

from contest.packages.models.HadoopSink import HadoopSink

from contest.config import config_local


if __name__ == '__main__':
	debug = False
	debug2 = True
	debug3 = True # TODO: this sets the script to just iterate over a fixed results
	""" connect to mysql """
	
	""" select as much ids as you want then enque this as a replay job. 
	Each worker will then fetch the task from the queue and request to 
	the Request handler then """
	
	IMPLICIT = True
	SAVE_ITEM_BY_USER = False
	SAVE_HADOOP_SINK = True
	hS = HadoopSink('/tmp/dump') 
	
	cycle_count = 1000000 #number of items to fetch at once
	n_maxrows = 100000
	
	
	if (not debug3):
		mysql_host = config_local.mysql_host
		user = config_local.mysql_user
		password = config_local.mysql_password
		db=_mysql.connect(host=mysql_host,user=user,
					  passwd=password,db="db_youfilter")
		
	
		if not IMPLICIT:
			sql = """SELECT userid, itemid, src, date as timestamp FROM db_youfilter.clickfeedback c \
			WHERE 1"""
		
		else :
			sql = """SELECT userid, itemid, date, domainid as timestamp FROM db_archive.implicitratings c \
			WHERE 1"""
			
		db.query(sql)
		r=db.use_result()
		result = r.fetch_row(maxrows = n_maxrows) # fetch N row maximum
		
	
	
	replay_time = time2.time()
	n = 1
	print "import data"
	
	if (debug3):
		result = ((1,2,3,4),(4,5,6,7))
	
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
			if ( n % cycle_count == 0 and debug2):
				print n
		
		if (not debug3):		
			result = r.fetch_row(maxrows = n_maxrows) # fetch N row maximum
		else: result = False
		
					
	if (not debug3): db.close() #close the database connection
	replay_time = time2.time() - replay_time
	
	print "time it took: " + str(replay_time)
	print 'It took {0:1f} seconds per item'.format(replay_time/n)
	
	