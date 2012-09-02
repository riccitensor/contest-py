'''
Created on 25.01.2012

Columnfamily to store a list of all messages and their ids


@author: christian.winkelmann@plista.com
'''
from config import config_global
from config import config_local
import cql
from baseModel import baseModel
from packages.helper.getTimestamp import getTimestamp


class MessageIdList(baseModel):
    
    mode_cassandra = True
    mode_riak = True
         
    
    def __init__(self):
        super(MessageIdList, self).__init__()

        self.column_family = config_global.dbname_message_ids        
        try:
            self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
        except cql.ProgrammingError as programmingError:
            print programmingError
        
 
 
    def save(self, impression_id):        
        currentTime = getTimestamp.gettimeStampInMicroseconds()        
        self.conn.cursor.execute(""" INSERT INTO :table ( KEY , :currentTime) 
        VALUES (impression_list, :impression_id) """, 
                        dict(table=self.column_family, 
                        currentTime = currentTime,
                        impression_id = impression_id

                        ) 
                       )
        
    def getNOldest(self, N = 3, ):
        #self.conn.cursor.execute("""USE )
        self.conn.cursor.execute("SELECT FIRST :number * FROM :table WHERE KEY = 'impression_list'", 
                   dict(table=self.column_family,
                        number = N
                   ) )
        result = self.conn.cursor.fetchone()
        #print self.conn.cursor.description
        return result
        
if __name__ == '__main__':
    """ at first we are excluding all those dangerous statements since the server runs already """ 
     
    try:
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port ) 
        cursor = dbconn.cursor()
    
    except:
        print "not able to create a database connection"
    
    cursor.execute("USE " + config_global.cassandra_default_keyspace)
    
    uBI = MessageIdList()
    uBI.save( impression_id = 1 )
    uBI.save( impression_id = 2 )
    uBI.save( impression_id = 3 )
    uBI.save( impression_id = 4 )
    
    print uBI.getNOldest(3)
    
    
