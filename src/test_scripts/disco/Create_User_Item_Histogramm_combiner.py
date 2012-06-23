import json

__author__ = 'karisu'


from disco.job import Job
from disco.worker.classic.func import chain_reader


class Create_User_Item_Histogramm_combiner(Job):
    """ from all the single ratings we are making a USER x ITEM Matrix

    """
    debug = False

    @staticmethod
    def map(line, params):
        #print "map"
        mytuple = line.split(',')

        #print mytuple[0]
        #print ""
        yield mytuple[0], 1


    @staticmethod
    def combiner(key, value, buffer, done, params):
        if not done:
            # Ensure variable is defined
            try:
                buffer[key]
            except KeyError:
                buffer[key] = None

            # Test whether variable is defined to be None
            if buffer[key] is None:
                buffer[key] = 1
            else:
                buffer[key] += 1

        else :
            for key_, value_ in buffer.items():
                yield key_, value_

            buffer.clear()

    @staticmethod
    def reduce(iter, params):
        #print " ============= reduce =================="
        from disco.util import kvgroup
        import redis
        redis_con = redis.Redis('localhost')

        for key, counts in kvgroup(sorted(iter)):
            sum_counts = sum(counts)
            yield key, sum_counts
            redis_con.zadd('userHistogramm', key, sum_counts )



