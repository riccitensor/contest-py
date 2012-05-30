# -*- coding: utf-8 -*-
'''
Created on 08.09.2011

@author: karisu

In the Training a model is generated from documents in order to get a "feeling" about the language

'''
#from gensim import similarities   

        

from packages.algorithm.gensimpy.Base import Base
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.similarities.simserver import SessionServer
from gensim import utils

import sqlite3
import sqlitedict
import time

class Training( Base ):
    '''
    This class is to train our gensim package
    '''
    
    # training_id = ''

    def __init__(self, training_id = '0', db_location = './linguisticModel/', local_execution = False):
    #def __init__(self, training_id = '0', db_location = '/tmp/ramdisk/linguisticModel/'):
        '''
        constructor
        '''
        super(Training, self).__init__(training_id, db_location, local_execution)
        
        
        
        

    def test_train(self):
            
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
            # service = similarities.SessionServer('bla') # create a local server
            #service = SessionServer(self.rootlocation, autosession=True)
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
 
            
    def init_training_set(self):
            ''' if a training set does not exist then create one
 
            '''
            import sqlite3
            training_id = str(self.training_id)
            import os
            
            self.delete_set()


            conn = sqlite3.connect(self.sqlserver)
            c = conn.cursor()

            # Create table
            try:
                sql = '''CREATE TABLE gensimTrainingSet'''+str(training_id)+''' ( text TEXT, id TEXT ) '''  
                c.execute( sql )
                
            
            except sqlite3.OperationalError:
                print "Training database already exists."
                return -1
                
            try: 
                sql = '''CREATE TABLE gensimIndexSet'''+str(training_id)+''' ( text TEXT, id TEXT ) '''  
                c.execute( sql )
                
            except sqlite3.OperationalError:
                print "Indexing database already exists."    
                return -1
            
            
            # Save (commit) the changes
            conn.commit()
            
            # We can also close the cursor if we are done with it
            c.close()

            return 1
        
     
    def delete_set(self):
        """ delete the Training set
        @todo refactor into a base class because Indexing, Training is the same in this kind
        """
        training_id = str(self.training_id)
        conn = sqlite3.connect(self.sqlserver)
            
        c = conn.cursor()
            
        sql = "DROP TABLE IF EXISTS gensimTrainingSet"+str(training_id)
        c.execute( sql )
        
        conn.commit()
            
        # We can also close the cursor if we are done with it
        c.close()

        
    def fill_training_set(self, document_string, document_id, training_id='0'):
            ''' fill a training set as you wish
            '''
            import sqlite3
            #training_id = str(self.training_id)
            conn = sqlite3.connect(self.sqlserver)
            
            c = conn.cursor()

            #sql_query = "INSERT INTO gensimTrainingSet"+str(self.training_id)+" VALUES (\""+document_string+"\", " + document_id + ")"
            sql_query = "INSERT INTO gensimTrainingSet"+str(self.training_id)+" ( id, text ) VALUES(?, ?)"
                                                                             
            #execute sql_query
            c.execute( sql_query, ( document_id, document_string ) )

            
            # Save (commit) the changes
            conn.commit()
            
            # We can also close the cursor if we are done with it
            c.close()
    
    
    def show_training_set(self):
            ''' show the content of the training set
            '''
            import sqlite3
            training_id = str(self.training_id)
            conn = sqlite3.connect(self.sqlserver)
            
            c = conn.cursor()

            # fetch the content 
            sql = "SELECT * FROM gensimTrainingSet"+str(training_id)
            print ( sql )
            c.execute( sql )
            
            # just fetch all items
            print c.fetchall();
          
            
            # We can also close the cursor if we are done with it
            c.close()    
                
    
    def commit_training_set(self):
            ''' after filling a training set the actual training needs to be done
            '''         
            import sqlite3
            training_id = str(self.training_id)
            conn = sqlite3.connect(self.sqlserver)
            
            c = conn.cursor()

            # fetch the content 
            sql = "SELECT * FROM gensimTrainingSet"+str(training_id)
            print ( sql )
            c.execute( sql )
            
            # just fetch all items
            
            training_data = c.fetchmany(30000);
            #print training_data
            #service = similarities.SessionServer(self.rootlocation, autosession=True)
            #service = SessionServer(self.rootlocation + 'gensimTraining'+str(self.training_id), autosession=True) # create a local server
            import Pyro4
            service = Pyro4.Proxy(Pyro4.locateNS().lookup('gensim.testserver'))
            
            while len(training_data) > 0 :
                    #for (text,id) in training_data:
                        
                    corpus = [{'id': id, 'tokens': utils.simple_preprocess(text)}
                        for (text, id) in training_data]
                
                    service.train(corpus, method='lsi') ## TODO we don't have a corpus yet, but we definatly need one big      
                    time.sleep(0.1)
                    training_data = c.fetchmany(30000);
                    
                    
            self.init_training_set()    
            return 'training done'
        
        
        
    def commit_WIKIPEDIA_training_set(self, ):
            ''' after filling a training set the actual training needs to be done
            '''         
            from packages.controller.gensim_sim import gensim_sim
            w = gensim_sim()

            service = SessionServer(self.rootlocation + 'gensimTraining'+str(self.training_id), autosession=True) # create a local server
            
            factor=20000
            for d in range (0, 100):
                
                print "currently working on text row " + str( d*factor ) + "up to" + str( (d+1)*factor )
                
                training_data = w.init_sql_connection(d*factor, factor )
                corpus = [{'id': id, 'tokens': utils.simple_preprocess(text)}
                    for (id, text) in training_data]
            
                 
                service.train(corpus, method='lsi') ## TODO we don't have a corpus yet, but we definatly need one big      
                
                        
                    
            #self.init_training_set()    
            return 'training done'
        
        



if __name__ == '__main__':
    """
    """
    
                    