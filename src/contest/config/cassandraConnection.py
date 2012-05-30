
"""
just a single of a cassandra instance


@author: christian.winkelmann@plista.com
"""

import contest.packages.designPatterns.Singleton
import contest.config
import cql

class CassandraConnection(contest.packages.designPatterns.Singleton.Singleton3):
        def __init__(self):
            pass
            #print "Instance initialization in derived."
            #self.s = s
            
            
        def __str__(self):
            return self.s
        
        def aStupidMethod(self):
            print "a stupid method"
            
            