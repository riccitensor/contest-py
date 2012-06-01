'''
Created on 15.01.2012

@author: karisu
'''
import time
#import datetime
from datetime import date, datetime
from datetime import time as time2 

class getTimestamp(object):
    
    def __init__(self):
        """ nothing to do
        """
    
    @staticmethod    
    def gettimeStampInMicroseconds():
        """ since python doesn't support normal Unix timestamp we have to compute it on our own """
        nowplus = datetime.now()
        curr_time = time.time()

        unix_timestamp = int( nowplus.microsecond + ( curr_time*1000 ) ) 
        return unix_timestamp
        
    @staticmethod    
    def gettimeStampInSeconds():
        """ get all Seconds since 1970 """

        curr_time = int(time.time())
 
        return curr_time

    @staticmethod    
    def gettimeStampIn_1_Minute(timestamp = None):
        """ @param: timestamp in seconds since 1970
        get all Seconds quantizized in 10 minutes block """
        if ( timestamp == None ):
            curr_time = int(time.time() / ( 60 ))
        else:
            curr_time = int(timestamp / 60)
        return curr_time

    @staticmethod    
    def gettimeStampIn_10_Minutes(timestamp = None):
        """ get all Seconds quantizized in 10 minutes block """
        if ( timestamp == None):
            curr_time = int(time.time() / ( 60 * 10 ))
        else:
            curr_time = timestamp / ( 60 * 10)
            
        return curr_time
    
    @staticmethod    
    def gettimeStampIn_Hours(timestamp = None):
        """ get all Seconds quantizized in 10 minutes block """
        if ( timestamp == None ):
            curr_time = int(time.time() / ( 60 * 60 ))
        else:
            curr_time = timestamp / ( 60 * 60 )
        return curr_time
    
    @staticmethod    
    def gettimeStampIn_Days(timestamp = None):
        """ get all Seconds quantizized in 10 minutes block """
        if ( timestamp == None ):
            curr_time = int(time.time() / ( 60 * 60 *24))
        else:
            curr_time = timestamp / ( 60 * 60 * 24)
        return curr_time


    @staticmethod
    def getTimeStampFromWeeks( weeks ):
        """ given an hour compute the earliest timestamp which lies in this hour 
        """
        timestamp = ( weeks * 60 * 60 * 24 * 7 )
        return timestamp


    @staticmethod
    def getTimeStampFromDays( days ):
        """ given an hour compute the earliest timestamp which lies in this hour 
        """
        timestamp = ( days * 60 * 60 * 24 )
        return timestamp


    @staticmethod
    def getTimeStampFromHours( hours ):
        """ given an hour compute the earliest timestamp which lies in this hour 
        """
        timestamp = ( hours * 60 * 60 )
        return timestamp
    
    
    @staticmethod
    def getTimeStampFromMinutes( minute ):
        """ given a minute and compute the earliest timestamp which lies in this minute 
        """
        timestamp = ( minute * 60  )
        return timestamp

    @staticmethod
    def getTimeStampFromPythonDateTime( pdatetime = datetime.now()):
        timestamp = time.mktime(pdatetime.timetuple()) 
        #print timestamp 
        return int( timestamp )
        
        
        
    @staticmethod
    def convertTimeStampsPairToRange(timestampStart, timestampEnd, origin, target):
        """ helper function which gets a range from to 'timestamps' of the largers bin
        i.e. minute0 to minute1 -> (0,1,2,3,4,....,59)
        minute1 to minute2 -> (60,....119)
        minute0 to minute2 -> (0,...,119)
        @todo use global CONSTANTS like minutes = 60
        """
        factor = 1
        if (target == 'seconds'):
            if (origin == 'minutes'):
                factor = 60
            elif ( origin == 'hours'):
                factor = 3600
            elif ( origin == 'days'):
                factor = 86400
        
        
        if ( target == origin ):
            factor = 1
        
        timestampStart *= factor
        timestampEnd = timestampEnd * factor
        
        if ((timestampEnd - timestampStart) > 1 ):
            timestampRange = tuple(xrange(timestampStart, timestampEnd))
        else: timestampRange = [timestampStart] 
            
        
        return timestampRange

if __name__ == '__main__':
    
    kk = getTimestamp.getTimeStampFromPythonDateTime()
    """
    for i in xrange(2):
        print getTimestamp.gettimeStampInMicroseconds()
        
    for i in xrange(2):
        print getTimestamp.gettimeStampInSeconds()
        time.sleep(1.1)
        
    for i in xrange(2):
        print getTimestamp.gettimeStampIn_1_Minute()
        time.sleep(1.1)
    """
    
    timestampEnd = 1
    timestampStart = 0
    target = 'seconds'
    origin = 'hours'
        
    print getTimestamp.convertTimeStampsPairToRange(timestampStart, timestampEnd, origin, target)