'''
Created on 21.01.2012

Columnfamily to store all items which has been seen by a user_id

This will be used for user based collaborative filtering 


@author: christian.winkelmann@plista.com
'''
from contest.config import config_global
from contest.config import config_local
import cql
from baseModel import baseModel


class ItemsByUser(baseModel):
    
    mode_cassandra = True
    mode_riak = True
         
    
    def __init__(self, user_id, timeStamp = None):
        super(ItemsByUser, self).__init__()

        self.column_family = config_global.dbname_itemByUserId
        self.user_id = user_id
        
        self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
        
        self.basekey = "user_id_" + str( self.user_id )
        
        if (timeStamp != None):
            self.timeStamp = timeStamp
            self.currentTimeS = int( self.timeStamp )
            self.minutesSince1970 = int (self.currentTimeS / 60 )
            self.hoursSince1970 = int( self.currentTimeS / (60 * 60) )
            self.daysSince1970 = int( self.currentTimeS / ( 60 * 60 * 24 ) )
            self.weeksSince1970 = int( self.currentTimeS / ( 60 * 60 * 24 * 7 ) )
        
        #try:
        #    self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
        #    self.conn.cursor.execute( """SELECT * FROM """ + self.column_family + """ USING CONSISTENCY ANY 
        #    WHERE user_id = :user_id """, 
        #                              dict(user_id = user_id) )
                        
        #except cql.ProgrammingError as programmingError:
        #    #print programmingError
        #    pass
    
        #r = self.conn.cursor.fetchone()
        #d = self.conn.cursor.description
        #print r
        #for i in xrange(len(r)):
            #self.item_table_dict[ d[i][0] ] = r[i]
            #print r
            
        
    def save(self, item_id):        
        
        self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
        
        base_key = self.basekey 
        key_all = base_key + "_all"
        
        
        key_days = base_key + "_days_" + str(self.daysSince1970)
        key_weeks = base_key + "_weeks_" + str(self.weeksSince1970)
        
        try:   
            cql_query = """ BEGIN BATCH USING CONSISTENCY ONE 
            UPDATE :table SET :item_id = :item_id + 1  WHERE KEY = :key_all 
            UPDATE :table SET :item_id = :item_id + 1  WHERE KEY = :key_weeks
            UPDATE :table SET :item_id = :item_id + 1  WHERE KEY = :key_days
            APPLY BATCH """
            self.conn.cursor.execute(cql_query, 
                                dict(table=config_global.dbname_itemByUserId, 
                                currentTime = self.currentTimeS,
                                key_all = key_all,
                                key_weeks = key_weeks,
                                key_days = key_days,
                                item_id = item_id
                                ) 
                               )
        except cql.ProgrammingError as programmingError:
            print programmingError


    def get(self, binSize = 'all', binId = None):
        """ get all items an user has seen. If wanted return only the one in the given timeframe """
        self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
        
        
        key = self.basekey + "_" + binSize 
        cql_query = """ SELECT * FROM :table WHERE KEY = :key """
        self.conn.cursor.execute(cql_query, 
                                 dict(table=config_global.dbname_itemByUserId, 
                                      key = key))
        
        element = self.conn.cursor.fetchone()
        description = self.conn.cursor.description
        resultSet = {}
        
        while element:
            if ( len( element) > 1 ) :
                resultSet[ element[0] ] = []
                for index in xrange(1, len(element)):
                    #resultSet[ element[0] ].append( tuple([ description[index][0], element[index] ]) )
                    resultSet[ element[0] ].append( description[index][0] )
                
            
            element = self.conn.cursor.fetchone()
            description = self.conn.cursor.description

        return resultSet    
    
if __name__ == '__main__':
    """ at first we are excluding all those dangerous statements since the server runs already """ 
     
    try:
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port ) 
        cursor = dbconn.cursor()
    
    except:
        print "not able to create a database connection"
    
    cursor.execute("USE " + config_global.cassandra_default_keyspace)
    
    iBU = ItemsByUser(user_id = 7)
    iBU.save( item_id = 1 )
    iBU.save( item_id = 2 )
    
    print iBU.getAll()
    
    
