'''
Created on 18.05.2012

Recommender which is recommends depending on the message the best item

@author: christian.winkelmann@plista.com
'''
from contest.packages.message_parsers.fullParser import FullContestMessageParser
from contest.packages.recommenders.Random_Recommender import Random_Recommender


class GeneralRecommender(object):
    resultSet = None

    def __init__(self, json_string, async=False, api='contest', backends=[]):
        '''
        Constructor
        '''
        self.backends = backends

        fullParsedDataModel = FullContestMessageParser()
        fullParsedDataModel.parse(json_string)

        domain_id = fullParsedDataModel.domain_id
        user_id = fullParsedDataModel.user_id
        additional_filter = {'domainid': domain_id}

        random_recommender = Random_Recommender()
        N = 4
        random_recommender.train(user_id, additional_filter)
        self.resultSet = random_recommender.get_recommendation(user_id, additional_filter, N=N, remove=False)

        # TODO parse the message to know what we are supposed to do: i.e. grab the constraints out of the data




        # TODO initialize a new training session if necessary

    def recomend(self):
        ''' lets hope there are recommendation ready for this user/constrain '''
        return self.resultSet









