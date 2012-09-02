'''
Query Class to retrieve similarities to indexed items

'''

from packages.algorithm.gensimpy.Base import Base
from packages.algorithm.gensimpy.JSON_CONVERT import JSON_DATA_SIMILAR

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim.similarities.simserver import SessionServer
from gensim import utils



import sqlite3
import sqlitedict
import time

class Query( Base ):
    '''
    Query the similarities between at least two already indexed documents
    '''
    """ for asynchronous computation we need an adress we can push the results to """
    callback_adress = ""

    def __init__(self, training_id = '0', db_location = './linguisticModel/'):
        '''
        constructor
        '''
        
        self.training_id = training_id
        self.sqlserver = db_location + 'Training' + str(training_id)  + '.db'
        self.rootlocation = db_location
        
    """ def index(self, id):
        import logging
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
        
        from gensim import utils
        from gensim.similarities.simserver import SessionServer
        
        
        texts = ["Human machine interface for lab abc computer applications",
          "A survey of user opinion of computer system response time",
          "The EPS user interface management system",
          "System and human system engineering testing of EPS",
          "Relation of user perceived response time to error measurement",
           "The generation of random binary unordered trees",
          "The intersection graph of paths in trees",
          "Graph minors IV Widths of trees and well quasi ordering",
          "Graph minors A survey"]
        #corpus = [{'id': 'doc_%i' % num, 'tokens': utils.simple_preprocess(text)}
        #          for num, text in enumerate(texts)]
        corpus = [{'id': 'doc_%i' % num, 'tokens': utils.simple_preprocess(text)}
                  for num, text in enumerate(texts)]
        
        service2 = SessionServer(self.rootlocation) # create a local server
        service2.index(corpus) # index the same documents that we trained on...
        
        """
    def queryById(self, document_id, min_score=0.4, max_results=50 ):
        '''
        Query the gensim server for similar items
        @param document_id: the id of the document
        @param min_score: the minimum similarity score a document should hold
        @param max_results: maximum number of results  
        '''
        from gensim.similarities.simserver import SessionServer
        
        #service = SessionServer(self.rootlocation+'gensimTraining'+str(self.training_id), autosession=True) # create a local server
        import Pyro4
        service = Pyro4.Proxy(Pyro4.locateNS().lookup('gensim.testserver'))    
        
        result = service.find_similar(document_id, min_score, max_results) 
        
        converter = JSON_DATA_SIMILAR()
        result = converter.castNumpyFloats(result)
        
        return result


if __name__ == '__main__':
    q = Query(5)
    print q.queryById( 'doc1' ) 
    print '\n'
#    print q.queryById( 'doc2' ) 
#    print  '\n'
#    print q.queryById( 'doc3' ) 
#    print  '\n'
#    print q.queryById( 'doc4' ) 
#    print  '\n'
    
    
    
    
