'''
Created on 11.02.2012

Using native Secondary Indizes in Cassandra is a messy thing. 
Using Bitmap Indizes might be an idea
B-Tree Indizes might be better but are hard to implement in Key/Value Store

BUT we can flatten the B-Tree to just a long key which saves path traversal
Idea:

Root -> Gender:male -> List of Keys
Root -> Gender:female -> List of Keys
Root -> Lives:Hamburg -> List of Keys
Root -> Lives:Berlin -> List of Keys
Root -> Lives:Cologne -> List of Keys
Root -> Gender:male -> Lives:Hamburg -> List of Keys
Root -> Gender:male -> Lives:Berlin -> List of Keys
Root -> Gender:male -> Lives:Cologne -> ...
Root -> Gender:female -> Lives:Hamburg -> ... 
Root -> Gender:female -> Lives:Berlin -> ...
Root -> Gender:female -> Lives:Cologne -> ...

The complexity to update shouldn't be higher then in a graph database. 

======================================================================
Now, we are getting a real Insert

Now, we are getting a real Update
 

@author: christian.winkelmann@plista.com
'''

from config import config_global
from config import config_local
import cql
from cql.cassandra import Cassandra
from baseModel import baseModel
from packages.helper.getTimestamp import getTimestamp
import time
from sets import Set


class SecondaryIndex(baseModel):
    '''
    build a secondary Index based on a flattened b-tree 
    '''


    def __init__(self):
        '''
        Constructor
        '''


    def select(self, condition = dict() ):
        
        indexkey = ""
        
        for key,value in condition.items():
            indexkey = key + ":" + value + "-" +  indexkey
            
        print indexkey
            
        
        
        
        
        
if __name__ == '__main__':
    conditions = {'location':'berlin', 'gender':'male'}
    sI = SecondaryIndex()
    sI.select(conditions)