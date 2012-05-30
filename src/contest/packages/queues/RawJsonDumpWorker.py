'''
Created on 27.12.2011

@author: christian.winkelmann@plista.com
'''
import sys
sys.path.append("/home/karisu/workspace/plistaContest/src/") 

import pika
import time
import redis
import sqlite3
from contest.config import config_local, config_global
from contest.packages.queues.QueueBase import QueueBase
from contest.packages.models.rawJsonModel import rawJsonModel


class rawJsonDumpWorker(QueueBase):
	'''
	save the raw json files somehow asynchronously and maybe remotely
	'''
	queue_name = 'rawJsonDump'
	routing_key = 'rawJsonDump'
	
	mode = 'redis' 

	def __init__(self, mode):
		''' '''
		self.mode = mode
		
	def callback(self, ch, method, properties, body):

		print body
		#print "rawJsonDump received a task %r" % (body)
		timestamp = time.time()
		
		raw = rawJsonModel( self.mode )
		raw.parse(body)
		raw.writeback(); 

	
	
		
	
	def writeToCassandra(self, timestamp, body):
		''' @todo: implement this '''
		""" no we are going to write the data into cassandra """
		
		""" 1. write down the raw data for later use with the timestamp of input """
		
		""" 2. save the itemid as they are. No more data. Usefull for 'joins' """
			
		""" 3. save the userid as they are. """
		
		""" 4. save the whole item """
		
		

			
	
	
		
if __name__ == '__main__':
	""" this class has an enqueue function and a worker function as well
	"""
	
	rw = rawJsonDumpWorker(mode = 'redis')
	rw.work()		