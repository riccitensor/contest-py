'''
Created on 24.11.2011

@author: christian.winkelmann@plista.com
'''
import unittest
import redis
from contest.packages.message_parsers.default_parser import default_parser
import json

# TODO Fix this unitTest
class default_parser_test(unittest.TestCase):
    
    
    def setUp(self):
        
        self.redis_con = redis.Redis("localhost")
        self.redis_con.flushall()


    def tearDown(self):
        self.redis_con.flushall()


    def test_parse_Normal_Single_Request_Message(self):
        """
        suppose you want to recommend an item. 
        You only have one item to recommend which unfortunatly is the one the user already sees.
        Recommending this is better then nothing
        """            
        
        df = default_parser()

        message = "{\"msg\":\"impression\",\"id\":1300277,\"client\":{\"id\":1},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"1234\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        df.enqueue( message )
        message = "{\"msg\":\"impression\",\"id\":1300277,\"client\":{\"id\":2},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"5678\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        df.enqueue(message)

        message = "{\"msg\":\"impression\",\"id\":1300277,\"client\":{\"id\":3},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"58509770\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        desired_result1 =  "{\"msg\": \"result\", \"items\": [{\"id\": \"1234\"}], \"version\": \"1.0\", \"team\": {\"id\": \"22\"}}"
        desired_result2 =  "{\"msg\": \"result\", \"items\": [{\"id\": \"5678\"}], \"version\": \"1.0\", \"team\": {\"id\": \"22\"}}"
        result_message = df.enqueue(message)
        result_message = json.loads(result_message)
        
        self.assertTrue( ( u'msg' in result_message ), 'the parser does not even return a message')
        self.assertTrue( ( result_message[u'msg'] == 'result' ), 'the parser does not return a result message ')
        
        print result_message
        # be aware: this will fail currently once in a while because the algorithm doesn't check if the currently viewed item is the same the one recommended
        self.assertTrue( ( ( result_message == json.loads(desired_result1) ) or 
                           ( result_message == json.loads(desired_result2) ) ), 
                        'the recommendation is the same item beeing currently viewed: ' + str(result_message[u'items']))
        
        self.assertTrue( ( len( result_message[u'items'] ) == 1 ), 'the number of recommended recommendation items is wrong' + str(result_message[u'items']))
        print json.dumps(result_message)
        
        
    def test_parse_Normal_Multi_Request_Message(self):
        """
        suppose you want more then one recommendation
        """
        df = default_parser()
        
        message = "{\"msg\":\"impression\",\"id\":2,\"client\":{\"id\":1},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"1234\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        df.enqueue(message)
        message = "{\"msg\":\"impression\",\"id\":3,\"client\":{\"id\":2},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"5678\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        df.enqueue(message)
        message = "{\"msg\":\"impression\",\"id\":4,\"client\":{\"id\":3},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"9012\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        df.enqueue(message)
        message = "{\"msg\":\"impression\",\"id\":5,\"client\":{\"id\":4},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"3456\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
        df.enqueue(message)

    
        message = """{\"msg\":\"impression\",\"id\":1300277,\"client\":{\"id\":565639045},
        \"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"58509770\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":2,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"""
    
        result_message = df.enqueue(message)
        result_message = json.loads(result_message)
        self.assertTrue( ( u'msg' in result_message ), 'the parser does not even return a message')
        self.assertTrue( ( result_message[u'msg'] == 'result' ), 'the parser does not return a result message ')
        self.assertTrue( ( len( result_message[u'items'] ) == 2 ), 'the number of recommended items is wrong')
        
        # be aware: this will fail currently once in a while because there is no checking if duplicates are put in the list
        self.assertFalse ( self.list_has_duplicate_items(result_message[u'items']), 'the list has duplicate entries for recommendation items' + str( result_message[u'items']) )
        print json.dumps(result_message)    
        
    
    def list_has_duplicate_items(self, L ):
        for item in L:
            if L.count(item) > 1:
                return True
        return False


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_parse_Normal_Request_Message']
    
    unittest.main()
    
    