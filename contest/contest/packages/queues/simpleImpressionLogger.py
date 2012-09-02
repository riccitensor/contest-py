#===============================================================================
# '''
# Created on 04.12.2011
# 
# @author: christian.winkelmann@plista.com
# '''
# import pika
# import redis
# import time
# 
# from contest.config import config_local
# 
# from plistaContestTransportLayer.packages.message_parsers.default_parser import default_parser
# 
# class simpleImpressionLogger(object):
#    '''
#    just save the user id and the item id. 
#    1. sorted list of items and their age
#    2. sorted list of users and their last appearance
#    3. one list for each user for items he has already seen ( for user based CF )
#    4. one list for each item and users who have seen it ( for item based CF )
#    5. save the raw message in a persistent storage like mysql or better in a cassandra cluster
#    6. save the raw message in a file
#    '''
#    queueName = ""
#    
#    def __init__(self, params):
#        '''
#        '''
#        self.redis_con = redis.Redis( config_local.config_redis_server_basic )
#        self.queueName = "test" """ @todo refactor this for a) exchanges b) with a config """
#        
#        
#    def save_item_with_age(self, msg):
#        pass
#    
#    def work(self):
#        """ first stage of consuming the message """    
#    
#    def main(self):    
#        """ main function """
# 
#        connection = pika.BlockingConnection(pika.ConnectionParameters(
#                host=config_local.config_rabbitmq_server ))
#        channel = connection.channel()
#        
#        channel.queue_declare(queue= self.queueName)
#        
#        print str( time.time() ) + ' [*] started Basic Impression logger To exit press CTRL+C'
#                
#        channel.basic_consume(self.parse_message,
#                              queue= self.queueName,
#                              no_ack=True)
#        
#        channel.start_consuming()
#        
#    def parse_message(self, ch, method, properties, body):
#        """ @todo change this"""
#        time.sleep(2.5)
#        print " [2] Received %r" % (body) + "and written to redis"
#        self.enqueue(body)
# 
#    
#        
# if __name__ == '__main__':
#    simpleImpressionLogger = simpleImpressionLogger()
#    # start the main process
#    simpleImpressionLogger.main()        
#===============================================================================