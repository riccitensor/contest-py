'''
Created on 23.05.2012

quite basic recommender which bases recommending random items, but exclude items alredy seen and is therefore 
individual for each user. For unknown users other dimensions can be taken like their browser or publisher

@author: christian.winkelmann@plista.com
'''
import logging
from contest.packages.recommenders.baseRecommender import baseRecommender
from contest.packages.models.RecommendationList import RecommendationList
import redis
import random

class Random_Recommender(baseRecommender):
    '''
    this will be the most naive recommender which just outputs random recommendations
    '''
    key = None

    userid = None

    def __init__(self):
        super(Random_Recommender, self).__init__()
        self.redis_con = redis.Redis("localhost")


    def compute_key(self, constraints, userid=None):
        itemList = "recommendable_items"
        if userid is None: suffix = ""
        else: suffix = ":userid:{}".format(userid)

        for key, value in constraints.items():
            suffix += ":{}:{}".format(str(key), str(value))
        key = itemList + suffix

        return key

    def compute_recommendationsListKey(self, constraints, userid=None):
        itemList = "recommendationList"
        if userid is None: suffix = ""
        else: suffix = ":userid:{}".format(userid)

        for key, value in constraints.items():
            suffix += ":{}:{}".format(str(key), str(value))
        key = itemList + suffix

        return key

    def compute_recommendablesKey(self):
        # todo implement this
        pass

    def get_recommendation(self, userid, constraints, N, remove=False, ranked=False):
        """ fetch a random recommendation
        @param N number of recommendations
        @param itemids which should be ignored
        """
        #
        key = self.compute_recommendationsListKey(constraints, userid)
        if not ranked:
            resultSet = self.redis_con.zrevrange(key, 0, N - 1)
        elif ranked:
            resultSet = self.redis_con.zrevrange(key, 0, N - 1, withscores=True)

        if remove: self.invalidate_recommended_items(key, resultSet)

        return resultSet

        '''
        @param userid: even though the recommendations are random we have to exclude items we already presented '''
        # todo grab the items and create a random list

        # @todo first get all recommendable items

        # @todo get the items the user has seen already seen, or other excluding factors

        # @todo compute the list of recommendations
        #self.userid

        #recList = RecommendationList(self.key, mode='redis')
        #recList = recList.get()
        #return recList


    def train(self, userid, addition_filter, N=10 ):

        recommendable_key = self.compute_key(addition_filter)
        recommendationList_key = self.compute_recommendationsListKey( addition_filter, userid)

        recList = []
        i = 0
        if (
            self.get_amount_of_recommendables(
                recommendable_key) >= N): #we have more items then we have to ignore + we need
            while i < N:
                recommendable_item = self.get_recommendable_item(key=recommendable_key)

                if recommendable_item in recList:
                    pass
                else:
                    recList.append(recommendable_item) # now compose the list of recommendable items
                    i += 1
        else:
            for i in xrange(N):
                # todo this is not covered in a unitTest
                recommendable_item = self.get_recommendable_item(key=recommendable_key)
                recList.append(recommendable_item)

        logging.debug('getting :' + str(N) + " recommendation, which are: " + str(recList))

        for value in recList:
            self.redis_con.zadd(recommendationList_key, value, random.random()) # we are giving the actual score

        return recList


    def train_filter(self, N=10, additional_filter=None):
        """ compute a random recommendation
        due to limitations like domain specific articles there should be restrictions

        @param N number of recommendations
        @param itemids which should be ignored
        """

        if additional_filter is None:
            # grab all the filters which exist and do a recursion with them
            pass

        else:
            available_items_key = self.itemList

            recList = []
            i = 0
            if (self.redis_con.scard(self.itemList) >= len(
                ignores) + N): #we have more items then we have to ignore + we need
                while (i < N):
                    recommendable_item = self.redis_con.srandmember(
                        available_items_key) # select possible item which meets the conditions
                    if (recommendable_item in ignores):
                        pass
                    elif (recommendable_item in recList):
                        pass
                    else:
                        recList.append(recommendable_item) # now compose the list of recommendable items
                        i += 1
            else:
                for i in xrange(N):
                    recommendable_item = self.redis_con.srandmember(self.itemList)
                    recList.append(recommendable_item)

            #print recList
            logging.debug('getting :' + str(N) + " recommendation, which are: " + str(recList))

            for value in recList:
                self.redis_con.zadd(self.key, value, random.random())

                # return recList


    #recommendationList = RecommendationList('userid:item' + str(userid), mode = 'redis')



    def set_recommendables(self, itemid, additional_filter={}, key=None):
        """ set a recommendable item, globally and with the given constraints """
        logging.debug('fallback_random: saving a recommendable item' + str(itemid))
        #TODO the filters need to be orthographically sorted
        if key is None:
            key = self.compute_key(additional_filter)
        self.redis_con.sadd(key, itemid)


    def get_recommendable_item(self, additional_filter=None, key=None):
        if key is None:
            key = self.compute_key(additional_filter)

        recommendable_item = self.redis_con.srandmember(key)
        return recommendable_item


    def get_amount_of_recommendables(self, key ):
        return self.redis_con.scard(key)


    def del_recommendables(self, itemid, additional_filter):
        """ delete an recommendable item again """

        self.redis_con.srem(self.itemList, itemid)


    def invalidate_recommended_items(self, key, recommendet_item_list):
        ''' already recommendet items should be shown again so soon
        '''
        for item in recommendet_item_list:
            if type(item) == type(()):
                self.redis_con.zrem(key, item[0])
            else:
                self.redis_con.zrem(key, item)

if __name__ == '__main__':
    '''
    '''


