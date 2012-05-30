'''
Created on 27.01.2012

@author: christian.winkelmann@plista.com
'''

class RollOut(object):
    '''
    Main Location to Rollout the migrations. 
    '''


    def __init__(self):
        '''
        Constructor
        '''
from setup_keyspaces import Setup_Keyspaces
    
from _001_itemTableFull_Class import itemTableFull_Class
from _002_rawJsonDump_Class import rawJsonDump_Class
from _003_interpreted_JSON import interpretedJson_class
from _004_itemsByUserId import ItemByUserId
from _005_usersByItemId_Class import UserByItemId
from _006_distributedCountersMigration import DistributedCountersMigration
from _007_dimensionLists import dimensionListsMigration
#from _008_usersByTimeMigration import UsersByTime_Migration
from _009_message_id import Message_ID_Migration

if __name__ == '__main__':
    
    sK = Setup_Keyspaces()
    
    iTF = itemTableFull_Class()
    rJD = rawJsonDump_Class()
    ipJ = interpretedJson_class()
    
    iBUI = ItemByUserId()
    uBI = UserByItemId()
    dC = DistributedCountersMigration()
    
    dL = dimensionListsMigration()
    
#   uBT = UsersByTime_Migration()
#    mI = Message_ID_Migration() # we probably don't need this because it is just a dimensionAsWell

    
    
    
    
    
    