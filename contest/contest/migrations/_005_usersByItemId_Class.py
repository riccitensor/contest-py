'''
Created on 10.01.2012

@author: christian.winkelmann@plista.com
testing the migrations for user by id. Each migration is supposed to test the models and expected queries 
right at instantiation time

'''
import cql
import random
from contest.packages.helper.getTimestamp import getTimestamp
from contest.config import config_global, config_local    
    
class UserByItemId(object):
    
    def __init__(self):
    
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port) 
        cursor = dbconn.cursor()
        
        try:
            cursor.execute(""" USE :keyspace """, dict(keyspace = config_global.cassandra_default_keyspace))
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        try:    
            cursor.execute(""" DROP COLUMNFAMILY :columnfamily; """, dict(columnfamily = config_global.dbname_usersByItemId))
            pass
        except cql.ProgrammingError as programmingError:
            print programmingError
        try:
            cursor.execute(""" CREATE COLUMNFAMILY :columnfamily ( 
                item_id bigint PRIMARY KEY )
                WITH comparator=timestamp AND default_validation=int; """, 
                dict(columnfamily = config_global.dbname_usersByItemId))
        except cql.ProgrammingError as programmingError:
            print programmingError
        
    
        currentTime = getTimestamp.gettimeStampInMicroseconds()
        print "currentTime: "
        print int(currentTime)
        
        for item_id in xrange(5):
            for i in xrange(5):
                #currentTime = int(time.time())
                currentTime = getTimestamp.gettimeStampInMicroseconds()
                #print int(currentTime)
    
                user_id = int( random.uniform(0,10000) )
                cursor.execute(""" INSERT INTO :table (item_id, :currentTime) VALUES (:item_id, :user_id)
                USING TTL 10""", 
                                dict(table=config_global.dbname_usersByItemId, 
                                currentTime = currentTime,
                                user_id = user_id,
                                item_id = item_id
                                ) 
                               )
                #time.sleep(0.5)
        
    
        cursor.execute("SELECT * FROM :table WHERE item_id = 1", dict(table=config_global.dbname_usersByItemId))
        print cursor.fetchall()
        print cursor.description

if __name__ == '__main__':
    
    uBI = UserByItemId()