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




	def save(self, message, async=False, api = 'contest', backends = ()):
		"""

		"""
		if (not async): # save the data instantly

			if api == 'contest':
				fullParsedDataModel = FullContestMessageParser()
				parsedMessage = fullParsedDataModel.parse(message)
				fullParsedDataModel.save()

				raw = rawJsonModel(message, mode='redis')
				raw.save();

			if api == 'orp':
				""" todo """

			elif api == 'id_list': ## this for debugging purposes
				userid = message['userid']
				itemid = message['itemid']
				timestamp = message['timestamp']
				domainid = message['domainid']

				additional_filter = {'domainid' : domainid}

				if config_global.SAVE_RANDOM_RECOMMENDER in backends:
					fb = Random_Recommender( )
					fb.set_recommendables(itemid, additional_filter)
				if config_global.SAVE_HADOOP_SINK in backends:
					hS = HadoopSink(append = True)
					rating = 1
					hS.save_mode2(userid, itemid, domainid, timestamp)

				us = UserStats('userid', 'itemid')
				us.save(userid,itemid)


		else:
			body_message = {'message' : message,
							'api' : api,
							'backends' : backends }


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



