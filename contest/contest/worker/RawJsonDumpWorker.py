'''
Created on 27.12.2011

@author: christian.winkelmann@plista.com
'''
import sys
from contest.worker import QueueBase

sys.path.append("/home/karisu/workspace/plistaContest/src/")

import time
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

		# todo get the message from the body
		# todo parse relevant options from the body
		#print "rawJsonDump received a task %r" % (body)
		timestamp = time.time()
		
		raw = rawJsonModel( self.mode )
		raw.parse(body)
		raw.save()

		
if __name__ == '__main__':
	""" this class has an enqueue function and a worker function as well
	"""
	
	rw = rawJsonDumpWorker(mode = 'redis')
	rw.work()		