import json

from scipy.sparse.csr import csr_matrix
from scipy.sparse.lil import lil_matrix

__author__ = 'karisu'


from disco.job import Job
from disco.worker.classic.func import chain_reader


class Create_Group_By_id(Job):
    """ we need the norms later

    """
    debug = False

    @staticmethod
    def map(line, params):
        mytuple = line.split()
        userid = mytuple[0]
        itemid = mytuple[1]
        timestamp = mytuple[2]

        yield "itemid:{}".format(itemid), timestamp


    @staticmethod
    def combiner(key, value, buffer, done, params):
        if not done:

            # Ensure variable is defined
            try:
                buffer[key]
            except KeyError:
                buffer[key] = {}

            try:
                buffer[key][value]
            except KeyError:
                buffer[key][value] = 0

            # Test whether variable is defined to be None
            buffer[key][value] += 1
            print "combiner not done: {}".format(key)

        else :
            print buffer
            for i,k in buffer.items():
                print "combiner done: {} and k: {}".format(i, k)
                yield i, k


            buffer.clear()


    @staticmethod
    def reduce(iter, params):
        from disco.util import kvgroup
        debug = False

        for id, timestamp_list in kvgroup(sorted(iter)):
            local_list = []
            for timestamp in timestamp_list:
                local_list.append(timestamp)

            #print type(local_list)
            print "id:{}".format(id)
            yield id, local_list








