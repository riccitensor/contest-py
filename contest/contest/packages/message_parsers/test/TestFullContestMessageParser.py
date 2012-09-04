from contest.packages.message_parsers.FullContestMessageParser import FullContestMessageParser

__author__ = 'cw'

import unittest
import json
import logging

class TestFullParser(unittest.TestCase):
    def setUp(self):
        '''
        '''
        logging.basicConfig(filename='plista-contest.log',level=logging.DEBUG)


    def tearDown(self):
        '''
        '''


    def test_parse_Normal_Single_Request_Message(self):
        """
        suppose you want to recommend an item.
        You only have one item to recommend which unfortunatly is the one the user already sees.
        Recommending this is better then nothing
        """

        fP = FullContestMessageParser()

        message = "{\"msg\":\"impression\",\"id\":1300277,\"client\":{\"id\":1},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"1234\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        fP.parse(message)

        print fP.flattenedJson

        self.assertEqual(fP.message_id, 1300277, "message id not correctly parsed")
        self.assertEqual(fP.user_id, 1, "user id not correctly parsed")
        self.assertEqual(fP.domain_id, 418, "domain id not correctly parsed")
        self.assertEqual(fP.message_type, 'impression', "message type not correctly parsed")


    def test_parse_contest_message_1(self):
        """
        suppose you want to recommend an item.
        You only have one item to recommend which unfortunatly is the one the user already sees.
        Recommending this is better then nothing
        """
        null = None
        true = True
        fP = FullContestMessageParser()

        message = {"msg":"impression","id":100222,"client":{"id":545639506},"domain":{"id":"418"},"item":{"id":"52400652","title":"EURO 2012: Diese Teams sind schon durch","url":"http:\/\/www.ksta.de\/html\/fotolines\/1318344142825\/rahmen.shtml?1","created":1318417485,"text":"Mit zehn Siegen in zehn Spielen hat sich Deutsch\u00adland souve\u00adr\u00e4n das Ticket f\u00fcr die Euro\u00adpa\u00admeis\u00adte\u00adschaft im kommenden Sommer gesi\u00adchert. (Bild: dpa)","img":null,"recommendable":true},"config":{"timeout":null,"recommend":true,"limit":4},"version":"1.0"}
        message = json.dumps(message)
        fP.parse(message)

        print fP.flattenedJson

        self.assertEqual(fP.message_id, 100222, "message id not correctly parsed")
        self.assertEqual(fP.user_id, 545639506, "user id not correctly parsed")
        self.assertEqual(fP.domain_id, 418, "domain id not correctly parsed")
        self.assertEqual(fP.message_type, 'impression', "message type not correctly parsed")
        self.assertEqual(fP.item_title, 'EURO 2012: Diese Teams sind schon durch', "item title not parsed")
        self.assertEqual(fP.config_recommend, True, "config recommend not parsed")
        self.assertEqual(fP.config_limit, 4, "limit not correctly parsed")

    def test_parse_contest_message_2(self):
        """
        suppose you want to recommend an item.
        You only have one item to recommend which unfortunatly is the one the user already sees.
        Recommending this is better then nothing
        """
        null = None
        true = True
        fP = FullContestMessageParser()

        message = {"msg":"impression","id":100216,"client":{"id":545639506},"domain":{"id":"418"},"item":{"id":"52400652","title":"EURO 2012: Diese Teams sind schon durch","url":"http:\/\/www.ksta.de\/html\/fotolines\/1318344142825\/rahmen.shtml?1","created":1318417485,"text":"Mit zehn Siegen in zehn Spielen hat sich Deutsch\u00adland souve\u00adr\u00e4n das Ticket f\u00fcr die Euro\u00adpa\u00admeis\u00adte\u00adschaft im kommenden Sommer gesi\u00adchert. (Bild: dpa)","img":null,"recommendable":true},"config":{"timeout":null,"recommend":true,"limit":1},"version":"1.0"}
        message = json.dumps(message)
        fP.parse(message)

        print fP.flattenedJson

        self.assertEqual(fP.message_id, 100216, "message id not correctly parsed")
        self.assertEqual(fP.user_id, 545639506, "user id not correctly parsed")
        self.assertEqual(fP.domain_id, 418, "domain id not correctly parsed")
        self.assertEqual(fP.message_type, 'impression', "message type not correctly parsed")
        self.assertEqual(fP.item_title, 'EURO 2012: Diese Teams sind schon durch', "item title not parsed")
        self.assertEqual(fP.config_recommend, True, "config recommend not parsed")
        self.assertEqual(fP.item_recommendable, True, "config recommend not parsed")
        self.assertEqual(fP.config_limit, 1, "limit not correctly parsed")





    def test_parse_feedback_message_1(self):

        message = {"msg":"feedback","client":{"id":"552220965"},"domain":{"id":418},"source":{"id":"2314"},"target":{"id":53082765},"version":"1.0"}
        message = json.dumps(message)
        fP = FullContestMessageParser()
        fP.parse(message)
        print fP.flattenedJson

        self.assertEqual(fP.user_id, 552220965, "user id not correctly parsed")
        self.assertEqual(fP.domain_id, 418, "domain id not correctly parsed")
        self.assertEqual(fP.message_type, 'feedback', "message type not correctly parsed")
        self.assertEqual(fP.source_id, 2314, "source id not correctly parsed")
        self.assertEqual(fP.target_id, 53082765, "source id not correctly parsed")
        self.assertEqual(fP.version, 1.0, "version not correctly parsed")

        #self.item_text


    def test_parse_feedback_message_team_id(self):
        """
        message with a given team id
        """
        message = {"msg":"feedback","client":{"id":"552196182"},"domain":{"id":418},"source":{"id":"2311"},"target":{"id":52958956},"config":{"team":{"id":15}},"version":"1.0"}
        message = json.dumps(message)
        fP = FullContestMessageParser()
        fP.parse(message)
        print fP.flattenedJson

        self.assertEqual(fP.user_id, 552196182, "user id not correctly parsed")
        self.assertEqual(fP.domain_id, 418, "domain id not correctly parsed")
        self.assertEqual(fP.message_type, 'feedback', "domain id not correctly parsed")



if __name__ == '__main__':
    unittest.main()
