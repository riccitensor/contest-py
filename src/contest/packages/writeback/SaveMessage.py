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
                fullParsedDataModel = FullContestMessageParser()
                fullParsedDataModel.parse(message)
                fullParsedDataModel.save()

                item_id = fullParsedDataModel.item_id

                if config_global.SAVE_RAW_JSON in backends:
                    raw = rawJsonModel(message, mode='redis')
                    raw.save()

                if config_global.SAVE_RANDOM_RECOMMENDER in backends:
                    fb = Random_Recommender()
                    domain_id = fullParsedDataModel.domain_id
                    ## todo the recommender has to decide on its own what to save and therefore save constraints, even though the constrain management should be centralized
                    #constraints = {'domainid': domain_id}
                    fb.set_recommendables(item_id, constraints)

            if api == 'orp':
                # todo throw not implemented error
                pass


            elif api == 'id_list': ## this for debugging purposes
                userid = message['userid']
                itemid = message['itemid']
                timestamp = message['timestamp']
                domainid = message['domainid']

                additional_filter = {'domainid': domainid}

                if config_global.SAVE_RANDOM_RECOMMENDER in backends:
                    fb = Random_Recommender()
                    fb.set_recommendables(itemid, additional_filter)

                if config_global.SAVE_HADOOP_SINK in backends:
                    hS = HadoopSink(append=True)
                    rating = 1
                    hS.save_mode2(userid, itemid, domainid, timestamp)

                if config_global.SAVE_USER_STATS in backends:
                    us = UserStats('userid', 'itemid')
                    us.save(userid, itemid)

                    #save sync
        else:
            body_message = {'message': message,
                            'api': api,
                            'backends': backends}

            body_message = pickle.dumps(body_message)

            self.enqueue(body_message)
            #from contest.packages.queues.RawJsonDumpWorker import rawJsonDumpWorker
            #raw = rawJsonDumpWorker(mode='redis')
            #raw.enqueue(message)


    def callback(self, ch, method, properties, body):
        """ """
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



