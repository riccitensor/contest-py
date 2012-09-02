'''
Created on 25.12.2011

@author: christian.winkelmann@plista.com

All impressions will be saved in their raw format.
pure json with the primary key "timestamp" when it came in

'''
from contest.config import config_local
from contest.config import config_global
import cql
    
class rawJsonDump_Class(object):
    
    def __init__(self):
        
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port ) 
        cursor = dbconn.cursor()
        
        try:
            cursor.execute("USE " + config_global.cassandra_default_keyspace)
            cql_query = """ DROP COLUMNFAMILY :rawJsonDump """
            cursor.execute(cql_query, dict(rawJsonDump = config_global.dbname_rawJson))
        except cql.ProgrammingError as programmingError:
            print cql_query
            print programmingError
        
        try:
            cursor.execute("USE " + config_global.cassandra_default_keyspace)
            cursor.execute(""" CREATE COLUMNFAMILY :rawJsonDump 
            ( incomingTime timestamp PRIMARY KEY, jsonString text ) 
            WITH comment = ' simply the raw input data received from the contest server ' """, 
                           dict(rawJsonDump = config_global.dbname_rawJson))
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        
        """ lets try getting the latest items ordered"""
        cursor.execute("USE " + config_global.cassandra_default_keyspace)
        cursor.execute(""" SELECT FIRST 5 * FROM :rawJsonDump LIMIT 5""", dict(rawJsonDump = config_global.dbname_rawJson))
        
        row = cursor.fetchone()
        while (row):
            print row
            row = cursor.fetchone()





if __name__ == '__main__':
    
    rJSD = rawJsonDump_Class()
    
    
    