'''
Created on 25.12.2011

@author: christian.winkelmann@plista.com

All impressions will be saved in their column based format.
primary key is a "timestamp" which we get from the interpreted json

'''
from contest.config import config_local
from contest.config import config_global
import cql
    

class interpretedJson_class(object):
    
    def __init__(self):
        

    
    
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port ) 
        cursor = dbconn.cursor()
        
        try:
            cursor.execute("USE " + config_global.cassandra_default_keyspace)
            cursor.execute(" DROP COLUMNFAMILY :columnfamily; ",  
                           dict(columnfamily = config_global.dbname_interpretedJson))
        except cql.ProgrammingError as programmingError:
            print programmingError
           
        try:
            cursor.execute("USE " + config_global.cassandra_default_keyspace)
            cursor.execute(""" CREATE COLUMNFAMILY :columnfamily ( 
                    id bigint PRIMARY KEY,
                    impression_id bigint, 
                    client_id int,
                    domain_id int,
                    item_id int,
                    item_title text,
                    item_url text,
                    item_created timestamp,
                    item_text text,
                    config_timeout int,
                    message_type text
                    ) 
                        WITH comment = 'the interpreted json message with one column for each datafield'; 
     """, 
                        dict(columnfamily = config_global.dbname_interpretedJson))
        except cql.ProgrammingError as programmingError:
            print programmingError
           
        try:   
            cursor.execute(""" CREATE INDEX ON :columnfamily (client_id);   """, 
                        dict(columnfamily = config_global.dbname_interpretedJson))
            
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        try:   
            cursor.execute(""" CREATE INDEX ON :columnfamily (domain_id);   """, 
                        dict(columnfamily = config_global.dbname_interpretedJson))
            
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        try:   
            cursor.execute(""" CREATE INDEX ON :columnfamily (item_id);   """, 
                        dict(columnfamily = config_global.dbname_interpretedJson))
                                                    
        except cql.ProgrammingError as programmingError:
            print programmingError
           
        try:   
            cursor.execute(""" CREATE INDEX ON :columnfamily (item_created);   """, 
                        dict(columnfamily = config_global.dbname_interpretedJson))
                                                    
        except cql.ProgrammingError as programmingError:
            print programmingError    
        
        try:   
            cursor.execute(""" CREATE INDEX ON :columnfamily (config_timeout);   """, 
                        dict(columnfamily = config_global.dbname_interpretedJson))
                                                    
        except cql.ProgrammingError as programmingError:
            print programmingError
    
        try:   
            cursor.execute(""" CREATE INDEX ON :columnfamily (message_type);   """, 
                        dict(columnfamily = config_global.dbname_interpretedJson))
                                                    
        except cql.ProgrammingError as programmingError:
            print programmingError
                
    
    
    
        
            """ lets try getting the latest items ordered"""
            cursor.execute("USE " + config_global.cassandra_default_keyspace)
            cursor.execute(""" SELECT * FROM :columnfamily
                    
                                     LIMIT 100 ;""", 
                           dict(columnfamily = config_global.dbname_interpretedJson))
            
            row = cursor.fetchone()
            while (row):
                #print row
                row_dict = {}
                row = cursor.fetchone()
                #print cursor.description
                
                d = cursor.description
                for i in xrange(len(row)):
                    row_dict[ d[i][0] ] = row[i]
        
                print row_dict


if __name__ == '__main__':

    ipJSON = interpretedJson_class()
    