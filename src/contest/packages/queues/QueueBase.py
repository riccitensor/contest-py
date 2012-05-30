'''
Created on 27.12.2011

@author: christian.winkelmann@plista.com
'''

import pika
from contest.config import config_local, config_global

class QueueBase(object):
	'''
	Base Class for all queues
	'''
	queue_name = None #overwrite this
	routing_key = None #overwrite this
	exchange_name = ''

	def __init__(self):
		''' empty '''
		
	def enqueue(self, _body):
		#print "create workload"
		""" @todo the connection itself has to be established over SINGLETON just ounce """
		connection = pika.BlockingConnection(pika.ConnectionParameters(
				host=config_global.config_rabbitmq_server))
		channel = connection.channel()
		
		channel.queue_declare(queue=self.queue_name)
		
		channel.basic_publish(exchange=self.exchange_name,
							  routing_key=self.routing_key,
							  body=_body)
		connection.close()
		
		return _body
		
		
		
		
	def work(self):	
		""" main function """

		connection = pika.BlockingConnection(pika.ConnectionParameters(
				host=config_global.config_rabbitmq_server))
		channel = connection.channel()
		
		channel.queue_declare(queue=self.queue_name)
		
		print ' [*] Waiting for messages. To exit press CTRL+C'
				
		channel.basic_consume(self.callback,
							  queue=self.queue_name,
							  no_ack=True)
		
		channel.start_consuming()
	
	def callback(self, ch, method, properties, body):
		''' @todo: overwrite this '''
	
	
		
