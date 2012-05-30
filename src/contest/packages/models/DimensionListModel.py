'''
Created on 21.01.2012

Columnfamily to store all points in dimensions which like items, users, messages, browser, days, hours this will serve 
as an index

instead of just saving just the global list of dimension items it will save kind of histograms in blocks of
time
This obsoletes "userByTime"


There are loads of types here: stream By Milliseconds hours, days, months, years, allTime 

To make the computation of the bins fast we are using a continous query pattern


@author: christian.winkelmann@plista.com
'''
from contest.config import config_global
from contest.config import config_local
import cql
from cql.cassandra import Cassandra
from baseModel import baseModel
from contest.packages.helper.getTimestamp import getTimestamp
import time
from sets import Set


class DimensionListModel(baseModel):
    
    mode_cassandra = True
    mode_riak = False
    mode_redis = False
         
    
    def __init__(self, dimensionName, mode):
        """ @param dimensionName: The name of the dimension like user_id, impression_id, browser_id...
        """
        super(DimensionListModel, self).__init__()

        self.column_family = config_global.dbname_dimensionList
        self.dimensionList = config_global.dbname_dimensionList_rowKeys
        
        self.dimensionName = dimensionName
        self.binSize = 'seconds'
        
        self.default_key = self.dimensionName + "_by_" + self.binSize 
        
        self.list = dict() # the dictionary which holds
        self.user_ids = 'user_ids'
            
        
    
    def save(self, dimension_id, timestamp, binSize = 'seconds'):        
        """ add ids to the columnfamily """
        
        self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
        #key = self.default_key + "_" + str(timestamp)
        key = self.dimensionName + "_by_" + binSize + "_" + str(timestamp) 
        if ( binSize == 'minutes'):
            print ""
        
        try:        
                self.conn.cursor.execute("""INSERT INTO :table ( dimension_name, :dimension_id ) VALUES 
                        ( :dimension_name, 0)""", 
                                            dict(table=config_global.dbname_dimensionList,
                                                 dimension_name = key,
                                                 dimension_id = dimension_id
                                                 ) 
                                           )
     
            
        except cql.ProgrammingError as programmingError:
            print programmingError
    

            
    #self.dL.binify('minutes', 0, 1)
    def binify(self, target, fromTime, toTime = None, origin = 'seconds'  ):
        """ push the data into bin according the binsize 
            @param: binsize like minutes or hours
            @param: fromTime starting Point
            @param: toTime endPoint
        """
        
        
        
        """ get the whole range at once """
        """ @todo: these following function should be dependent from the origin """
        if ( target == 'minutes'):
            fromTime_origin = getTimestamp.getTimeStampFromMinutes(fromTime)
            toTime_origin = getTimestamp.getTimeStampFromMinutes(toTime)
            idlist = self.getByTime( fromTime_origin, toTime_origin, 'seconds')
        
        if ( target == 'hours'):
            fromTime_origin = getTimestamp.getTimeStampFromHours(fromTime)
            toTime_origin = getTimestamp.getTimeStampFromHours(toTime)
            idlist = self.getByTime( fromTime_origin, toTime_origin, 'seconds')
            
        if ( target == 'days'):
            fromTime_origin = getTimestamp.getTimeStampFromDays(fromTime)
            toTime_origin = getTimestamp.getTimeStampFromDays(toTime)
            idlist = self.getByTime( fromTime_origin, toTime_origin, 'seconds')
            
        if ( target == 'weeks'):
            fromTime_origin = getTimestamp.getTimeStampFromWeeks(fromTime)
            toTime_origin = getTimestamp.getTimeStampFromWeeks(toTime)
            idlist = self.getByTime( fromTime_origin, toTime_origin, 'seconds')

        """ now we have a list of all """
        target_list = Set([])
        
        for key, element in idlist.items():
            target_list = target_list.union( Set(element) )
            
            
        for dimension_id in target_list:
            self.save(dimension_id, fromTime, target )   
             
        self.setComputedIds(self.dimensionName, fromTime, toTime, target)

        return list
        
        
    def getByTime(self, timestampStart, timestampEnd = None, binSize = 'seconds', renew = False):
        """ grab all entries for the dimensions
        @param: timeStampStart start of range or single point 
        @param: timeStampEnd end of the range
        @param: binSize default ist seconds otherwise aggregated data is requested """
        self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
        
        if (binSize == 'seconds'):
            """ we access the raw data """
        
        else:
            """ if the binsize is not seconds, there is a chance it is already computed and therefore doesn'have to 
            be computed again """
            
            r = self.getComputedIds(self.dimensionName, timestampStart, timestampEnd, binSize)
            """ according to the result we might need to compute something """
            #print r

            requestIdRange = list(xrange(timestampStart,timestampEnd+1))
            if (not renew):
                for rIR in requestIdRange:
                    if (rIR in r):
                        requestIdRange.remove(rIR)                       
            else:
                pass
                
            for i in requestIdRange:
                self.binify(binSize, i, i+1)
                


  
        if ( timestampStart != None and timestampEnd != None ) :
            
            
            # origin = 'seconds'
            origin = binSize
            ids = getTimestamp.convertTimeStampsPairToRange(timestampStart, timestampEnd, binSize, origin)
            basekey = self.dimensionName + "_by_" + binSize + "_"
            if len(ids) > 1 :
                """ check for the lists """
                ids = [basekey + str(id) for id in ids]
                ids = tuple(ids)
                
                self.conn.cursor.execute("SELECT * FROM :table WHERE dimension_name in :ids", 
                                                 dict(table=self.column_family,
                                                      ids = ids
                                                      ))
            
            else:
                """ in case there is only one result """
                ids = ids[0]
                ids = basekey + str(ids)
                self.conn.cursor.execute("SELECT * FROM :table WHERE dimension_name = :ids", 
                                                 dict(table=self.column_family,
                                                      ids = ids
                                                      ))

        """ interpret the result since the format suck """
        self.dict = {}
        r = self.conn.cursor.fetchone()
        d = self.conn.cursor.description
        while r :
            if ( len(r) > 1):
                self.dict[ r[0] ] = []
                for i in xrange(1, len(r)):
                    self.dict[ r[0] ].append( d[i][0] )
            r = self.conn.cursor.fetchone()
            d = self.conn.cursor.description
            
        return self.dict

   
    
    def getComputedIds(self, dimension, rangeStart = None, rangeEnd = None, binSize = 'minutes'):
        """ to monitor which computation have been done already and therefore results should exist
        """
        self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
            
        key = self.dimensionName + "_by_" + binSize + "_done"
    
        cql_query = "SELECT * FROM :table WHERE dimension_name = :dimension_name"
        self.conn.cursor.execute(cql_query, 
                                             dict(table=self.column_family, 
                                                  dimension_name = key
                                                  ))
        r = self.conn.cursor.fetchone()
            
        return r[1:]
                
    
    def setComputedIds(self, dimension, rangeStart, rangeEnd = None, binSize = 'minutes'):
        """ set the ids which indicated which data was already computed 
        """
        self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
            
        key = self.dimensionName + "_by_" + binSize + "_done"
        timerange = getTimestamp.convertTimeStampsPairToRange(rangeStart, rangeEnd, binSize, binSize )
        for dimension_id in timerange:
            cql_query = """UPDATE :table SET :dimension_id = :dimension_id WHERE dimension_name = :dimension_name """
            self.conn.cursor.execute(cql_query, 
                                                 dict(table=self.column_family, 
                                                      dimension_name = key,
                                                      dimension_id = dimension_id
                                                      ))
                
    
if __name__ == '__main__':
    """ just try to get a full list from the given dimension """
     
    try:
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port ) 
        cursor = dbconn.cursor()
    
    except:
        print "not able to create a database connection"
    
    cursor.execute("USE " + config_global.cassandra_default_keyspace)
    
    #config_global.dbname_dimensionList_rowKeys[0]
    #dL = DimensionListModel(config_global.dbname_dimensionList_rowKeys[0])
    dL = DimensionListModel('user_ids')

    timestamp = int( time.time() )
    for i in xrange(70):
        id = 2
        curr_timestamp = timestamp + i 
        dL.save( id, curr_timestamp )
    
    
    binId = getTimestamp.gettimeStampIn_Hours( timestamp )
    
    print timestamp
    print dL.getByTime(timestamp-60, timestamp+50)
    
    #dL.save_bin(1, 'hours', binId)
    
    print getTimestamp.getTimeStampFromHours( binId )
    
    #print dL.getAll()
    print "binbify"
    x = ( dL.binify('hours', binId-1, binId) )
    print len( x )
    
    
