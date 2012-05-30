'''
Created on 25.12.2011

@author: christian.winkelmann@plista.com
'''
from contest.config import config_local
from contest.config import config_global
import cql
    

class itemTableFull_Class(object):
    
    
    def __init__(self, *args, **kwargs):
        object.__init__(self, *args, **kwargs)
        
        dbconn = cql.connect(config_local.cassandra_host, config_local.cassandra_port ) 
        cursor = dbconn.cursor()
        print "migrating of itemTableFull"
        
        try:
            cursor.execute("USE " + config_global.cassandra_default_keyspace)
            cursor.execute(""" DROP COLUMNFAMILY :columnfamily """, 
                           dict(columnfamily = config_global.dbname_itemModel))
        except:
            print "error at dropping itemTableFull, which might be fine"
        
        try:
            cursor.execute(""" CREATE COLUMNFAMILY :columnfamily
            ( 
            item_id bigint PRIMARY KEY,
            item_id_sec bigint,  
            full_text text,
            domain_id bigint,
            filter_a int,
            filter_b int, 
            filter_c int, 
            filter_d int,
            filter_e int,
            filter_f int,
            filter_g int,
            filter_h int,
            filter_i int,
            filter_j int,
            filter_k int,
            filter_l int,
            item_format varchar,
            created varchar,
            email varchar,
            birth_day int,
            birth_month int,
            birth_year int,
            domain_filter_json text,
            plz_filter varchar,
            friend_domain_id int,
            status int,
            img_url text
            ) 
            WITH comment = 'item information' AND
            default_validation = int""", 
                           dict(columnfamily = config_global.dbname_itemModel))
            
            print " created ItemTableFull "
        except cql.ProgrammingError as programmingError:
            print programmingError
            
            
        # set up the indizes
        try:
            cursor.execute("CREATE INDEX ON :columnfamily (domain_id)", 
                           dict(columnfamily = config_global.dbname_itemModel) )
    
            
            cursor.execute("""CREATE INDEX ON :columnfamily ( filter_a )""", dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("""CREATE INDEX ON :columnfamily ( filter_b )""", dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("""CREATE INDEX ON :columnfamily ( filter_c )""", dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("""CREATE INDEX ON :columnfamily ( filter_d )""", dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("""CREATE INDEX ON :columnfamily ( filter_e )""", dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("""CREATE INDEX ON :columnfamily ( filter_f )""", dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("""CREATE INDEX ON :columnfamily ( filter_g )""", dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("""CREATE INDEX ON :columnfamily ( filter_h )""", dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("""CREATE INDEX ON :columnfamily ( filter_i )""", dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("""CREATE INDEX ON :columnfamily ( filter_j )""", dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("""CREATE INDEX ON :columnfamily ( filter_k )""", dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("""CREATE INDEX ON :columnfamily ( filter_l )""", dict(columnfamily = config_global.dbname_itemModel) )
            
            cursor.execute("CREATE INDEX ON :columnfamily (email)", dict(columnfamily = config_global.dbname_itemModel) )
            
            cursor.execute("CREATE INDEX ON :columnfamily (status)", dict(columnfamily = config_global.dbname_itemModel) )
            
            cursor.execute("CREATE INDEX ON :columnfamily (item_id_sec)", dict(columnfamily = config_global.dbname_itemModel) )
            
            
            """
            cursor.execute("CREATE INDEX ON :columnfamily (birth_year, birth_month, birth_day)", 
                           dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("CREATE INDEX ON :columnfamily (domain_id)", 
                           dict(columnfamily = config_global.dbname_itemModel) )
            cursor.execute("CREATE INDEX ON :columnfamily (domain_id)", 
                           dict(columnfamily = config_global.dbname_itemModel) )
            """
            print "done with the indizes"
            
        except cql.ProgrammingError as programmingError:
            print "problem at creating indizes"
            print programmingError
            
        try:
            cursor.execute(""" INSERT INTO :columnfamily (item_id, full_text, domain_id) 
            VALUES (1, 'keks', 2) USING TTL 20
            """, dict(columnfamily = config_global.dbname_itemModel))
            
            cursor.execute(""" INSERT INTO :columnfamily (item_id, full_text, domain_id) 
            VALUES (2, 'hawaii!', 3) USING TTL 20
            """, dict(columnfamily = config_global.dbname_itemModel))
            
            print " inserted into ItemTableFull "
        except cql.ProgrammingError as programmingError:
            print programmingError
        
            
        try:
            cursor.execute(""" SELECT * FROM :columnfamily """, 
           
                           dict(columnfamily = config_global.dbname_itemModel))
            
            
            print " queried from ItemTableFull "
            print cursor.fetchall()
        except cql.ProgrammingError as programmingError:
            print programmingError
        
        try:
            cursor.execute(""" SELECT * FROM :columnfamily WHERE domain_id = 2 """, 
           
                           dict(columnfamily = config_global.dbname_itemModel))
            
            
            print " queried from ItemTableFull "
            print cursor.fetchall()
        except cql.ProgrammingError as programmingError:
            print programmingError
            
    
            
        


if __name__ == '__main__':
    
    itemTableFullC = itemTableFull_Class()