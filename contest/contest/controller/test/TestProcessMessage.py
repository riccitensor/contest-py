import unittest
import json
from contest.controller.ProcessMessage import *

class TestFullParser(unittest.TestCase):
    def setUp(self):
        """
        """


    def tearDown(self):
        """
        """




    def test_small_Integration(self):
        """
        send 10 impressions without any recommendation request
        send 1 impression with a recommendation request

        the result has to be non empty and with items among the first if they were recommendable
        """
        recommend_flag = False
        for i in range(1,20):
            message = self.get_custom_impression_message(
                id_flag = i, # autoincrement message ids
                client_id_flag = i % 3, # three users are making the impression
                item_id_flag = i % 6,
                recommendable_flag = i % 2,
                recommend_flag = recommend_flag,
                message_json = True
            )
            ProcessMessage(message)


        # compose a recommendation request message
        message = self.get_custom_impression_message(
            id_flag = 21,
            client_id_flag = 1, # three users are making the impression
            item_id_flag = 1,
            recommendable_flag = False,
            recommend_flag = True,
            message_json = True
        )

        # the result has to consist of 4 items
        pm = ProcessMessage(message)
        print pm.result_message






    def get_custom_impression_message(self, id_flag, client_id_flag, item_id_flag, recommendable_flag, recommend_flag, message_json = True):
        message = {"msg":"impression",
                   "id":id_flag,
                   "client":{"id":client_id_flag},
                   "domain":{"id":"418"},
                   "item":{"id":item_id_flag,
                           "title":"The Title Text",
                           "url":"http://url.de",
                           "created":"1318417485",
                           "text":"Mit zehn Siegen in zehn Spielen hat sich Deutsch\u00adland souve\u00adr\u00e4n das Ticket f\u00fcr die Euro\u00adpa\u00admeis\u00adte\u00adschaft im kommenden Sommer gesi\u00adchert. (Bild: dpa)",
                           "img":None,
                           "recommendable":recommendable_flag},
                   "config":{"timeout":None,
                             "recommend":recommend_flag,
                             "limit":4},
                   "version":"1.0"}

        if message_json:
            return json.dumps(message)
        else:
            return message


    def get_cusom_feedback_message(self, id_flag, client_id_flag, item_id_flag, recommendable_flag, recommend_flag, message_json = True):
        message = {"msg":"feedback",
                   "client":
                           {"id":"552196182"},
                   "domain":{"id":418},
                   "source":{"id":"2311"},
                   "target":{"id":52958956},
                   "config":{"team":{"id":15}},
                   "version":"1.0"}

        if message_json:
            return json.dumps(message)
        else:
            return message


    def get_custom_result_message(self):


        message = {"msg":"result",
                    "items":[
                        {"id":id_1},
                        {"id":id_2}
                    ],
                    "team":{"id":22},
                    "version":1.0
                    }
        return message

if __name__ == '__main__':
    unittest.main()
