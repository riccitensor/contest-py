import json

__author__ = 'karisu'


from disco.job import Job
from disco.worker.classic.func import chain_reader


class Create_User_Item_Matrix(Job):
    """ from all the single ratings we are making a USER x ITEM Matrix

    """
    debug = False

    @staticmethod
    def map(line, params):
        """
        userid,itemid,rating
        """
        _tuple = line.split(',')
        userid = _tuple[0]
        itemid = int(_tuple[1])

        yield userid, itemid


    @staticmethod
    def reduce(iter, params):
        """

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



