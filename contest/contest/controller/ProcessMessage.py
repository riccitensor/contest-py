'''
Created on 24.08.2012



@author: christian.winkelmann@plista.com
'''
import logging
from contest.controller.ProcessMessage_Impression import ProcessMessage_Impression
from contest.packages.message_parsers.FullContestMessageParser import FullContestMessageParser
from contest.controller.constants import *
from contest.controller.constants import MESSAGE_TYPE_IMPRESSION
import pika
import pickle
import cPickle

import json
from contest.packages.recommenders.Random_Recommender import Random_Recommender

class ProcessMessage(object):

    message = ""
    result_message = "{}"

    def __init__(self, message):
        """ @param message a contest message which has to be parsed and processed
        """
        logging.basicConfig(filename='plista-contest.log',level=logging.DEBUG)



        message_instance = FullContestMessageParser()
        message_instance.parse(message)

        if message_instance.message_type == MESSAGE_TYPE_IMPRESSION:
            pI = ProcessMessage_Impression(message_instance)
            self.result_message = pI.result

        debug = True ## TODO !! local debugging statement
        debug = False
        if not debug:
            pMW = ProcessMessageWorker()
            pMW.enqueue(None, message)
        else:
            pmW = ProcessMessageWorker()
            pmW.log_data(message_instance)
            pmW.train_recommender(message_instance)





class ProcessMessageWorker(object):
    queue_name = "process"
    routing_key = "process"

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost')) # todo this needs to be configured via a config
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)


    def main(self):
        """ main function """

        print ' [*] Waiting for messages. To exit press CTRL+C'

        self.channel.basic_consume(self.callback,
                                   queue=self.queue_name)
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        """ in the body is metadata and the main information """
        _body = cPickle.loads(body)
        self.process_message(_body['message'])
        print _body


        ch.basic_ack(delivery_tag = method.delivery_tag) # send an ack

    def enqueue(self, metadata, message):
        body = {"metadata":metadata, "message":message}
        _body = cPickle.dumps(body)
        self.channel.basic_publish(exchange='',
                                   routing_key=self.routing_key,
                                   body=_body)



    def process_message(self, message):
        fP = FullContestMessageParser()
        fP.parse(message)

        self.log_data(fP)
        self.train_recommender(fP)



    def log_data(self, message):
        """
            @type message: FullContestMessageParser
            @param message: a general message.
        """
        # TODO write data to log files
        # TODO write statistics
        logger = logging.getLogger("processMessage:")

        logger.info(message)

    def train_recommender(self, message):
        """
            @type message: FullContestMessageParser
            @param message: a general message.
        """
        rrW = Random_Recommender()
        rrW.set_recommendables( message.item_id, { 'domainid' : message.domain_id } )
        rrW.train(message.user_id, { 'domainid' : message.domain_id })


if __name__ == '__main__':
    rw = ProcessMessageWorker()
    rw.main()