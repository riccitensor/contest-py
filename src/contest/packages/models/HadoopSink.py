'''
Created on 12.02.2012

@author: karisu
'''

from contest.config import config_local, config_global
import cql
from cql.cassandra import Cassandra
from baseModel import baseModel
from contest.packages.helper.getTimestamp import getTimestamp
import time
import bisect
from sets import Set


class HadoopSink(baseModel):

	path = '/tmp/one_million_test'
	path = '/media/trekstor/one_million_test_bench' 
	
	def __init__(self, path = '/tmp/hadoopSink'):
		''' open target write location '''
		#self.f = open('/tmp/one_million_test', 'w')
		self.f = open(path, 'w')

	
	def save_mode1(self, user_id, item_id, rating):
		""" @param user_id: the user identification
		@param item_id: the item identification   
		just save a tuple user_id item_id
		and in the end a list of all users and all items
		"""
		
		
		klm = '{0:1d},{1:1d},{2:1d}'.format(user_id, item_id, rating)
		self.f.write(klm + '\n')

		
	def save_mode2(self, user_id, item_id, domainid, date):
		""" @param user_id: the user identification
		@param item_id: the item identification   
		just save a tuple user_id item_id
		and in the end a list of all users and all items
		"""
		
		
		klm = '{0:1d},{1:1d},{2:1d}'.format(user_id, item_id, domainid)
		self.f.write(klm + '\n')

if __name__ == '__main__':
	pass

	hS = HadoopSink()
	hS.save_mode2(1, 2, 1, "bla")
	
	
	
	
	