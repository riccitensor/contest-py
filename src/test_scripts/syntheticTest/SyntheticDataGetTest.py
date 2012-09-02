'''
Created on 06.02.2012

Test if the where clauses in cassandra work as we want them
The result is dissappointing. Since multiple where conditions fail to result

@author: christian.winkelmann@plista.com
'''
import time
from contest.packages.models.itemModel import itemModel 

from contest.config import config_global
from contest.config import config_local
import cql
import random


class SyntheticDataGetTest():
#class SyntheticDataGetTest(unittest.TestCase):


    def setUp(self):
        print "bla"
        pass


    def tearDown(self):
        pass

    def warmUp(self):
        print "warmup"
        dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
    
        cursorb = dbconn2.cursor()
        cursorb.execute("USE plistaContest")
        


        cursorb.execute("""SELECT * FROM itemTableFull WHERE 
                            filter_a = 1 AND
                            filter_b = 1 AND
                            filter_c = 1 AND
                            filter_d = 1 
                            LIMIT 4""" )
        print "warmup done"
        print "\n\n"
        
    def testSynteticDataGet_filter_a(self):
        print "filter_a"
        dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
    
        cursorb = dbconn2.cursor()
        cursorb.execute("USE plistaContest")
        
        startTime = time.time()
        
        count = 300
        for n in xrange(count):
            filter_a_val = int( random.uniform(1,10) )
            cursorb.execute("""SELECT * FROM itemTableFull WHERE 
                            filter_a = :filter_a_val
                            LIMIT 4""", 
                            dict(filter_a_val = filter_a_val))
            resultset = cursorb.fetchall()
        endTime = time.time() - startTime
        print "endTime: \t" + str(endTime)
        
        print "requests per seconds:\t" + str ( count / endTime)
        
        resultset = cursorb.fetchall()
        #print resultset
        #print len(resultset)
        print "\n\n"
        
        
    def testSynteticDataGet_filter_b(self):
        print "filter_b"
        dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
    
        cursorb = dbconn2.cursor()
        cursorb.execute("USE plistaContest")
        
        startTime = time.time()
        
        count = 300
        for n in xrange(count):
            filter_b_val = int( random.uniform(1,100) )
            cursorb.execute("""SELECT * FROM itemTableFull WHERE 
                            filter_b = :filter_b_val
                            LIMIT 4""", 
                            dict(filter_b_val = filter_b_val))
            resultset = cursorb.fetchall()
        endTime = time.time() - startTime
        print "endTime: \t" + str(endTime)
        
        print "requests per seconds:\t" + str ( count / endTime)
        
        resultset = cursorb.fetchall()
        #print resultset
        #print len(resultset)
        print "\n\n"
        
        
    def testSynteticDataGet_filter_c(self):
        print "filter_c"
        dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
    
        cursorb = dbconn2.cursor()
        cursorb.execute("USE plistaContest")
        
        startTime = time.time()
        
        count = 300
        for n in xrange(count):
            filter_c_val = int( random.uniform(1,1000) )
            cursorb.execute("""SELECT * FROM itemTableFull WHERE 
                            filter_c = :filter_c_val
                            LIMIT 4""", 
                            dict(filter_c_val = filter_c_val))
            resultset = cursorb.fetchall()
        endTime = time.time() - startTime
        print "endTime: \t" + str(endTime)
        
        print "requests per seconds:\t" + str ( count / endTime)
        
        resultset = cursorb.fetchall()
        #print resultset
        #print len(resultset)
        print "\n\n"



    def testSynteticDataGet_filter_a_and_c(self):
        print "filter_a_c"
        dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
    
        cursorb = dbconn2.cursor()
        cursorb.execute("USE plistaContest")
        
        startTime = time.time()
        
        count = 300
        for n in xrange(count):
            filter_a_val = int( random.uniform(1,10) )
            filter_c_val = int( random.uniform(1,100) ) 
            cursorb.execute("""SELECT * FROM itemTableFull WHERE 
                            filter_a = :filter_a_val AND
                            filter_c = :filter_c_val
                            LIMIT 4""", 
                            dict(filter_a_val = filter_a_val,
                                 filter_c_val = filter_c_val))
            resultset = cursorb.fetchall()
        
        endTime = time.time() - startTime
        print "endTime: \t" + str(endTime)
        
        print "requests per seconds:\t" + str ( count / endTime)
        
        
        resultset = cursorb.fetchall()
        #print resultset
        #print len(resultset)
        print "\n\n"
    
    
    def testSynteticDataGet_filter_a_and_b(self):
        print "filter_a_b"
        dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
    
        cursorb = dbconn2.cursor()
        cursorb.execute("USE plistaContest")
        
        startTime = time.time()
        
        count = 300
        for n in xrange(count):
            filter_a_val = int( random.uniform(1,10) )
            filter_b_val = int( random.uniform(1,100) ) 
            cursorb.execute("""SELECT * FROM itemTableFull WHERE 
                            filter_a = :filter_a_val AND
                            filter_b = :filter_b_val
                            LIMIT 4""", 
                            dict(filter_a_val = filter_a_val,
                                 filter_b_val = filter_b_val))
            resultset = cursorb.fetchall()
        
        endTime = time.time() - startTime
        print "endTime: \t" + str(endTime)
        
        print "requests per seconds:\t" + str ( count / endTime)
        
        
        resultset = cursorb.fetchall()
        #print resultset
        #print len(resultset)
        print "\n\n"
    
    
    def testSynteticDataGet_filter_b_and_c(self):
        print "filter_b_c"
        dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
    
        cursorb = dbconn2.cursor()
        cursorb.execute("USE plistaContest")
        
        startTime = time.time()
        
        count = 300
        for n in xrange(count):
            filter_c_val = int( random.uniform(1,1000) )
            filter_b_val = int( random.uniform(1,100) ) 
            cursorb.execute("""SELECT * FROM itemTableFull WHERE 
                            filter_b = :filter_b_val AND
                            filter_c = :filter_c_val
                            LIMIT 4""", 
                            dict(filter_c_val = filter_c_val,
                                 filter_b_val = filter_b_val))
            resultset = cursorb.fetchall()
        
        endTime = time.time() - startTime
        print "endTime: \t" + str(endTime)
        
        print "requests per seconds:\t" + str ( count / endTime)
        
        
        resultset = cursorb.fetchall()
        #print resultset
        #print len(resultset)
        print "\n\n"
    
    
    def testSynteticDataGet_filter_b_and_a(self):
        print "filter_b_a ( reversed )"
        dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
    
        cursorb = dbconn2.cursor()
        cursorb.execute("USE plistaContest")
        
        startTime = time.time()
        
        count = 300
        for n in xrange(count):
            filter_a_val = int( random.uniform(1,10) )
            filter_b_val = int( random.uniform(1,100) ) 
            cursorb.execute("""SELECT * FROM itemTableFull WHERE 
                            filter_b = :filter_b_val AND
                            filter_a = :filter_a_val
                            LIMIT 4""", 
                            dict(filter_a_val = filter_a_val,
                                 filter_b_val = filter_b_val))
            resultset = cursorb.fetchall()
        
        endTime = time.time() - startTime
        print "endTime: \t" + str(endTime)
        
        print "requests per seconds:\t" + str ( count / endTime)
        
        resultset = cursorb.fetchall()
        #print resultset
        #print len(resultset)
        print "\n\n"
    
    
    def testSynteticDataGet_filter_c_and_a(self):
        print "filter_c_a (reversed )"
        dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
    
        cursorb = dbconn2.cursor()
        cursorb.execute("USE plistaContest")
        
        startTime = time.time()
        
        count = 300
        for n in xrange(count):
            filter_a_val = int( random.uniform(1,10) )
            filter_c_val = int( random.uniform(1,1000) ) 
            cursorb.execute("""SELECT * FROM itemTableFull WHERE 
                            filter_c = :filter_c_val AND
                            filter_a = :filter_a_val
                            LIMIT 4""", 
                            dict(filter_a_val = filter_a_val,
                                 filter_c_val = filter_c_val))
            resultset = cursorb.fetchall()
        
        endTime = time.time() - startTime
        print "endTime: \t" + str(endTime)
        
        print "requests per seconds:\t" + str ( count / endTime)
        
        
        resultset = cursorb.fetchall()
        #print resultset
        #print len(resultset)
        print "\n\n"
    
    
        
    def testSynteticDataGet_filter_a_and_b_and_c(self):
        print "filter_a_b_c"
        dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
    
        cursorb = dbconn2.cursor()
        cursorb.execute("USE plistaContest")
        
        startTime = time.time()
        
        count = 300
        for n in xrange(count):
            filter_a_val = int( random.uniform(1,10) )
            filter_b_val = int( random.uniform(1,100) ) 
            filter_c_val = int( random.uniform(1,1000) )
            cursorb.execute("""SELECT * FROM itemTableFull WHERE 
                            filter_a = :filter_a_val AND
                            filter_b = :filter_b_val AND
                            filter_c = :filter_c_val
                            LIMIT 4""", 
                            dict(filter_a_val = filter_a_val,
                                 filter_b_val = filter_b_val,
                                 filter_c_val = filter_c_val
                                 ))
            resultset = cursorb.fetchall()
        
        endTime = time.time() - startTime
        print "endTime: \t" + str(endTime)
        
        print "requests per seconds:\t" + str ( count / endTime)
        
        
        resultset = cursorb.fetchall()
        #print resultset
        #print len(resultset)
        print "\n\n"
        
        
    def testSynteticDataGet_filter_c_and_b_and_a(self):
        print "filter_c_b_a"
        dbconn2 = cql.connect(config_local.cassandra_host, config_local.cassandra_port )
    
        cursorb = dbconn2.cursor()
        cursorb.execute("USE plistaContest")
        
        startTime = time.time()
        
        count = 300
        for n in xrange(count):
            filter_a_val = int( random.uniform(1,10) )
            filter_b_val = int( random.uniform(1,100) ) 
            filter_c_val = int( random.uniform(1,1000) )
            cursorb.execute("""SELECT * FROM itemTableFull WHERE 
                            filter_c = :filter_a_val AND
                            filter_b = :filter_b_val AND
                            filter_a = :filter_c_val
                            LIMIT 4""", 
                            dict(filter_a_val = filter_a_val,
                                 filter_b_val = filter_b_val,
                                 filter_c_val = filter_c_val
                                 ))
            resultset = cursorb.fetchall()
        
        endTime = time.time() - startTime
        print "endTime: \t" + str(endTime)
        
        print "requests per seconds:\t" + str ( count / endTime)
        
        
        resultset = cursorb.fetchall()
        #print resultset
        #print len(resultset)
        print "\n\n"
    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    sData = SyntheticDataGetTest()
    #sData.warmUp()

    sData.testSynteticDataGet_filter_a()
    print "test"
    
    
#    try:
#        sData.testSynteticDataGet_filter_b()
#        sData.testSynteticDataGet_filter_c()
#    except:
#        print "a or b failed"
#    
#    try:
#        sData.testSynteticDataGet_filter_a_and_b()
#    except:
#        print "a and b failed"
#    
#    try:
#        sData.testSynteticDataGet_filter_a_and_c()
#    except:
#        print "a and c failed"
#    
#    try:
#        sData.testSynteticDataGet_filter_b_and_c()
#    except:
#        sData.testSynteticDataGet_filter_b_and_a()
#    
#    try:
#        sData.testSynteticDataGet_filter_c_and_a()
#    except:
#        print "c and a failed"
#    
#    try:
#        sData.testSynteticDataGet_filter_c_and_b()
#    except:
#        print "c and b failed"
#    
#    try:
#        sData.testSynteticDataGet_filter_a_and_b_and_c()
#    except: 
#        print "a and b and c failed"
#    
#    try:
#        sData.testSynteticDataGet_filter_c_and_b_and_a()
#    except:
#        print "c and b and a failed"
        
        
        
        