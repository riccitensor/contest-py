
from disco.job import Job

from disco.worker.classic.func import chain_reader


class Create_discretize(Job):
    """ from all the single ratings we are making a USER x ITEM Matrix

    """
    debug = False

    @staticmethod
    def map(line, params):

        def to_hour(microsec):
            return int(microsec) / ( 1000 * 60 )

        print "==== discrete ===="
        print line

        itemid = line[0]
        counts = line[1]
        print "======== counts: {}".format(counts[0])
        ratings = counts[0]
        ratings_new = {}
        for i, k in ratings.items():
            print "iterate: {}".format(i)
            try:
                ratings_new[to_hour(i)]
            except KeyError:
                ratings_new[to_hour(i)] = 0

            # Test whether variable is defined to be None
            ratings_new[to_hour(i)] += k

        print "============= itemid: {} \tratings_new: {} =============0".format(itemid, ratings_new)
        yield 1, 1




    @staticmethod
    def reduce(iter, params):
        from disco.util import kvgroup


        for hitcount, id_list in kvgroup(sorted(iter)):
            local_list = []
            for id in id_list:

                local_list.append(id)

            #print type(local_list)


            print local_list
            print hitcount
            yield hitcount, local_list





