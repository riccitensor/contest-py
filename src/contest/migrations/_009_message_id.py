'''
Created on 10.01.2012

RAW Clickstream data

@author: christian.winkelmann@plista.com

A list of the message ids. This is something which is potentially not suited for cassandra at a large scale.
Every time a message gets in it will be saved in raw format and the id will be pushed into this


'''
import time
import cql
import random
import datetime
from contest.packages.helper.getTimestamp import getTimestamp
from contest.config import config_global, config_local    
    


class Message_ID_Migration(object):
    
    def __init__(self):
        columnfamily = config_global.dbname_message_ids

    
        
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port) 
        cursor = dbconn.cursor()
        
        try:
            cursor.execute(""" USE :keyspace """, dict(keyspace = config_global.cassandra_default_keyspace))
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        try:    
            cursor.execute(""" DROP COLUMNFAMILY :columnfamily; """, dict(columnfamily = columnfamily))
            pass
        except cql.ProgrammingError as programmingError:
            print programmingError
        try:
            cursor.execute(""" CREATE COLUMNFAMILY :columnfamily ( 
                KEY varchar PRIMARY KEY )
                WITH comparator=timeuuid AND default_validation=bigint; """, 
                dict(columnfamily = columnfamily))
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        
    
        currentTime = getTimestamp.gettimeStampInMicroseconds()
        print "currentTime: "
        print int(currentTime)
        
        for impression_id in xrange(5000):
            #currentTime = getTimestamp.gettimeStampInMicroseconds()
            currentTime = impression_id
            cursor.execute(""" INSERT INTO :table ( KEY , :currentTime) 
            VALUES (impression_list, :impression_id)
            USING TTL 10""", 
                            dict(table=columnfamily, 
                            currentTime = currentTime,
                            impression_id = 1327522
    
                            ) 
                           )
        
        #cursor.execute("SELECT FIRST 5 REVERSED 7..3 FROM :table WHERE KEY = 'impression_list'", 
        #               dict(table=columnfamily))
        
        cursor.execute("SELECT FIRST 5000 REVERSED * FROM :table WHERE KEY = 'impression_list'", 
                       dict(table=columnfamily))
        result = cursor.fetchone()
        print result
        print len(result)
        #print cursor.description
    
if __name__ == '__main__':
    
    mI = Message_ID_Migration()