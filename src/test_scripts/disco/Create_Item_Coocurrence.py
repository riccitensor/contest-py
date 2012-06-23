import json
from scipy.sparse.lil import lil_matrix

__author__ = 'karisu'


from disco.job import Job
from disco.worker.classic.func import chain_reader


class Create_Item_Coocurrence(Job):
    """ from all the single ratings we are making a USER x ITEM Matrix

    """
    debug = False

    @staticmethod
    def map(line, params):
        """
        line: userid json of all items
        """
        from scipy.sparse.lil import lil_matrix
        # todo get the size of the matrix from a cache or somewhere else

        v1 = lil_matrix((1, 1000)) # create Row-based linked list sparse matrix

        # one line is userid itemid_1,itemid_2,...

        split = line.split()
        userid = split[0]
        itemids = split[1]
        itemid_list = itemids.split(',')

        for id in itemid_list:
            v1[0,int(id)] = 1

        v1_transpose = v1.transpose()
        matrix_A = v1_transpose * v1

        yield userid, matrix_A


    @staticmethod
    def reduce(iter, params):
        """
        item, matrix
        """
        from disco.util import kvgroup
        from scipy.sparse.lil import lil_matrix

        debug = False

        cooccurence_matrix = lil_matrix((1000, 1000)) # create Row-based linked list sparse matrix

        for userid, matrizes in kvgroup(sorted(iter)):

            for matrix in matrizes:
                #print matrix
                cooccurence_matrix = cooccurence_matrix + matrix

        yield 'cooc', cooccurence_matrix





