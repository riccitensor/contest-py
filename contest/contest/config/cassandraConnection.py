
"""
just a single of a cassandra instance


@author: christian.winkelmann@plista.com
"""
from contest.packages.designPatterns import Singleton

import contest.packages.designPatterns.Singleton
import contest.config


class CassandraConnection(Singleton.Singleton3):
    def __init__(self):
        pass

    def __str__(self):
        return self.s



class RedisConnection(Singleton.Singleton_Redis):
	def __init__(self):
		pass


	def __str__(self):
		return self.s


