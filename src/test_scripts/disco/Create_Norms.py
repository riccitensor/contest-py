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
        norm_prefix = 'norm_prefix:'
        import redis
        redis_con = redis.Redis('localhost')

        mytuple = line.split()
        id_list = mytuple[1].split(',')
        id_primary = int( mytuple[0] )
        print "id_primary: {}".format(id_primary)

        print id_list
        for i in id_list:
            redis_con.incr(norm_prefix + str(i), 1)

        #num_ids = len(id_list)
        #num_ids_nonZero = 0
        #num_ids_nonZero = id_list.count('1') # there only two possible values in the list: 0 or 1
        key_rated = 'create_norms_rated'
        #redis_con.zadd(key_rated, id_primary, num_ids_nonZero)
        #key_id_list = 'create_norms_idlist'
        #redis_con.sadd(key_id_list, id_primary)


        #print redis_con.smembers(key_id_list)

        yield id_primary,1





