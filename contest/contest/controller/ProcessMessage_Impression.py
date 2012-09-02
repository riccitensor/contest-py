from contest.packages.message_parsers.FullContestMessageParser import FullContestMessageParser
from contest.controller.constants import *

class ProcessMessage_Impression(object):
    """
    if the incoming message is an Impression do the following
    """
    message = ""
    result = "{}"

    def __init__(self, message):
        """ @param message an impression contest message
        """
        self.message = message

        if message.config_recommend:
            self.result = self.recommend(message)

        if message.item_recommendable:
            #trigger some sort of training
            pass




        # todo log raw the message somewhere




#    def __str__(self):
#        return "bla"

    def recommend(self, message):
        """ now the actual Recommendation is done """

        return "{result message}"
        