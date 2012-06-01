'''
Created on 27.01.2012

Instead of mocking the database beforehand testing the models we are going to test 
the database 


@author: christian.winkelmann@plista.com
'''

import unittest
from config import config_local
from config import config_global
import cql


class itemTableFullTest(unittest.TestCase): 

    def setUp(self):
        self.dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port ) 
        self.cursor = self.dbconn.cursor()


    def tearDown(self):
        pass


    

    
    def testSelect(self):
        
        try:
            self.cursor.execute("USE " + config_global.cassandra_default_keyspace)
        except:
            print "error at using to keyspace"
        
        try:
            self.cursor.execute(""" INSERT INTO :columnfamily (item_id, full_text, domain_id) 
                VALUES (1, 'blakeks', 2) USING TTL 20
            """, dict(columnfamily = config_global.dbname_itemModel))
        
            self.cursor.execute(""" INSERT INTO :columnfamily (item_id, full_text, domain_id) 
                VALUES (2, 'hawaii!', 3) USING TTL 20
                """, dict(columnfamily = config_global.dbname_itemModel))
        
            print " inserted into ItemTableFull "
        except cql.ProgrammingError as programmingError:
            print programmingError
    
        
        try:
            self.cursor.execute(""" SELECT * FROM :columnfamily """, 
           
                           dict(columnfamily = config_global.dbname_itemModel))
            
            
            print " queried from ItemTableFull "
            print self.cursor.fetchall()
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        try:
            self.cursor.execute(""" SELECT * FROM :columnfamily WHERE domain_id = 2 """, 
           
                           dict(columnfamily = config_global.dbname_itemModel))
            
            
            print " queried from ItemTableFull "
            print self.cursor.fetchall()
        except cql.ProgrammingError as programmingError:
            print programmingError
            
    
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()