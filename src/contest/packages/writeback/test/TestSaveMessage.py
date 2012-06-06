from contest.config import config_global
from contest.packages.helper.getTimestamp import getTimestamp
from contest.packages.models.rawJsonModel import rawJsonModel
from contest.packages.recommenders.Random_Recommender import Random_Recommender

__author__ = 'cw'

import unittest
from contest.packages.writeback.SaveMessage import SaveMessage


class SaveMessageTest(unittest.TestCase):
    def setUp(self):
        """

        """

    def saveJson(self, backends):
        messages = []

        message = "{\"msg\":\"impression\",\"id\":3,\"client\":{\"id\":2},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"5678\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        messages.append(message)

        message = "{\"msg\":\"impression\",\"id\":4,\"client\":{\"id\":2},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"5678\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        messages.append(message)

        message = "{\"msg\":\"impression\",\"id\":5,\"client\":{\"id\":2},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"5678\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        messages.append(message)

        for m in messages:
            sM = SaveMessage()
            sM.save(m, async=False, api='contest', backends=backends)


    def test_SaveMessage_rawJsonModel(self):
        backend = [config_global.SAVE_RAW_JSON]
        self.saveJson(backend)

        N = 2
        raw = rawJsonModel()
        rawJson = raw.getN(N)
        self.assertEqual(N, len(rawJson))

        N = 4
        rawJson = raw.getN(N)
        self.assertEqual(N, len(rawJson))


    def test_SaveMessage_interpretedJson(self):
        ''' tests the generation of the writeBack of the interpreted data coming in from the contest messages
        '''
        backends = [config_global.SAVE_HADOOP_SINK, config_global.SAVE_RANDOM_RECOMMENDER]
        userid = 5678
        domainid = 8

        sM = SaveMessage()
        for itemid in xrange(5):
            timestamp = getTimestamp.gettimeStampInMicroseconds()
            id_list = {'userid': userid, 'itemid': itemid, 'timestamp': timestamp, 'domainid': domainid}

            sM.save(id_list, async=False, api='id_list', backends=backends)

    def test_SaveMessage_interpretedJson_async(self):
        ''' tests the generation of the writeBack of the interpreted data coming in from the contest messages
        '''
        backends = [config_global.SAVE_HADOOP_SINK, config_global.SAVE_RANDOM_RECOMMENDER]
        userid = 5678
        domainid = 8

        sM = SaveMessage()
        for itemid in xrange(5):
            timestamp = getTimestamp.gettimeStampInMicroseconds()
            id_list = {'userid': userid, 'itemid': itemid, 'timestamp': timestamp, 'domainid': domainid}

            sM.save(id_list, async=True, api='id_list', backends=backends)


    def test_SaveMessage_userStats(self):
        ''' tests the generation of statistics from the incoming stream of data
        '''
        pass


    def test_RandomRecommender(self):
        backend = [config_global.SAVE_RANDOM_RECOMMENDER]
        self.saveJson(backend)

        fb = Random_Recommender()
        additional_filter_1 = {'domainid': 'domain1'}
        fb.train(userid, additional_filter_1) # train for the specific user and the filter

        resultSet_1 = fb.get_recommendation(userid, additional_filter_1, N=N, remove=False)

if __name__ == '__main__':
    unittest.main()
