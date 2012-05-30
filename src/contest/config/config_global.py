
'''
Created on 16.12.2011

@author: karisu
'''
import cql
from cql.cassandra import Cassandra

cassandra_default_keyspace = 'plistaContest'
cassandra_test_keyspace = 'plistaTest'
#cassandra_default_keyspace = cassandra_test_keyspace


""" database names """
dbname_rawJson = "rawJsonDump"
dbname_interpretedJson = "interpretedJson"
dbname_itemByUserId = "itemsByUserId"
dbname_usersByItemId = "usersByItemId"
dbname_dimensionList = "dimensionList"
dbname_dimensionList_rowKeys = ["client_id", "browser_id", "domain_id", "item_id"]
dbname_recommendationsList = 'recommendationList' 

""" this is the central store for incoming messages in their raw format
it is just for backup purposes and later integeration tests
"""

dbname_message_ids = "incoming_messages"
dbname_itemModel = "itemTableFull"
dbname_distributedCounter = "distributedCounter"

""" Users by Time """
dbname_userLogByMicroSec = "userLogByMicroSec" 
dbname_userLogByMicroSec_Description = "this is the raw log for all user activities. It will express the time and the item an user has seen"
dbname_userLogByMinutes_One = "userLogByMinutes_One" 
dbname_userLogByMinutes_Ten = "userLogByMinutes_Ten"
dbname_userLogByHours_One = "userLogByHours_One"

dbnames_userLogList = [dbname_userLogByMicroSec,
                    dbname_userLogByMinutes_One,
                    dbname_userLogByMinutes_Ten,
                    dbname_userLogByHours_One]


""" rabbitMQ configuration """
config_rabbitmq_server = 'localhost'