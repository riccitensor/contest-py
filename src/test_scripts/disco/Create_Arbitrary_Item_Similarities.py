import json
from scipy.sparse.csr import csr_matrix
from scipy.sparse.lil import lil_matrix

__author__ = 'karisu'


from disco.job import Job
from disco.worker.classic.func import chain_reader


class Create_Arbitrary_Item_Similarities(Job):
    """ to compute the similarities the method resembles the Item cooccurrence computation

    """
    debug = False

    @staticmethod
    def map(line, params):
        """
        param: line: userid json of all items
        """
        from scipy.sparse.lil import lil_matrix
        # todo get the size of the matrix from a cache or somewhere else. The size is the maximum itemid

        v1 = lil_matrix((1, 5)) # create Row-based linked list sparse matrix

        # one line is userid itemid_1,itemid_2,...

        split = line.split()
        userid = split[0]
        itemids = split[1]
        itemid_list = itemids.split(',')

        # convert the input data to sparse matrix format
        for id in itemid_list:
            v1[0,int(id)] = 1



        # transpose the vector
        v1_transpose = v1.transpose()

        # compute the occurences for this user
        matrix_A = v1_transpose * v1


        yield userid, matrix_A #




    @staticmethod
    def reduce(iter, params):
        """
        item, matrix
        """
        from disco.util import kvgroup
        from scipy.sparse.csr import csr_matrix

        # todo load norms from redis
        import redis
        redis_con = redis.Redis('localhost')

        key_norms = 'create_norms_rated'
        #norms = redis_con.zrange(key, 0, -1, withscores=True)

        key_id_list = 'create_norms_idlist'
        id_list = redis_con.smembers(key_id_list)
        print "norms: {}".format(id_list)

        for i in id_list:
            print i


        cooccurence_matrix = csr_matrix((5, 5)) # create Row-based linked list sparse matrix

        #cooccurence_matrix[1,1] = 999

        for id, matrizes in kvgroup(sorted(iter)):
            # the id is an userid oder itemid
            id = int(id)
            norm_for_id = int( redis_con.zscore(key_norms, id) )

            # load the norms
            #norms = {1 : 2, 2 : 2, 3 : 1}

            for matrix in matrizes:
                #print matrix
                cooccurence_matrix = cooccurence_matrix + matrix

            print type(cooccurence_matrix)
            cooccurence_matrix = cooccurence_matrix.tolil()

            for norm_id in id_list:
                print "id: {}".format(id)
                norm_id = int(norm_id)
                #print "norm: {}".format(norm)
                #print "norm_id: {}".format(norms[id])
                norm_other_id = int( redis_con.zscore(key_norms, norm_id) )
                #print "cooccurence_matrix[id,norm_id]: {}".format(cooccurence_matrix[id,norm_id])

                cooccurence_matrix[id, norm_id] = cooccurence_matrix[id, norm_id] / (  norm_other_id +  norm_for_id - cooccurence_matrix[id, norm_id] )


        #yield 'cooc', cooccurence_matrix
        yield 'cooc', cooccurence_matrix




