__author__ = 'karisu'
from disco.worker.classic.func import chain_reader

from disco.job import Job
import disco

class FirstJob(Job):
    @staticmethod
    def map(line, params):
        #print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1"
        mytuple = line.split(',')
        yield "userid:{}".format(mytuple[0]), 1
        yield "numlines", 1


    @staticmethod
    def reduce(iter, params):
        from disco.util import kvgroup

        for word, counts in kvgroup(sorted(iter)):
            yield word, sum(counts)



class SecondJob(Job):
    map_reader = staticmethod(chain_reader)

    @staticmethod
    def map(line, params):
        #print "============= MAP 2 =================="
        #print line
        yield "numusers", 1
        mytuple = line
        if mytuple[1] > 10:
            yield mytuple[0], 1


    @staticmethod
    def reduce(iter, params):
        from disco.util import kvgroup

        # print " ============ REDUCE ============"
        for word, counts in kvgroup(sorted(iter)):
            yield word, sum(counts)
