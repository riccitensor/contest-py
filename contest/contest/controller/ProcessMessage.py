'''
Created on 24.08.2012



@author: christian.winkelmann@plista.com
'''
from contest.controller.ProcessMessage_Impression import ProcessMessage_Impression
from contest.packages.message_parsers.FullContestMessageParser import FullContestMessageParser
from contest.controller.constants import *

import json

class ProcessMessage(object):

    message = ""
    result_message = "{}"

    def __init__(self, message):
        """ @param message a contest message which has to be parsed and processed
        """
        message_instance = FullContestMessageParser()
        message_instance.parse(message)

        if message_instance.message_type == MESSAGE_TYPE_IMPRESSION:
            pI = ProcessMessage_Impression(message_instance)

            self.result_message = json.dumps(pI.result)

        elif message_instance.message_type == MESSAGE_TYPE_FEEDBACK:
            pass
#            if message_instance.config_recommend:
#                self.result = self.recommend(parsed_message)
#            if message_instance.item_recommendable:
#                # trigger some sort of training
#                pass

        # TODO now we can enque the message


        # todo log raw the message somewhere




