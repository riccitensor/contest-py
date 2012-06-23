import json

__author__ = 'karisu'


from disco.job import Job


class Create_User_Average_Item(Job):
    """ from all the single ratings we are making a USER x ITEM Matrix

    """
    debug = False

    @staticmethod
    def map(line, params):
        mytuple = line.split()

        yield "average", mytuple[1]
        yield "user_num", 1


    @staticmethod
    def combiner(key, value, buffer, done, params):
        if not done:
            # Ensure variable is defined
            try:
                buffer[key]
            except KeyError:
                buffer[key] = 0

            # Test whether variable is defined to be None
            if buffer[key] is None:
                buffer[key] = int(value)
            else:
                buffer[key] += int(value)

        else :
            for key_, value_ in buffer.items():
                yield key_, value_

            buffer.clear()


    """
    @staticmethod
    def partition(key, nrp, params):
        return int(key) % int(nrp)
    """


    @staticmethod
    def reduce(iter, params):
        from disco.util import kvgroup

        for key, counts in kvgroup(sorted(iter)):
            sum_counts = sum(counts)
            #print "reduce: sum_counts {}".format(sum_counts)
            yield key, sum_counts

