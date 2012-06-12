'''
Created on 18.05.2012

central station for all incoming messages

@author: christian.winkelmann@plista.com
'''
import pickle
from contest.config import config_global
from contest.packages.models.HadoopSink import HadoopSink
from contest.packages.models.rawJsonModel import rawJsonModel
from contest.packages.message_parsers.fullParser import FullContestMessageParser
from contest.packages.recommenders.Random_Recommender import Random_Recommender
from contest.packages.queues.QueueBase import QueueBase
from contest.packages.statistics.userStats import UserStats

class SaveMessage(QueueBase):
    ''' dump messages into various formats '''
    rawJson = None
    fullyParsed = None

    queue_name = 'SaveMessage'
    routing_key = 'SaveMessage'
    exchange_name = ''

    def __init__(self):
        '''
          get the message, parse it and then save
          '''


    def save(self, message, async=False, api='contest', backends=(), constraints={}):
        """
        """

        if not async: # save the data instantly

            if api == 'contest':
                self.save_contest(message, backends)

            elif api == 'orp':
                self.save_orp(message, backends)

            elif api == 'id_list':
                self.save_id_list(message, backends)


        # async case
        else:
            body_message = {'message': message,
                            'api': api,
                            'backends': backends}

            body_message = pickle.dumps(body_message)

            self.enqueue(body_message)


    def save_contest(self, message, backends):
        fullParsedDataModel = FullContestMessageParser()
        fullParsedDataModel.parse(message)
        fullParsedDataModel.save()

        itemid = fullParsedDataModel.item_id
        userid = fullParsedDataModel.user_id
        domainid = fullParsedDataModel.domain_id
        timestamp = 1 # todo get this from fullParsedDataModel

        if config_global.SAVE_RAW_JSON in backends:
            raw = rawJsonModel(message, mode='redis')
            raw.save()

        constraint = {'domainid': domainid}

        if config_global.SAVE_RANDOM_RECOMMENDER in backends:
            self.__save_random_recommender(itemid, constraint)

        if config_global.SAVE_HADOOP_SINK in backends:
            self.__save_hadoop_sink(userid, itemid, domainid, timestamp)

        if config_global.SAVE_USER_STATS in backends:
            self.__save_userstats('userid', userid, 'itemid', itemid)


    def save_orp(self, message):
        """ """


    def save_id_list(self, message, backends):
        userid = message['userid']
        itemid = message['itemid']
        timestamp = message['timestamp']
        domainid = message['domainid']

        # todo generate constraint set
        constraint = {'domainid': domainid}

        if config_global.SAVE_RANDOM_RECOMMENDER in backends:
            self.__save_random_recommender(itemid, constraint)

        if config_global.SAVE_HADOOP_SINK in backends:
            self.__save_hadoop_sink(userid, itemid, domainid, timestamp)

        if config_global.SAVE_USER_STATS in backends:
            self.__save_userstats('userid', userid, 'itemid', itemid)


    def __save_random_recommender(self, itemid, constraint={}):
        fb = Random_Recommender()
        fb.set_recommendables(itemid, constraint)


    def __save_hadoop_sink(self, userid, itemid, domainid, timestamp):
        hS = HadoopSink(append=True)
        rating = 1
        hS.save_mode2(userid, itemid, domainid, timestamp)


    def __save_userstats(self, idname1, id1, idname2, id2 ):
        us = UserStats(idname1, idname2)
        us.save(id1, id2)


    def callback(self, ch, method, properties, body):
        """ callback method to actually make this class work asynchronous """
        print "working..."
        body_message = pickle.loads(body)

        message = body_message['message']
        api = body_message['api']
        backends = body_message['backends']
        async = False
        print message

        self.save(message, async, api, backends)


if __name__ == '__main__':
    sM = SaveMessage()
    sM.work()



