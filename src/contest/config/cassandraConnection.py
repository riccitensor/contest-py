
"""
just a single of a cassandra instance


@author: christian.winkelmann@plista.com
"""

import contest.packages.designPatterns.Singleton
import contest.config


class CassandraConnection(contest.packages.designPatterns.Singleton.Singleton3):
    def __init__(self):
        pass

    def __str__(self):
        return self.s



class RedisConnection(contest.packages.designPatterns.Singleton.Singleton_Redis):
	def __init__(self):
		pass


	def __str__(self):
		return self.s


