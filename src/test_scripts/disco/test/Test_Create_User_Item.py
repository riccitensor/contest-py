__author__ = 'karisu'

import unittest
from test_scripts.disco.Create_User_Item_Matrix import Create_User_Item_Matrix

class Test_Create_User_Item(unittest.TestCase):

    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testMap(self):
        line = "1,2"

        Create_User_Item_Matrix().map(line)


