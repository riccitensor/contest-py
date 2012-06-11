'''
Created on 18.05.2012

Recommender which is recommends depending on the message the best item

@author: christian.winkelmann@plista.com
'''
from contest.packages.message_parsers.fullParser import FullContestMessageParser
from contest.packages.recommenders.GeneralRecommender import GeneralRecommender
from contest.packages.recommenders.Random_Recommender import Random_Recommender


class CrosssiteRecommender(GeneralRecommender):
    resultSet = None

    def __init__(self, json_string, async=False, api='contest', backends=[] ):
        '''
        Constructor
        '''
        self.backends = backends

        fullParsedDataModel = FullContestMessageParser()
        fullParsedDataModel.parse(json_string)

        user_id = fullParsedDataModel.user_id

        # now compile the constraints, which are important for an onsite Recommender: do not recommend item from another domain
        constraints = {}

        random_recommender = Random_Recommender()
        N = 4
        # TODO initialize a new training session if necessary
        random_recommender.train(user_id, constraints)
        self.resultSet = random_recommender.get_recommendation(user_id, constraints, N=N, remove=True)


    def recommend(self):
        """ lets hope there are recommendation ready for this user/constraint """
        return self.resultSet









