from disco.core import result_iterator

__author__ = 'karisu'

import unittest
import redis
from Create_Item_Coocurrence import Create_Item_Coocurrence
import disco

from test_scripts.disco.Create_User_Item_Matrix import Create_User_Item_Matrix


class Test_Create_User_Item(unittest.TestCase):

    redis_con = None

    def setUp(self):
        pass
        self.redis_con = redis.Redis('localhost')
        self.redis_con.flushall()


    def tearDown(self):
        pass


    def test_CF(self):
        # todo create testData
        line = "1 1,2,10"
        result = Create_Item_Coocurrence.map(line, None)
        for i in result:
            print i

        # todo calculate coocurrences


        # todo calculate jaccard coefficent



        # test

    def test_CF_map_reduce(self):
        location = "http://localhost/user_item_matrix"

        # 1. create coocurences
        data = Create_Item_Coocurrence().run(input=[location])

        for key, value in result_iterator(data.wait(show=True)):
            print key, value

        # todo 2. compute jaccard coefficient


        # todo 3. make a recommendation










