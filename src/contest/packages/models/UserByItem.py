'''
Created on 21.01.2012

Columnfamily to store all items which has been seen by a user_id

This going to be hard at aggregation level, because the request might be:

give me all users for certain items in the last 12 hours in hour blocks

@author: christian.winkelmann@plista.com
'''
from contest.config import config_global
from contest.config import config_local
import cql
from cql.cassandra import Cassandra
from baseModel import baseModel
from contest.packages.helper.getTimestamp import getTimestamp


class UserByItem(baseModel):
    
    mode_cassandra = True
    mode_riak = True
         
    
    def __init__(self, item_id, check = False):
        super(UserByItem, self).__init__()

        self.column_family = config_global.dbname_usersByItemId
        self.item_id = item_id
        
        """ don't check if the item is already in the database """
        if (not check):
            try:
                self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
                self.conn.cursor.execute( "SELECT * FROM " + self.column_family + ' USING CONSISTENCY ANY WHERE item_id = :item_id ', 
                                          dict(item_id = self.item_id) )
                            
            except cql.ProgrammingError as programmingError:
                print programmingError
        
 
    def save(self, user_id):
        self.conn.cursor.execute("""USE :keyspace""", dict(keyspace = config_global.cassandra_default_keyspace))
        currentTime = getTimestamp.gettimeStampInMicroseconds()        
        self.conn.cursor.execute(""" INSERT INTO :table (item_id, :currentTime) 
                                    VALUES (:item_id, :user_id) """, 
                            dict(table=config_global.dbname_usersByItemId, 
                            currentTime = currentTime,
                            item_id = self.item_id,
                            user_id = user_id
                            ) 
                           )

    def getAll(self):
        self.conn.cursor.execute("""USE :keyspace""", dict(keyspace = config_global.cassandra_default_keyspace))
        self.conn.cursor.execute("SELECT * FROM :table WHERE item_id = :item_id", 
                                 dict(table=config_global.dbname_usersByItemId, item_id = self.item_id))
        print self.conn.cursor.fetchall()
        print self.conn.cursor.description
    



if __name__ == '__main__':
    """ at first we are excluding all those dangerous statements since the server runs already """ 
     
    try:
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port ) 
        cursor = dbconn.cursor()
    
    except:
        print "not able to create a database connection"
    
    cursor.execute("USE " + config_global.cassandra_default_keyspace)
    
    uBI = UserByItem(item_id = 7)
    uBI.save( user_id = 1 )
    uBI.save( user_id = 2 )
    
    print uBI.getAll()
    
    
