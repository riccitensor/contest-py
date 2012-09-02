import unittest
from contest.config import config_global
from contest.packages.recommenders.CrosssiteRecommender import CrosssiteRecommender
from contest.packages.recommenders.OnsiteRecommender import OnsiteRecommender
from contest.packages.writeback.SaveMessage import SaveMessage
from contest.unitTests.integration.WorkFlowBase import WorkFlowBase


class TestComputation(unittest.TestCase):
    debug = True


    def setUp(self):
        #super(Indexing, self).__init__(training_id, db_location, local_execution = True)
        self.wfb = WorkFlowBase()
        self.wfb.setUp()

    def tearDown(self):
        self.wfb.tearDown()


    def importTrainingData(self, backends):
        if not self.debug:
            self.getResults()
            n_maxrows = 10 #amount of items fetched for training
            result = r.fetch_row(maxrows=n_maxrows) # fetch N row maximum
        else:
            result = self.wfb.mockMysqlResults_domain418()
            result2 = self.wfb.mockMysqlResults_domain800()

        constraints = {'domainid': 418}
        for result_item in result:
            json_string = result_item[3]
            sM = SaveMessage()
            sM.save(json_string, async=False, api='contest', backends=backends, constraints=constraints)

        constraints = {'domainid': 800}
        for result_item in result2:
            json_string = result_item[3]
            sM = SaveMessage()
            sM.save(json_string, async=False, api='contest', backends=backends, constraints=constraints)

        for result_item in result:
            json_string = result_item[3]
            sM = SaveMessage()
            sM.save(json_string, async=False, api='contest', backends=backends, constraints={})

        for result_item in result2:
            json_string = result_item[3]
            sM = SaveMessage()
            sM.save(json_string, async=False, api='contest', backends=backends, constraints={})


    def test_train_recommender_with_impressions_only_contest(self):
        """
        todo this is an intermediate unit Test and it might be changed later on when the framework evolves
        """

        # backends = [config_global.SAVE_HADOOP_SINK, config_global.SAVE_RANDOM_RECOMMENDER]
        backends = [config_global.SAVE_RANDOM_RECOMMENDER]
        self.debug = True


        # todo something do something with the data

        self.importTrainingData(backends)

        message_418 = "{\"msg\":\"impression\",\"id\":1300277,\"client\":{\"id\":1},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"123\",\"title\":\"TEXT1\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        gR = OnsiteRecommender(message_418, async=False, api='contest', backends=backends)

        recList = gR.recommend()
        print recList
        self.assertGreater(len(recList), 0)

        message_800 = "{\"msg\":\"impression\",\"id\":1300280,\"client\":{\"id\":1},\"domain\":{\"id\":\"800\"},\"item\":{\"id\":\"999\",\"title\":\"TEXT1\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        gR = OnsiteRecommender(message_800, async=False, api='contest', backends=backends)

        recList = gR.recommend()
        print recList
        self.assertGreater(len(recList), 0)




        # todo sleep for a short while

        # todo get a recommendation now


    def test_train_recommender_with_impressions_only_contest_Crosssite(self):
        """
        todo this is an intermediate unit Test and it might be changed later on when the framework evolves
        """

        # backends = [config_global.SAVE_HADOOP_SINK, config_global.SAVE_RANDOM_RECOMMENDER]
        backends = [config_global.SAVE_RANDOM_RECOMMENDER]
        self.debug = True


        # todo something do something with the data

        self.importTrainingData(backends)

        message_418 = "{\"msg\":\"impression\",\"id\":1300277,\"client\":{\"id\":1},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"123\",\"title\":\"TEXT1\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        gR = CrosssiteRecommender(message_418, async=False, api='contest', backends=backends)

        recList = gR.recommend()
        print recList
        self.assertGreater(len(recList), 0)





        # todo sleep for a short while

        # todo get a recommendation now

