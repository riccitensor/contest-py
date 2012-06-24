import json
from scipy.sparse.csr import csr_matrix
from scipy.sparse.lil import lil_matrix

__author__ = 'karisu'


from disco.job import Job
from disco.worker.classic.func import chain_reader


class Create_Norms(Job):
    """ we need the norms later

    """
    debug = False

    @staticmethod
    def map(line, params):
        """
        param: line: userid json of all items
        """

        import redis
        redis_con = redis.Redis('localhost')

        mytuple = line.split()
        id_list = mytuple[1].split(',')
        id_primary = int( mytuple[0] )

        print id_list
        num_ids = len(id_list)
        key_rated = 'create_norms_rated'
        redis_con.zadd(key_rated, id_primary, num_ids)
        key_id_list = 'create_norms_idlist'
        redis_con.sadd(key_id_list, id_primary)


        print redis_con.smembers(key_id_list)

        yield 1,1





