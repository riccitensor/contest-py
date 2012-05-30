'''
Created on 10.01.2012

@author: christian.winkelmann@plista.com
testing the migrations for user by id. Each migration is supposed to test the models and expected queries 
right at instantiation time

'''
import time
import cql
import random
import datetime
from contest.packages.helper.getTimestamp import getTimestamp
from contest.config import config_global, config_local    

class ItemByUserId(object):
    
    def __init__(self):
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port) 
        cursor = dbconn.cursor()
        
        try:
            cursor.execute(""" USE :keyspace """, dict(keyspace = config_global.cassandra_default_keyspace))
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        try:    
            cursor.execute(""" DROP COLUMNFAMILY :columnfamily; """, dict(columnfamily = config_global.dbname_itemByUserId))
            pass
        except cql.ProgrammingError as programmingError:
            print programmingError
        try:
            cursor.execute(""" CREATE COLUMNFAMILY :columnfamily ( 
                KEY varchar PRIMARY KEY )
                WITH comparator=int AND default_validation = counter; """, dict(columnfamily = config_global.dbname_itemByUserId))
        except cql.ProgrammingError as programmingError:
            print programmingError
        
    
    
    """
        currentTime = getTimestamp.gettimeStampInMicroseconds()
        print "currentTime: "
        print int(currentTime)
        
        for user_id in xrange(2):
            for i in xrange(2):
                #currentTime = int(time.time())
                currentTime = getTimestamp.gettimeStampInMicroseconds()
                #print int(currentTime)
    
                # time.sleep(0.11)
                item_id = int( random.uniform(0,10000) )
                cursor.execute(" INSERT INTO :table (KEY, :currentTime) VALUES (:user_id, :item_id)
                USING TTL 100", 
                                dict(table=config_global.dbname_itemByUserId, 
                                currentTime = currentTime,
                                user_id = user_id,
                                item_id = item_id
                                ) 
                               )
                
                item_id = int( random.uniform(0,10000) )
                cursor.execute( INSERT INTO :table (KEY, :currentTime) VALUES (:user_id, :item_id)
                USING TTL 100, 
                                dict(table=config_global.dbname_itemByUserId, 
                                currentTime = currentTime,
                                user_id = user_id,
                                item_id = item_id
                                ) 
                               )
                #time.sleep(0.5)
        
    
        #cursor.execute("SELECT * FROM :table", dict(table="itemsByUserId"))
        cursor.execute("SELECT * FROM :table WHERE KEY = 1", dict(table="itemsByUserId"))
        print cursor.fetchall()
        print cursor.description
"""

if __name__ == '__main__':
    
    IBU = ItemByUserId()