'''
Created on 22.01.2012

The keep lists of all dimensions. I.e. we keep track of all 
users, browser, domains, items,

To accomplish this we have to use ultra wide rows. That is a feature of cassandra which issues
several problems: it is difficult to scale. writing a ultra wide row uses a single server only

@see: the distributed Counters are doing quite the same.


@author: christian.winkelmann@plista.com


'''
import time

import cql
import random
import datetime
from contest.packages.helper.getTimestamp import getTimestamp
from contest.config import config_global, config_local    


class dimensionListsMigration(object):
    
    def __init__(self):
    
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port) 
        cursor = dbconn.cursor()
        
        try:
            cursor.execute(""" USE :keyspace """, dict(keyspace = config_global.cassandra_default_keyspace))
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        try:    
            cursor.execute(""" DROP COLUMNFAMILY :columnfamily; """, dict(columnfamily = config_global.dbname_dimensionList))
            pass
        except cql.ProgrammingError as programmingError:
            print programmingError
        try:
            cursor.execute("""
            CREATE COLUMNFAMILY :columnfamily 
            (
            dimension_name text PRIMARY KEY 
            )
            WITH comparator = int AND default_validation = int;
        """, 
                dict(columnfamily = config_global.dbname_dimensionList))
        except cql.ProgrammingError as programmingError:
            print programmingError
        
    
        """ lets insert row keys """
        
        for dimension in config_global.dbname_dimensionList_rowKeys:
            
            try: 
                
                for dimension_value in xrange(3):
                    
                    cursor.execute("""INSERT INTO :table ( dimension_name, :dimension_value ) VALUES 
                    ( :dimension_name, :dimension_value) USING TTL 10 """, 
                                        dict(table=config_global.dbname_dimensionList,
                                             dimension_name = dimension,
                                             dimension_value = dimension_value) 
                                       )
                    
            except cql.ProgrammingError as programmingError:
                print programmingError

             
            """ now we have to check if a dimension is already known """
            try:
                for test_id in xrange(1):
                       
                    cursor.execute("""SELECT FIRST 3 REVERSED * FROM :table WHERE dimension_name = :dimension_name""", 
                                           dict(table=config_global.dbname_dimensionList,
                                                dimension_name = dimension
                                                ) 
                                          )
                    print cursor.fetchall()
                    
            except cql.ProgrammingError as programmingError:
                print programmingError
                
            

if __name__ == '__main__':
    
    dL = dimensionListsMigration()