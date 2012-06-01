'''
Created on 18.05.2012

central station for all incoming messages

@author: christian.winkelmann@plista.com
'''
from contest.packages.models.rawJsonModel import rawJsonModel
from contest.packages.message_parsers.fullParser import FullContestMessageParser
from contest.packages.recommenders.Random_Recommender import Random_Recommender
from contest.packages.queues.QueueBase import QueueBase
class SaveMessage(QueueBase):
	''' dump messages into various formats '''
	rawJson = None
	fullyParsed = None

	def __init__(self, message, async=False, api = 'contest', backends = ()):
		'''
		  get the message, parse it and then save
		  '''




	def save(self, message, async=False, api = 'contest', backends = ()):

		if (not async):

			if api == 'contest':
				fullParsedDataModel = FullContestMessageParser()
				parsedMessage = fullParsedDataModel.parse(message)
				fullParsedDataModel.save()

				raw = rawJsonModel(message, mode='redis')
				raw.save();

			if api == 'orp':
				""" todo """

			elif api == 'id_list': ## this for debuggin purposes
				userid = message['userid']
				itemid = message['itemid']
				timestamp = message['timestamp']
				domainid = message['domainid']

				additional_filter = {'domainid' : domainid}

				fb = Random_Recommender( userid )
				fb.set_recommendables(itemid, additional_filter)





		else:
			""" """
			from contest.packages.queues.RawJsonDumpWorker import rawJsonDumpWorker

			raw = rawJsonDumpWorker(mode='redis')
			raw.enqueue(message)


if __name__ == '__main__':
	""" """
