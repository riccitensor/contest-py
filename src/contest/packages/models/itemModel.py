'''
Created on 16.12.2011
test implementation of an item model. It offers save and get methods
An item could be anything. An advertising campaign with banners, a theme, text, an url...

@author: christian.winkelmann@plista.com
'''
from contest.config import config_global
from contest.config import config_local
import cql
from cql.cassandra import Cassandra
from baseModel import baseModel


class itemModel(baseModel):
    
    mode_cassandra = True
    mode_riak = True
    
    """ the item itself in form of a dictionary """
    item = None
    updated_items = None # just a list which items have changed
    
    item_table_dict = {} # the item which should be in sync with the database unless it has changed
    item_table_dict_temp = {} # the temporay item which hasn't been saved yet
    
    item_id = None #int
     
    
    def __init__(self, item_id, mode = 'cassandra'):
        super(itemModel, self).__init__(mode)
#        self.dbconn = dbconn
#        self.cursor = self.dbconn.cursor()
        self.column_family = "itemTableFull"
        self.item_id = item_id
        
        try:
            # try to get the item from the database
            #self.item = self.get_item_id(item_id)
            self.conn.cursor.execute("USE " + config_global.cassandra_default_keyspace)
            #self.conn.cursor.execute( "SELECT * FROM " + self.column_family + ' USING CONSISTENCY ANY WHERE item_id = :item_id ', dict(item_id = item_id) )
            pass 
                       
        except cql.ProgrammingError as programmingError:
            print programmingError
            # it is ok if there is none, but we have to create it then
            """ @todo create item_attribute list """
            self.item_table_dict_temp = {}
            #print "no item here"
            
        #r = self.conn.cursor.fetchone()
        #d = self.conn.cursor.description
        #for i in xrange(len(r)):
        #    self.item_table_dict[ d[i][0] ] = r[i]
        
        #print "get Item Id:\t" +  str(self.item_table_dict)
    
        
    def set_attributes_by_dictionary(self, dict):
        """ this will be the shortcut for setting more attributes at once """
        self.item_table_dict_temp = dict    
        
    def set_item_id(self, item_id):
        pass
    
    def getAttributes(self):
        """ """
        return self.item_table_dict

    def query_by(self):
        """ Select items by """
        self.conn.cursor.execute( "SELECT * FROM " + self.column_family + ' USING CONSISTENCY ANY WHERE item_id = :item_id ', 
                                  dict(item_id = 1) )
        r = self.conn.cursor.fetchone()
        d = self.conn.cursor.description
        for i in xrange(len(r)):
            self.item_table_dict[ d[i][0] ] = r[i]
        
        print "get Item Id:\t" +  str(self.item_table_dict)

    def query_submitted_String(self, cql_query):
        
        self.conn.cursor.execute( "SELECT * FROM " + self.column_family + ' WHERE domain_id > 1 ')
        r = self.conn.cursor.fetchall()
        print len(r)


    def save(self):
        d = dict( column_family = self.column_family, item_id = self.item_id)
        
        self.item_table_dict = dict(self.item_table_dict.items() + self.item_table_dict_temp.items())

        insert_query = ""
         
        for key, value in self.item_table_dict_temp.items():
                insert_query += key + ","
                d[key] = value
        
        
        keys = self.item_table_dict_temp.keys()
        
        def my_function(x):
            r = x[0] + " = :" + x[0]
            return r
        
        #print ','.join( map( my_function, keys ) )
        insert_query = ','.join( map( my_function, self.item_table_dict_temp.items() ) )
        
        cql_query = "UPDATE :column_family USING CONSISTENCY ANY SET " + insert_query + " WHERE item_id = :item_id "
        
        self.conn.cursor.execute(cql_query, d )
    
    
    
    
    
if __name__ == '__main__':
    """ at first we are excluding all those dangerous statements since the server runs already """ 
     
    try:
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port ) 
        cursor = dbconn.cursor()
    
    except:
        print "not able to create a database connection"
    try:
        cursor.execute(" DROP KEYSPACE :keyspace ;", dict(keyspace=config_global.cassandra_default_keyspace))
        print "drop keyspace"
    except:
        print "not able to drop keyspace "+ config_global.cassandra_default_keyspace
    
    try:
        cursor.execute(" CREATE KEYSPACE :keyspace with strategy_class = 'SimpleStrategy' and strategy_options:replication_factor=1;", dict(keyspace=config_global.cassandra_default_keyspace))
        print "keyspace created: " + config_global.cassandra_default_keyspace
    except cql.ProgrammingError as programmingError:
        print programmingError
        print "keyspace creation is not possible"
     
    cursor.execute("USE " + config_global.cassandra_default_keyspace)
    
    #print itemModel.column_family
    
    try : 
        cursor.execute("DROP COLUMNFAMILY itemTableFull;")
        #cursor.execute("DROP COLUMNFAMILY " + itemModel.column_family + ";")
        
    except cql.ProgrammingError as programmingError:
       print programmingError
       print "itemTableFull not there, which is correct"
    " @todo this has to move into the migration "
    cursor.execute("CREATE COLUMNFAMILY itemTableFull ( item_id bigint PRIMARY KEY, full_text text, domainid bigint, friend_domain_id bigint ) WITH comment = 'item information' AND comparator = ascii AND default_validation = ascii;")
    #cursor.execute("CREATE COLUMNFAMILY " + itemModel.column_family + "( item_id varint PRIMARY KEY, full_text text ) WITH comment = 'item information'" )
    query = "CREATE INDEX on itemTableFull ( domainid );"
    cursor.execute(query)
    query = "CREATE INDEX on itemTableFull ( friend_domain_id );"
    cursor.execute(query)
    
    
    #cursor.execute("ALTER COLUMNFAMILY itemTableFull ALTER full_text TYPE text" )
    #cursor.execute("ALTER COLUMNFAMILY " + itemModel.column_family + " ALTER full_text TYPE text" )
    
    itemA = itemModel(125)
    #itemA.set_attributes_by_dictionary( {'keks' : 'keks1', 'bla' : 'bla1', 'humpi' : 'humpi1' } )
    #itemA.save()
    """
    cursor.execute( "SELECT * FROM " + itemA.column_family )
    r = cursor.fetchone()
    d = cursor.description

    #print d
    #print r
    
    
    itemB = itemModel(123, dbconn = dbconn)
    itemB.set_attributes_by_dictionary( {'pumpi' : 'pumpi1' } )
    itemB.save()
    
    cursor.execute( "SELECT * FROM " + itemB.column_family )
    r = cursor.fetchone()
    
    #print cursor.description
    #print r
    
    itemC = itemModel(123, dbconn = dbconn)
    #print itemC.getAttributes
    
    #print itemB
        
        #column_family = "item_table_full"
        
    """