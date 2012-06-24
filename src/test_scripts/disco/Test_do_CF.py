from disco.core import result_iterator
from Create_Arbitrary_Item_Similarities import Create_Arbitrary_Item_Similarities




import unittest
import redis
from Create_Norms import Create_Norms
from Create_Item_Coocurrence import Create_Item_Coocurrence

__author__ = 'karisu'






class Test_Do_CF(unittest.TestCase):

    redis_con = None

    def setUp(self):
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
            print type(value)
            print "sum {} ".format( value[1,:].sum() )
            print key, value



        # todo 2. compute jaccard coefficient
        # todo 2.1  implement preprocess, but not necessary with binary data
        # todo 2.2. implement norm
        # todo 2.3  implement dot_i_j
        # todo implement S_i_j = similarity(dot_i_j, n_i, n_j)


        # todo 3. make a recommendation


    def test_CF_Arbitrary_Sim(self):
        location = "http://localhost/user_item_matrix"

        norms = Create_Norms().run(input=[location]).wait(show=False)

    # 1. create coocurences
        data = Create_Arbitrary_Item_Similarities().run(input=[location])


        for key, value in result_iterator(data.wait(show=True)):
            #print type(value)
            #print "sum {} ".format( value[1,:].sum() )
            print key, value
            #print value.toarray()


            # todo 3. make a recommendation










