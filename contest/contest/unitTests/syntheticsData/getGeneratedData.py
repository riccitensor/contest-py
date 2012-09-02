'''
Created on 03.01.2012

now we are testing querying data from our cassandra table

@author: christian.winkelmann@plista.com
@TODO: major refactoring needed since this is just a big conglomerate of various script snippets
'''

import time
from contest.packages.models.itemModel import itemModel 

from contest.config import config_global
from contest.config import config_local
import cql


if __name__ == '__main__':
	'''start the server on command line
	sudo bin/cassandra -f '''
	''' connect to the server '''


	dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
	item_id = 1

	cursorb = dbconn2.cursor()
	cursorb.execute("USE " + config_global.cassandra_default_keyspace)
	a = time.time()
#	
#	cursorb.execute("USE plistaContest")
#	cursorb.execute("""SELECT COUNT(*) FROM itemTableFull WHERE filter_a = 1 LIMIT 100""")
#	
#	resultset = cursorb.fetchall()
#	print resultset
#	print len(resultset)
#	
#	
#	
#	a = time.time() - a
#	print "length"
#	print resultset
#	print "time:"
#	print a
#	
	#print len(resultset)
	
	
	query = "SELECT COUNT(*) FROM itemTableFull;"
	cursorb.execute(query )
	print "number of items:\t" + str(cursorb.fetchone())
	print ""
	
	query = "SELECT COUNT(*) FROM itemTableFull WHERE domainid = 1 AND friend_domain_id = 5"
	cursorb.execute(query )
	print cursorb.fetchall()
	
	"""
	cursorb.execute("SELECT * FROM user WHERE key >= 123;")
	print "should give 3 results"
	print cursorb.fetchall()
	
	cursorb.execute("SELECT * FROM user WHERE key >= 123 AND state = 'MI' AND domainid >= 1 LIMIT 100")
	print cursorb.fetchall()
	"""
	#itemA = itemModel( int(item_id) )
	#itemA.query_by()
	
	# itemA.query_submitted_String(cql_query = "bla")
	