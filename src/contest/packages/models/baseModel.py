'''
Created on 25.12.2011

@author: christian.winkelmann@plista.com
'''
from contest.config import config_global
from contest.config import config_local
import cql 
import redis
from contest.packages.designPatterns import Singleton
from contest.config.cassandraConnection import CassandraConnection

class RedisConnection(object):
	pass


class baseModel(object):
    '''
    base Model connection
    '''

    def __init__(self, mode = 'cassandra'):
        '''
        Constructor
        '''
        
        if ( mode == 'cassandra' ):
            self.conn = CassandraConnection()
        else:
            if ( mode == 'redis' ):
                #self.conn = redis.Redis("localhost")
				self.conn = RedisConnection() #redis.Redis("localhost")
        
    def save(self):
        """ to overload this function """
        return "now it should be saved"
    
    def get(self):
        """ get something """
        return " I got something "
        
