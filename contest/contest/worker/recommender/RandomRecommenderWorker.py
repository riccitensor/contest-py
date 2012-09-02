import pika
import time
import json
from contest.controller.constants import MESSAGE_TYPE_IMPRESSION

from contest.packages.message_parsers.FullContestMessageParser import FullContestMessageParser

class RandomRecommenderWorker(object):
    queue_name = "random_recommender"
    routing_key = "randon_recommender_routing_key"

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
        """
        in the body is metadata and the main information
        """
        print " RandomRecommender: %r" % body + "and written to redis"
        ch.basic_ack(delivery_tag = method.delivery_tag)



    def uncompress_message(self, body):
        body = json.loads(body)
        message = body['message']
        fP = FullContestMessageParser()
        fP.parse(message)
        metadata = None

        return metadata, fP

    def compress_message(self, metadata, message):
        # TODO implement
        pass

    def enqueue(self, metadata, message):

        body = json.dumps( (metadata, message))
        self.channel.basic_publish(exchange='',
                                   routing_key=self.routing_key,
                                   body=body)

    def process_message(self, message):
        message_instance = FullContestMessageParser()
        message_instance.parse(message)

        if message_instance.message_type == MESSAGE_TYPE_IMPRESSION:

            pass

if __name__ == '__main__':
    rw = RandomRecommenderWorker()
    rw.main()