'''
Created on 22.01.2012


    use Counters to find out which dimensions of the impression
    vector might be interesting 



@author: karisu
'''

from contest.config import config_local, config_global
import cql
from cql.cassandra import Cassandra
from baseModel import baseModel
from contest.packages.helper.getTimestamp import getTimestamp
import time
import bisect
from sets import Set

class distributedCounters(baseModel):
    """
    global_counter for items, user
    time_bined counter for items, user
    """

    def __init__(self, flattenedJson = None, timestamp = None):
        '''
        Constructor
        '''
        super(distributedCounters, self).__init__()
        self.columnfamily = config_global.dbname_distributedCounter
        self.flattenedJson = flattenedJson
        
        try:
            self.timestamp = timestamp 
        except:
            self.timestamp = int( flattenedJson['item_created'])
            """ use the item created time instead """
    
        try:
            self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
                        
        except cql.ProgrammingError as programmingError:
            print programmingError
            
        """ at first the data has to be quantisized, i.e. impressions of users on some hours """
        
    
    def increment(self):
        try:
            self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
                        
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        """ the total impression and domain_id counter will actually count the same numbers
        because we only have a single domain_id currently """

        try:
            user_key = 'client_id:' + str((self.flattenedJson['client_id']))
            self.conn.cursor.execute( """BEGIN BATCH USING CONSISTENCY ONE
                UPDATE :columnfamily SET total_impression = total_impression + 1 WHERE key = :user_id
                UPDATE :columnfamily SET total_impression = total_impression + 1 WHERE key = total_impression
                APPLY BATCH
                """, dict(columnfamily = config_global.dbname_distributedCounter,
                          user_id = user_key
                          )
                        
                )
        except cql.ProgrammingError as programmingError:
            print "problem with batch execute of distributed Counters: " + programmingError
            # UPDATE :columnfamily SET count_y = count_y + 1 WHERE key = 'test_counter'
            
            
            
    def increment_by_collumn(self):
        try:
            self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
                        
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        currentTime = self.timestamp
            
        minutesSince1970 = int (currentTime / 60 )
        hoursSince1970 = int( currentTime / (60 * 60) )
        daysSince1970 = int( currentTime / ( 60 * 60 * 24 ) )
        
        try:
            user_id = (self.flattenedJson['client_id'])
        except:
            user_id = None
            print "no user id given in distributed Counters"
        
        try: 
            item_id = (self.flattenedJson['item_id'])
        except:
            print "no item id given in distributed Counters"
        try:
            domain_id = self.flattenedJson['domain_id']
        except:
            print "no domain id given in distributed Counters"

    
    
        if (not ( 'item_id' in self.flattenedJson)) :
            """
            save the user impressions by time bin
            """    
            try:
                self.conn.cursor.execute( """BEGIN BATCH USING CONSISTENCY ONE
                    UPDATE :columnfamily SET :user_id = :user_id + 1 WHERE key = user_ids_by_hours_:hoursSince1970
                    UPDATE :columnfamily SET :user_id = :user_id + 1 WHERE key = user_ids_by_minutes_:minutesSince1970
                    UPDATE :columnfamily SET :user_id = :user_id + 1 WHERE key = user_ids_by_days_:daysSince1970
                    APPLY BATCH
                    """, dict(columnfamily = config_global.dbname_distributedCounter,
                              user_id = (self.flattenedJson['client_id']),
                              minutesSince1970 = minutesSince1970,
                              daysSince1970 = daysSince1970,
                              hoursSince1970 = hoursSince1970
                               ) )
            except cql.ProgrammingError as programmingError:
                print "problem with batch execute of distributed Counters: " + programmingError
        
                 
        else:
            """ if there is an item in the data """
            try:
                
                cql_query = """ UPDATE :columnfamily SET :user_id = :user_id + 1 WHERE key = user_ids_by_hours_:hoursSince1970
                    UPDATE :columnfamily SET :user_id = :user_id + 1 WHERE key = user_ids_by_minutes_:minutesSince1970
                    UPDATE :columnfamily SET :user_id = :user_id + 1 WHERE key = user_ids_by_days_:daysSince1970
                    UPDATE :columnfamily SET :item_id = :item_id + 1 WHERE key = item_ids_by_hours_:hoursSince1970
                    UPDATE :columnfamily SET :item_id = :item_id + 1 WHERE key = item_ids_by_minutes_:minutesSince1970
                    UPDATE :columnfamily SET :item_id = :item_id + 1 WHERE key = item_ids_by_days_:daysSince1970 """
                
                if ('domain_id' in self.flattenedJson):
                    cql_query = cql_query + """ UPDATE :columnfamily SET :domain_id = :domain_id + 1 WHERE key = domain_ids_by_days_:daysSince1970 """
                self.conn.cursor.execute( """BEGIN BATCH USING CONSISTENCY ONE """ +
                    cql_query + 
                    """ APPLY BATCH
                    """, dict(columnfamily = config_global.dbname_distributedCounter,
                              user_id = (self.flattenedJson['client_id']),
                              item_id = (self.flattenedJson['item_id']),
                              domain_id = (self.flattenedJson['domain_id']),
                              minutesSince1970 = minutesSince1970,
                              daysSince1970 = daysSince1970,
                              hoursSince1970 = hoursSince1970
                               ) )
            except cql.ProgrammingError as programmingError:
                print "problem with batch execute of distributed Counters: " + programmingError

        """
        save the item impressions by time bin
        """
        try:
            self.conn.cursor.execute( """BEGIN BATCH USING CONSISTENCY ONE
                UPDATE :columnfamily SET :item_id = :item_id + 1 WHERE key = item_ids_by_hours_:hoursSince1970
                UPDATE :columnfamily SET :item_id = :item_id + 1 WHERE key = item_ids_by_minutes_:minutesSince1970
                UPDATE :columnfamily SET :item_id = :item_id + 1 WHERE key = item_ids_by_days_:daysSince1970
                APPLY BATCH
                """, dict(columnfamily = config_global.dbname_distributedCounter,
                          item_id = (self.flattenedJson['item_id']),
                          minutesSince1970 = minutesSince1970,
                          daysSince1970 = daysSince1970,
                          hoursSince1970 = hoursSince1970
                           ) )
        except cql.ProgrammingError as programmingError:
            print "problem with batch execute of distributed Counters: " + programmingError
        
    
    
    def getMostImportant(self, dimension, binSize, timestampFrom, timestampTo = None):
        """
        access the distributed counters to find the most important user, item etc in that time period
        """
        
        """ UPDATE :columnfamily SET :user_id = :user_id + 1 WHERE key = users_byHour_:hoursSince1970 """
        
        base_key = dimension + "_by_" + binSize + "_"
        "user_ids_by_hour_0"
        if ( ( timestampTo == None ) or ( timestampTo - timestampFrom < 1 ) ):
            cql_query = """ SELECT * FROM :columnfamily WHERE key = :dimension_key """
            
            key = base_key + str(timestampFrom)
            d = dict(columnfamily = config_global.dbname_distributedCounter,
                     dimension_key = key
                 )
            self.conn.cursor.execute(cql_query, d)
            
        else :
            cql_query = """ SELECT * FROM :columnfamily WHERE key in :dimension_key """
            
            timerange = tuple( xrange(timestampFrom, timestampTo+1) )
            keylist = [base_key + str( binId ) for binId in timerange ]
            keylist = tuple(keylist)
            
            d = dict(columnfamily = config_global.dbname_distributedCounter,
                     dimension_key = keylist
                 )
            self.conn.cursor.execute(cql_query, d)
        
        
        # for key, element in idlist.items():
        element = self.conn.cursor.fetchone()
        description = self.conn.cursor.description
        resultSet = {}
        index_list = Set([])
        
        while element:
            if ( len( element) > 1 ) :
                resultSet[ element[0] ] = []
                for index in xrange(1, len(element)):
                    resultSet[ element[0] ].append( tuple([ description[index][0], element[index] ]) )
                resultSet[ element[0] ].sort(self.inplaceComp)
            
            element = self.conn.cursor.fetchone()
            description = self.conn.cursor.description
            
        

        
            
        return resultSet
        # d = self.conn.cursor.description
        #trans = {}
        #for i in xrange(len(x)):
        #    trans[ d[i][0] ] = x[i]
        #print x
        #self.conn.cursor.description
        
        
    def inplaceComp(self, x, y):
                """ do some sorting """
                if x[1] > y[1]:
                    return -1
                if x[1] < y[1]:
                    return 1
                else: return 0
    
if __name__ == '__main__':
    
    pass