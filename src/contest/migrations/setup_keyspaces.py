'''
Created on 25.12.2011

@author: christian.winkelmann@plista.com
'''

from contest.config import config_global
from contest.config import config_local
import cql


class Setup_Keyspaces(object):
    
    def __init__(self):
        
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port ) 
        cursor = dbconn.cursor()
        
        try: 
            cql_query = """ DROP KEYSPACE :keyspace; """
            cursor.execute(cql_query, dict(keyspace = config_global.cassandra_default_keyspace))
        except cql.ProgrammingError as programmingError:
            print cql_query
            print programmingError
        
        try:
            cql_query = """ CREATE KEYSPACE :keyspace WITH strategy_class = 'SimpleStrategy'
     AND strategy_options:replication_factor = 1; """
            cursor.execute(cql_query, dict(keyspace = config_global.cassandra_default_keyspace))
        except cql.ProgrammingError as programmingError:
            print cql_query
            print programmingError
            
    

if __name__ == '__main__':
    
    sK = Setup_Keyspaces()