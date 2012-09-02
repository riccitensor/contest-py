'''
Created on 09.01.2012

@author: christian.winkelmann@plista.com
test the maximum amount of counter increments per second
'''
import time
#from pycassa.types import UTF8Type, LongType
#from models.itemModel import itemModel
from contest.packages.models.itemModel import itemModel 

from contest.config import config_global
from contest.config import config_local
import cql


dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
item_id = 1

cursor = dbconn2.cursor()
cursor.execute("USE plistaContest")

""" cursor.execute("
        CREATE COLUMN FAMILY CounterCF (KEY text PRIMARY KEY, count_me counter)
            WITH comparator = ascii AND default_validation = counter;
    ")

"""
#cursor.execute("INSERT INTO CounterCF (key) VALUES ('counter1');")
currentTime = time.time()
increments = 1000
for i in xrange( increments ):
    
    #cursor.execute("UPDATE CounterCF USING CONSISTENCY ONE SET count_me = count_me + 2 WHERE key = 'counter1'")
    #cursor.execute("UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter2'")
    #cursor.execute("UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter3'")
    cursor.execute( """BEGIN BATCH USING CONSISTENCY ONE
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter1'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter2'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter3'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter4'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter5'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter6'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter7'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter8'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter9'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter10'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter11'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter12'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter13'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter14'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter15'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter16'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter17'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter18'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter19'
    UPDATE CounterCF SET count_me = count_me + 2 WHERE key = 'counter20'
    APPLY BATCH
    """)
    
    
cursor.execute("SELECT * FROM CounterCF WHERE KEY = 'counter1'")
print cursor.rowcount
print time.time() - currentTime
print "increments per second :\t" + str( increments / (time.time() - currentTime) )
r = cursor.fetchone()
print r
