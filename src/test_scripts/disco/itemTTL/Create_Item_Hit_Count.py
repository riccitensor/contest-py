
from disco.job import Job

from disco.worker.classic.func import chain_reader


class Create_Item_Hit_Count(Job):
    """ from all the single ratings we are making a USER x ITEM Matrix

    """
    debug = False

    @staticmethod
    def map(line, params):
        print line
        print type(line)
        itemid = line[0]
        timestamp_count = len( line[1] )

        yield timestamp_count, itemid




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





