'''
Created on 08.09.2011

@author: karisu

After Training a Model you need to index documents you actually want to query later. 


'''

from packages.algorithm.gensimpy.Base import Base

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.similarities.simserver import SessionServer
from gensim import utils

import Pyro4
import sqlite3
import sqlitedict
import time


class Indexing( Base ):
    '''
    This class is to train our gensim package
    '''
    training_id = 5

    def __init__(self, training_id = '0', db_location = './linguisticModel/'):
    #def __init__(self, training_id = '0', db_location = '/tmp/ramdisk/linguisticModel/'):
        '''
        constructor
        '''
        super(Indexing, self).__init__(training_id, db_location, local_execution = True)
       

    def test_index(self):
            
            # a stupid first training set               
            texts = ["Human machine interface for lab abc computer applications",
            "A survey of user opinion of computer system response time",
            "The EPS user interface management system",
            "System and human system engineering testing of EPS",
            "Relation of user perceived response time to error measurement",
            "The generation of random binary unordered trees",
            "The intersection graph of paths in trees",
            "Graph minors IV Widths of trees and well quasi ordering",
            "Graph minors A survey"]
            corpus = [{'id': 'doc_%i' % num, 'tokens': utils.simple_preprocess(text)}
                       for num, text in enumerate(texts)]
            
            service_id = '1234'
            #from gensim.similarities.simserver import SessionServer
            # service = similarities.SessionServer('bla') # create a local server
            # service = SessionServer(self.rootlocation, autosession=True)
            import Pyro4
            service = Pyro4.Proxy(Pyro4.locateNS().lookup('gensim.testserver'))
            
            
            service.train(corpus, method='lsi') ## TODO we don't have a corpus yet, but we definatly need one big
            
            ''' texts = ["Human machine interface for lab abc computer applications",
            "A survey of user opinion of computer system response time",
            "The EPS user interface management system",
            "System and human system engineering testing of EPS",
            "Relation of user perceived response time to error measurement",
            "The generation of random binary unordered trees",
            "The intersection graph of paths in trees",
            "Graph minors IV Widths of trees and well quasi ordering",
            "Graph minors A survey"]
            corpus = [{'id': 'doc_%i' % num, 'text': text} for num, text in enumerate(texts)]
            '''
                       
    def init_indexing_set(self):
            ''' if it does not exist then create one 
 
            '''
            self.delete_set()
        
            import sqlite3
            training_id = str(self.training_id)
            conn = sqlite3.connect(self.sqlserver)
            
            c = conn.cursor()

            # Create table
            try:
                sql = '''CREATE TABLE gensimIndexingSet'''+str(training_id)+''' ( text TEXT, id TEXT ) '''  
                c.execute( sql )
            
            except sqlite3.OperationalError:
                print "database already exists, but that not that bad"

            
            # Save (commit) the changes
            conn.commit()
            
            # We can also close the cursor if we are done with it
            c.close()

    def fill_indexing_set(self, document_string='123', document_id='23'):
        ''' fill a training set as you wish
        '''
        #import redis
        #redis_con = re
        
        
        #redis_new_item_list = "new_semantic_items" 
        #redis_itemid_document_text = "redis_itemid_document_text"
        
        #self.redis_con.rpush(self.l_redis_new_item_list, document_id)
        self.redis_con.sadd(self.s_redis_new_item_list, document_id)
        self.redis_con.hset(self.h_redis_itemid_document_text, document_id, document_string )
        

        
        
    def fill_indexing_set_old(self, document_string='123', document_id='23'):
            ''' fill a training set as you wish
            '''
            import sqlite3
            training_id = str(self.training_id)
            conn = sqlite3.connect(self.sqlserver)
            
            c = conn.cursor()
            
            #sql_query = "INSERT INTO gensimIndexingSet"+training_id +" VALUES (\""+document_string+"\", \"" + str(document_id) + "\")"                                                                             
            sql_query = "INSERT INTO gensimIndexingSet"+training_id +" ( id, text ) VALUES (?, ?)"
            #print sql_query
            c.execute( sql_query, ( str( document_id ), document_string ) )
            # Save (commit) the changes
            conn.commit()
            
            
            # We can also close the cursor if we are done with it
            c.close()

            
    
    def get_indexing_set(self):
        result = self.redis_con.hgetall(self.h_redis_itemid_document_text)
        return result
                
    
    def commit_indexing_set_old(self):
        ''' after filling an indexing set the actual indexing needs to be done
        '''         
        import sqlite3
        training_id = str(self.training_id)
        conn = sqlite3.connect(self.sqlserver)
        
        c = conn.cursor()

        # fetch the content 
        sql = "SELECT * FROM gensimIndexingSet"+str(training_id)
        print ( sql )
        c.execute( sql )
        
        # just fetch all items
        
        indexing_data = c.fetchmany(500);
        
        #service = similarities.SessionServer(self.rootlocation, autosession=True)
        service = SessionServer(self.rootlocation + 'gensimTraining'+str(self.training_id), autosession=True) # create a local server
        import Pyro4
        service = Pyro4.Proxy(Pyro4.locateNS().lookup('gensim.testserver'))
        print self.rootlocation + 'gensimTraining'+str(self.training_id)
        
        while len(indexing_data) > 0 :       
            corpus = [{'id': str(id), 'tokens': utils.simple_preprocess(text)}
                for (text, id) in indexing_data]
            
            service.index(corpus) ## TODO we don't have a corpus yet, but we definatly need one big      
            indexing_data = c.fetchmany(500)
            service.autosession = True
            time.sleep(0.5)          
        
        # sql = "DROP TABLE IF EXISTS gensimIndexingSet"+str(training_id)
        # c.execute( sql )
        
        self.delete_set()
        self.init_indexing_set()
        
        return 'indexing done'
    
    
    def commit_indexing_set(self):
        ''' after filling an indexing set the actual indexing needs to be done
        '''         
        #indexing_data = c.fetchmany(500);
        
        #service = similarities.SessionServer(self.rootlocation, autosession=True)
        #service = SessionServer(self.rootlocation + 'gensimTraining'+str(self.training_id), autosession=True) # create a local server
        
        service = Pyro4.Proxy(Pyro4.locateNS().lookup('gensim.testserver'))
        indexing_data = self.get_indexing_set()
        
        keys = self.redis_con.smembers(self.s_redis_new_item_list)
        self.redis_con.srem(self.s_redis_new_item_list, keys)
        indexing_data = self.redis_con.hmget(self.h_redis_itemid_document_text, keys)
                       
        corpus = []
        #for (id, text) in indexing_data.iteritems():
        #    corpus.append({ 'id' : str(id), "tokens" : utils.simple_preprocess(text) })
        for id in keys:
            corpus.append({ "id" : id, "tokens" : utils.simple_preprocess( self.redis_con.hget(self.h_redis_itemid_document_text, id) ) } )    
        
        # print corpus
        service.index(corpus) ## TODO we don't have a corpus yet, but we definatly need one big
                
        return 'indexing done'
        
        
    def delete_set(self):
            #import sqlite3
            training_id = str(self.training_id)
            conn = sqlite3.connect(self.sqlserver)
            
            
            c = conn.cursor()
            
            sql = "DROP TABLE IF EXISTS gensimIndexingSet"+str(training_id)
            c.execute( sql )
        
            
        
            conn.commit()
            
            # We can also close the cursor if we are done with it
            c.close()

if __name__ == '__main__':
    t = Indexing(5)
    t.init_indexing_set()
   
    
    texts = ["Human machine interface for lab abc computer applications",
                "A survey of user opinion of computer system response time",
                "The EPS user interface management system",
                "System and human system engineering testing of EPS",
                "Relation of user perceived response time to error measurement",
                "The generation of random binary unordered trees",
                "The intersection graph of paths in trees",
                "Graph minors IV Widths of trees and well quasi ordering",
                "Graph minors A survey"]
        
    num = 1
    for text in texts:
        t.fill_indexing_set(text, "doc"+str(num))
        num = num+1
    
    print t.get_indexing_set()
    print t.commit_indexing_set()
    #t.delete_set()
