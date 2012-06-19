import json

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
        userid json of all items
        """

        yield "userid", 1


    @staticmethod
    def reduce(iter, params):
        """
        """
        yield "bla", 1




