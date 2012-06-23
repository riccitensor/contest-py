import json

__author__ = 'karisu'


from disco.job import Job


class Create_Filter_Users_below_average(Job):
    """ Map Reduce Job to filter users which have lesser then X items seen
    """
    debug = False

    @staticmethod
    def map(line, params):
        mytuple = line.split()

        if int(mytuple[1]) > 7:
            yield int(mytuple[0]), int(mytuple[1])




    @staticmethod
    def partition(key, nrp, params):
        return int(key) % int(nrp)



    @staticmethod
    def reduce(iter, params):
        from disco.util import kvgroup

        for key, impressions in kvgroup(sorted(iter)):
            sum_impression = sum(impressions)
            yield key, sum_impression

