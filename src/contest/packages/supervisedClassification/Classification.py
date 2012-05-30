'''
all supervised classification have to inherit from this class


Created on 21.10.2011

@author: karisu
'''


class SupervisedClassification(object):
    """Base class for a supervised classifications for either vector or text/string based
    @todo merge because a 1 dimensional vector containing text is just a text and two dimensional vector could hold one float and one string"""
    
    training_id = '0'
    type = 'default'
    
    def __init__(self, type, training_id):
        """ @param type use this for defining the type i.e. string
        """
        import sqlite3
        self.training_id = str( training_id )
        self.type = type
        #import os
        
        
        dbname = self.type + "_" + self.training_id
        print self.sqlserver
       
        #print os.getcwd()

        conn = sqlite3.connect(self.sqlserver)
        c = conn.cursor()


        """ @todo use pytables hdf format instead """  
        try:
        # Create table
            if type == 'stext':
                """ supervised text """
                sql = '''CREATE TABLE '''+ dbname +''' ( text TEXT, label TEXT, id TEXT ) '''  
                c.execute( sql )
                
            if type == 'uvector':
                """ supervised 3 dim vector """
                sql = '''CREATE TABLE '''+ dbname +''' ( dim1 REAL, dim2 REAL, dim3 REAL, label TEXT, id TEXT ) '''  
                c.execute( sql )
            
            
        except sqlite3.OperationalError:
            print type + str(training_id) +" database already exists."
            
        # Save (commit) the changes
        conn.commit()
        
        # We can also close the cursor if we are done with it
        c.close()
    

    def database_connection(self, storage='sqlite'):
        """
            pseudo abstraction for database access
        """     
        
        
        