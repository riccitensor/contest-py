'''
Created on 28.01.2012

@author: christian.winkelmann@plista.com
'''

import time

from contest.packages.models.distributedCounters import distributedCounters
from contest.packages.models.DimensionListModel import DimensionListModel

class ContestReplayAnalytics(object):
    '''
    Analyse the data which was replayed from the contest data. That implies you have a database full data by 
    i.e. using the "replayFromMysql.py" script
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    
        
        
        
if __name__ == '__main__':
    
    """ show us all user ids """
    #dL = DimensionListModel(config_global.dbname_dimensionList_rowKeys[0])
    #client_ids = dL.getAll()
    #print "number of clients:\t" + str( len(client_ids[1]) )
    
    #dL = DimensionListModel(config_global.dbname_dimensionList_rowKeys[3])
    #item_ids = dL.getAll()
    #print "number of items:\t" + str( len(item_ids[1]) )
    
    timestampStart = 1318415675
    timestampEnd = 1318421723
    
    """
    some helping times
    01.10.2011 as timestamp in seconds
    
    2011-10-26 10:17:37
    1319617057
    
    2011-10-26 10:23:44
    1319617424
    hours: 366560
    
    2011-10-26 12:26:01
    1319624761
    hours: 366562
    
    2011-10-26 13:53:33
    1319630013
    
    
    2011-10-27 15:21:41
    1319721701
    
    """ 
    
    dL = DimensionListModel('user_ids', mode = 'redis')
    """
    userList = dL.getByTime(1319617057, 1319617424, binSize = 'seconds')
    print len( userList ) """
    
    
    first_computation = time.time()
    userList = dL.getByTime(366560, 366562, binSize = 'hours', renew = True)
    print "\nhour bin"
    print len( userList )
    first_computation = time.time() - first_computation
    print first_computation
    
    second_computation = time.time()
    userList = dL.getByTime(366560, 366562, binSize = 'hours', renew = False )
    print "\nhour bin"
    print len( userList )
    
    for userList_element in userList:
        #print userList_element
        #print len( userList[userList_element] )
        #print userList[userList_element]
        pass

    second_computation = time.time() - second_computation
    print second_computation
    
    dimension = 'user_ids'
    binSize = 'hours'
    timestampFrom = 0
    print "most important"
    dC = distributedCounters()
    most_important_users = dC.getMostImportant(dimension, binSize, 366560, 366561)
    #for most_important_users_element in most_important_users:
        #print "most important users"
        #print most_important_users_element
        #print most_important_users[most_important_users_element]
    
    #print "most important users"
    #print len(most_important_users)
    #print most_important_users
        
    
    
    
    
    
    """
    dL = DimensionListModel('user_ids')
    userList = dL.getByTime(1319617057, 1319624761, binSize = 'seconds')
    print len( userList )
    """
    
    """
    timestampStartMinute = getTimestamp.gettimeStampIn_1_Minute(timestampStart)
    timestampEndMinute = getTimestamp.gettimeStampIn_1_Minute(timestampEnd)
    dL = DimensionListModel('user_ids')
    userList = dL.getByTime(timestampStartMinute, timestampEndMinute, binSize = 'minutes')
    print "minute bins"
    print len( userList )
    print userList
    """
    
    """
    timestampStartHour = getTimestamp.gettimeStampIn_Hours( timestampStart )
    timestampEndHour = getTimestamp.gettimeStampIn_Hours( timestampEnd )
    dL = DimensionListModel('user_ids')
    userList = dL.getByTime(timestampStartHour, timestampEndHour, binSize = 'hours')
    print "\nhour bin"
    print len( userList )
    print userList
    
    
    dC = distributedCounters()
    dimension = 'user_ids'
    binSize = 'hours'
    print "\nmost important"
    print dC.getMostImportant(dimension, binSize, timestampStartHour, timestampEndHour)
    """
    
    #dL = DimensionListModel('days')
    #days = dL.getAll()
    #print "number of days:\t\t" + str( len(days[1]) )
    
    
    """ show us all item ids """
    
    """ give us the most viewed items """
    