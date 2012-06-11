'''
Created on 18.05.2012

Recommender which is recommends depending on the message the best item

@author: christian.winkelmann@plista.com
'''
from contest.packages.message_parsers.fullParser import FullContestMessageParser
from contest.packages.recommenders.Random_Recommender import Random_Recommender


class GeneralRecommender(object):
    resultSet = None

    def __init__(self, json_string, async=False, api='contest', backends=[], type='onsite'):
        '''
        Constructor
        '''


    def recommend(self):
        """ lets hope there are recommendation ready for this user/constraint """
        return self.resultSet









