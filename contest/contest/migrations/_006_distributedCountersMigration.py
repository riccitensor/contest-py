'''
Created on 10.01.2012

@author: christian.winkelmann@plista.com
testing the migrations for user by id. Each migration is supposed to test the models and expected queries 
right at instantiation time

'''
import cql
from contest.packages.helper.getTimestamp import getTimestamp
from contest.config import config_global, config_local    
    
    
class DistributedCountersMigration(object):
    
    def __init__(self):

    
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port) 
        cursor = dbconn.cursor()
        
        try:
            cursor.execute(""" USE :keyspace """, dict(keyspace = config_global.cassandra_default_keyspace))
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        try:    
            cursor.execute(""" DROP COLUMNFAMILY :columnfamily; """, dict(columnfamily = config_global.dbname_distributedCounter))
            pass
        except cql.ProgrammingError as programmingError:
            print programmingError
        try:
            cursor.execute("""
            CREATE COLUMNFAMILY :columnfamily (KEY text PRIMARY KEY, count_x counter)
                WITH comparator = ascii AND default_validation = counter;
        """, 
                dict(columnfamily = config_global.dbname_distributedCounter))
        except cql.ProgrammingError as programmingError:
            print programmingError
        
    
        try:
            cql_query =  """BEGIN BATCH USING CONSISTENCY ONE
                UPDATE :columnfamily SET count_x = count_x + 1 WHERE key = 'test_counter' 
                UPDATE :columnfamily SET count_y = count_y + 1 WHERE key = 'test_counter' 
                APPLY BATCH 
                """
            d = dict(columnfamily = config_global.dbname_distributedCounter)
            cursor.execute(cql_query, d) 
        except cql.ProgrammingError as programmingError:
            print programmingError
            
        try:
            cql_query = "SELECT * FROM :columnfamily WHERE KEY = 'test_counter'"
            cql_query = "SELECT * FROM :columnfamily"
            cursor.execute(cql_query, dict(columnfamily = config_global.dbname_distributedCounter))
            print cursor.rowcount
            r = cursor.fetchone()
            print cursor.description
            print r
    
        except:
            print "counter problem"
            
        
        
        
        
if __name__ == '__main__':
    dC = DistributedCountersMigration()
            