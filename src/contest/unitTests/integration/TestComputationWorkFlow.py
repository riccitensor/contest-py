import unittest
import _mysql
from contest.config import config_local
from contest.packages.controller.http_connector import http_connector
from contest.packages.recommenders.GeneralRecommender import GeneralRecommender
from contest.packages.writeback.SaveMessage import SaveMessage
from contest.unitTests.integration.WorkFlowBase import WorkFlowBase

__author__ = 'karisu'


class TestComputation(unittest.TestCase):

    debug = True


    def setUp(self):
        #super(Indexing, self).__init__(training_id, db_location, local_execution = True)
        self.wfb = WorkFlowBase()
        self.wfb.setUp()

    def tearDown(self):
        self.wfb.tearDown()



    def test_train_recommender_with_impressions_only_contest(self):
        backends = [config_global.SAVE_HADOOP_SINK, config_global.SAVE_RANDOM_RECOMMENDER]
        self.debug = False

        if not self.debug:
            self.getResults()
            n_maxrows = 10 #amount of items fetched for training
            result = r.fetch_row(maxrows = n_maxrows) # fetch N row maximum
        else:
            result = self.mockMysqlResults()


        while result:
            for result_item in result:

                json_string = result_item[3]
                sM = SaveMessage()

                sM.save(json_string , async = False, api = 'contest', backends=backends)
                # todo something do something with the data


        # todo sleep for a short while

        # todo get a recommendation now
        GeneralRecommender()
