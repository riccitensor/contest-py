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
        line: userid json of all items
        """
        print line
        split = line.split()
        key = split[0]
        value = split[1]
        value = json.loads(value)

        # todo compute the outer product now

        # todo return these matrices
        yield key, value


    @staticmethod
    def reduce(iter, params):
        """
        item, matrix
        """
        from disco.util import kvgroup

        debug = False

        for userid, itemids in kvgroup(sorted(iter)):
            itemids_dict = {}
            for itemid in itemids:
                if debug:
                    print "reduce: userid:{} itemid:{}".format(userid, itemid)
                itemids_dict[itemid] = True

            itemids = itemids_dict.keys()
            yield userid, json.dumps(itemids)





