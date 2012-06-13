import redis
from contest.packages.statistics.histogramm_graph import Plot_Helper
from contest.packages.models.ObjectByObject import ObjectByObject

__author__ = 'christian.winkelmann@plista.com'

import unittest

class TestObjectByObject(unittest.TestCase):
    def setUp(self):
        self.redis_con = redis.Redis('localhost')
        self.redis_con.flushall()

    def testStatsList(self):
        us = ObjectByObject('userid', 'itemid')
        us.save(1, 2)
        us.save(1, 3)
        us.save(1, 4)

        us.save(2, 2)
        us.save(2, 3)
        us.save(3, 4)
        us.save(4, 4)

        toplist = us.get_Top_N('userid', 3)
        print toplist
        self.assertEqual(len(toplist), 3, "toplist has not enough entries")
        toplist = us.get_Top_N('userid', 4)
        self.assertEqual(len(toplist), 4, "toplist has not enough entries")
        self.assertEqual(int(toplist[0][0]), 1, "")
        self.assertEqual(int(toplist[0][1]), 3, "")


    def test_plot_histogramm(self):
        the_list = [(154234234, 3.0), (2323232, 2.0), (5645343, 1.0)]
        us = ObjectByObject('userid', 'itemid')
        pH = Plot_Helper()
        pH.make_plot(the_list)


if __name__ == '__main__':
    unittest.main()
