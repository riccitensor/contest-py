__author__ = 'karisu'

__author__ = 'karisu'

import unittest
from test_scripts.disco.Create_Item_Coocurrence import Create_Item_Coocurrence

class Test_Create_Item_Coocurrence(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testMap(self):
        line = "1 [1,2,3,4,5]"
        result = Create_Item_Coocurrence().map(line, params=None)

        for a,k in result:
            print "a: {} k: {}".format(a,k)



