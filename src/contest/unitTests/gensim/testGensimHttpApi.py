'''
Created on 25.11.2011

This script is calling the Flask Server Gensim Rest Interface


@author: karisu
'''
import unittest
from contest.packages.controller.http_connector import http_connector
from contest.packages.algorithm.gensimpy.Training import Training
import json


class BaseOverRest(object):
    training_id = None
    
    def __init__(self, training_id = 5):
        """
        nothing to construct
        """
        self.training_id = training_id
        self.doc_id = 1
        self.baseurl = "localhost:5002"
        self.connection = http_connector( self.baseurl )
    

class TrainingOverRest( BaseOverRest ):
    
    def __init__(self, training_id = 5):

        super(TrainingOverRest, self).__init__( training_id )
        
#        self.training_id = training_id
#        self.doc_id = 1
#        self.baseurl = "localhost:5002"
#        self.connection = http_connector( self.baseurl )
#        
    
    
    def initTrainingSet(self):
        #from packages.algorithm.gensimpy.Training import Training 
    
        
        
        my_dict = { "training_id" : self.training_id }
        url_endpoint = "/unsupervised/clustering/gensim/initTrainingSet"
        print self.connection.fetch(my_dict, url_endpoint)
        pass
        
    def fillTrainingSet(self, text, document_id):
        url_endpoint = "/unsupervised/clustering/gensim/fillTrainingSet"
      
        my_dict = {"document_text" : text, "document_id" : document_id, "training_id" : self.training_id}
        return self.connection.fetch(my_dict, url_endpoint)

                
    def trainTrainingset(self):
        
        url_endpoint = "/unsupervised/clustering/gensim/trainTrainingSet"
        my_dict = { "training_id" : self.training_id }
        return self.connection.fetch(my_dict, url_endpoint)
        

class IndexingOverRest( BaseOverRest ):
    training_id = None
    
    def __init__(self, training_id = 5):
        super(IndexingOverRest, self).__init__( training_id )

    
    def fillIndexingSet(self, text, document_id):
        url_endpoint = "/unsupervised/clustering/gensim/fillIndexingSet"
      
        my_dict = {"document_text" : text, "document_id" : document_id, "training_id" : self.training_id}
        return self.connection.fetch(my_dict, url_endpoint)

    def indexIndexingSet(self):
        url_endpoint = "/unsupervised/clustering/gensim/indexSet"
        my_dict = { "training_id" : self.training_id }
        return self.connection.fetch(my_dict, url_endpoint)
    

class QueryingOverRest( BaseOverRest ):
    
    def __init__(self, training_id = 5):
        super(QueryingOverRest, self).__init__( training_id )


    def QueryById(self, document_id):
        """
        query an id and return ids of documents which match best
        """
        url_endpoint = "/unsupervised/clustering/gensim/queryById"
        my_dict = { "training_id" : self.training_id, "document_id" : document_id }
        return self.connection.fetch(my_dict, url_endpoint)
        
        
        
    def QueryByFullText(self, document_text):
        """
        query the full text and return ids of documents which match best
        """

class GensimRestApiTest(unittest.TestCase):

    training_id = None
    doc_id = None
    baseurl = None
    connection = None
    
    def setUp(self):
        self.baseurl = "localhost:5002"
        self.connection = http_connector( self.baseurl )

        self.texts = ["Human machine interface for lab abc computer applications",
                "A survey of user opinion of computer system response time",
                "The EPS user interface management system",
                "System and human system engineering testing of EPS",
                "Relation of user perceived response time to error measurement",
                "The generation of random binary unordered trees",
                "The intersection graph of paths in trees",
                "Graph minors IV Widths of trees and well quasi ordering",
                "Graph minors A survey",
                "Human machine interface for lab abc computer applications",
                "A survey of user opinion of computer system response time",
                "The EPS user interface management system",
                "System and human system engineering testing of EPS",
                "Relation of user perceived response time to error measurement",
                "The generation of random binary unordered trees",
                "The intersection graph of paths in trees",
                "Graph minors IV Widths of trees and well quasi ordering",
                "Graph minors A survey"]
        
        # texts = ["kuessen geht ueber studieren"] 

    def tearDown(self):
        pass


    def testhelloWorld(self):
        #({"type" : "POST" })
        url_endpoint = "/test/hello_world"
        # my_dict = { "training_id" : self.training_id }
        my_dict = {}
        print self.connection.fetch(my_dict, url_endpoint)
    
    def testTrainingProcess(self):
        # self.assertTrue ( self.initTrainingSet() == json.dumps( {"msg" : "ok"}), "initialising the training set failed" )
        tr = TrainingOverRest()
        print tr.initTrainingSet()
        
        num = 1
        for text in self.texts:
            num = num+1
            self.assertTrue( tr.fillTrainingSet(text, "doc"+str(num) ) == json.dumps( {"msg" : "fill_ok"}) )
    
        result = tr.trainTrainingset()
        self.assertTrue( result == json.dumps( {"msg" : "training_ok"}), "training failed: " + result)
    
    def _testIndexingProcess(self):
        ip = IndexingOverRest()
        
        num = 1
        for text in self.texts:
            num = num+1
            result = ip.fillIndexingSet( text, "doc"+str(num) )
            self.assertTrue( result == json.dumps( {"msg" : "fill_ok"}), "filling the index failed:" + result )
    
        result = ip.indexIndexingSet()
        self.assertTrue( result == json.dumps( {"msg" : "indexing_ok"}), "indexing failed: " + result)
        
    
    def _testQueryingProcess(self):
        qr = QueryingOverRest()
    
        document_id = "doc1"
        result = qr.QueryById( document_id )
        self.assertTrue(json.loads( result ) == {"doc1": 1.0, "doc14": 0.7482595443725586, "doc5": 0.7482595443725586}, "querying failed: " + result)
    



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
