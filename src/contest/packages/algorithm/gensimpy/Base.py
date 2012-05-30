'''
Created on 26.11.2011

@author: karisu
'''

#import logging
#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
#
#from gensim.similarities.simserver import SessionServer
#from gensim import utils
#
#import sqlite3
#import sqlitedict
#import time

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.similarities.simserver import SessionServer
from gensim import utils

import sqlite3
import sqlitedict
import time
import redis

class Base( object ):
    '''
    classdocs
    '''
    
    s_redis_new_item_list = "s_new_semantic_items_" 
    h_redis_itemid_document_text = "h_redis_itemid_document_text_"
    
    training_id = None
    base_url = None
    test = None
    local_execution = None

    def __init__( self, training_id, db_location, local_execution ):
        '''
        Constructor
        '''
        self.training_id = "5"
        self.base_url = "localhost:5002"
        self.test = "test"
        self.training_id = training_id
        self.sqlserver = db_location + 'Training' + str(training_id)  + '.db'
        self.rootlocation = db_location
        self.local_execution = local_execution
        
        self.redis_con = redis.Redis("localhost")
        self.s_redis_new_item_list + str(training_id)
        self.h_redis_itemid_document_text + str(training_id)
        
    def test(self):
            
        """
        """
      
      
      
if __name__ == '__main__':
    print "bla"

  