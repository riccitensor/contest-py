from contest.packages.message_parsers.FullContestMessageParser import FullContestMessageParser
from contest.controller.constants import *
from contest.packages.recommenders.Random_Recommender import *


class ProcessMessage_Impression(object):
    """
    if the incoming message is an Impression do the following
    """
    message = ""
    result = "{}"
    RANDOM_RECOMMENDER_ENABLED = True

    def __init__(self, message):
        """
            @type message: FullContestMessageParser
            @param message: a general message.
        """

        self.message = message

        if message.config_recommend:
            self.result = self.recommend(message)

        if message.item_recommendable:
            self.store_recommendable_item(message)




        # todo log raw the message somewhere




#    def __str__(self):
#        return "bla"

    def recommend(self, message):
        """ now the actual Recommendation is done """
        if self.RANDOM_RECOMMENDER_ENABLED:
            fb = Random_Recommender()
            domain_id = message.domain_id
            result = fb.get_recommendable_item( { 'domainid' : domain_id } )

        return result


    def store_recommendable_item(self, message):
        """ if the item is recommendable we need to do somehting with it
        @type message: FullContestMessageParser
        @param message: a general message.
        """



        if self.RANDOM_RECOMMENDER_ENABLED:
            fb = Random_Recommender()

            item_id = message.item_id
            domain_id = message.domain_id
            fb.set_recommendables( item_id, { 'domainid' : domain_id } )
        