'''
Created on 09.12.2011

@author: christian.winkelmann@plista.com

this is just a testscript which writes custom GENERATED items as fast as possible into cassandra
uses the itemmodel


the 1. test scenario states:
writing 100.000.000 items which 20 properties each and non sparse

2. test scenario. randomly picking one item at a time and read it

3. filtering and sorting items like for geo targeting or day budget

'''

print "bla"
import sys
# print sys.path
# sys.path.append("/home/karisu/python_env/lib/python2.7/site-packages/contest/Transport/contest")
# sys.path.append("/home/karisu/python_env/")
#sys.path.append("/home/karisu/workspace/plistaContest/src/")
sys.path.append("/home/karisu/workspace/plistaContest/src/contest/") 
print sys.path

from contest.config import config_global, config_local
from contest.packages.models.itemModel import itemModel
import cql
import random
import time


if __name__ == '__main__':
    '''start the server on command line
    $ sudo bin/cassandra -f '''
    ''' connect to the server '''
    
        
    n = 0
    n2 = 10000

    cycles = 1
    end_time = 0
    start_time = 0
    
    # dbconn = cql.connect(config.cassandra_host, config.cassandra_port )
    
    email_adress = ["a@plista.com", "b@plista.com", "c@plista.com", "d@plista.com","e@plista.com", "f@plista.com", "g@plista.com", "h@plista.com","i@plista.com", "j@plista.com", "k@plista.com", "l@plista.com"]
    email_adress_len = len(email_adress)
    
    for k in xrange( n, n2 ):
        #time.sleep(0)
        start_time = time.time()
        for i in xrange(cycles): ## this seem very useless
            
            item_id = int(k)
            print "item_id:" + str(item_id)
            
            created = random.uniform( 0, 10000 )
            email = email_adress[ int(random.uniform(0,email_adress_len))]
            birth_year = int( random.uniform( 1970, 2032) )
            birth_month = int( random.uniform( 1, 12) )
            birth_day = int( random.uniform( 1, 31) )
            fulltext = "Gillingham Football Club is an English professional football club based in the town of Gillingham, Kent "
            domain_filter_json = "de,en,at,ch,us"
            domain_id = int( random.uniform(1, 3500) ) 
            plz_filter = random.uniform(0,100000)
            img_url = "http://en.wikipedia.org/wiki/File:Gillingham.png"
            friend_domain_id = int( random.uniform(0,2000) )
            categoryids = "1,2,3,4,5"
            updated_at = int(random.uniform(10000000, 40000000))
            filter_a = int(random.uniform(1, 10))
            filter_b = int(random.uniform(1, 100))
            filter_c = int(random.uniform(1, 1000))
            filter_d = int(random.uniform(1, 2000))
            filter_e = int(random.uniform(1, 3000))
            filter_f = int(random.uniform(1, 4000))
            filter_g = int(random.uniform(1, 5000))
            filter_h = int(random.uniform(1, 10000))
            filter_i = int(random.uniform(1, 20000))
            filter_j = int(random.uniform(1, 40000))
            filter_k = int(random.uniform(1, 80000))
            filter_l = int(random.uniform(1, 160000))
            
                       
            
            itemA = itemModel( int(item_id) )
            
            itemA.set_attributes_by_dictionary({ 
                                            'created' : created, 
                                            'email' : str( email ), 
                                           'birth_day' : birth_day,
                                           'birth_year' : birth_year ,
                                           'birth_month' : birth_month ,   
                                           'full_text' : fulltext,
                                           'domain_filter_json' : domain_filter_json, 
                                           'plz_filter' : str(plz_filter),
                                           'img_url' : img_url, 
                                           'friend_domain_id' :  friend_domain_id , 
                                           'updated_at' : str(updated_at),
                                           'status' : int(round(random.uniform(0,1))),
                                           'filter_a' : filter_a,
                                           'filter_b' : filter_b,
                                           'filter_c' : filter_c,
                                           'filter_d' : filter_d,
                                           'filter_e' : filter_e,
                                           'filter_f' : filter_f,
                                           'filter_g' : filter_g,
                                           'filter_h' : filter_h,
                                           'filter_i' : filter_i,
                                           'filter_j' : filter_j,
                                           'filter_k' : filter_k,
                                           'filter_l' : filter_l
              
                                           })
            """itemA.set_attributes_by_dictionary({  
                                                'full_text' : str( fulltext ), 
                                                'domainid' : domain_id,
                                                'friend_domain_id' : friend_domain_id
              
                                           })
            """
            itemA.save()
            
        end_time = time.time()
        
        #print str( round ( (1 / ( end_time - start_time)) * cycles ) ) + "\titems per second "
        #print str(k*i+cycles) + "\titems written"
            