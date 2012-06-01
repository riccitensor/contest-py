'''
Created on 18.05.2012

central station for all incoming messages

@author: christian.winkelmann@plista.com
'''
from contest.packages.models.rawJsonModel import rawJsonModel
from contest.packages.message_parsers.fullParser import FullContestMessageParser


class SaveMessage(object):
	''' dump messages into various formats '''
	rawJson = None
	fullyParsed = None

	def __init__(self, message, async=False, api = 'contest'):
		'''
		  get the message, parse it and then save
		  '''

		if (not async):
			raw = rawJsonModel(message, mode='redis')
			fullParsedDataModel = FullContestMessageParser()

			raw.save();


			fullParsedDataModel.parse(message)
			#fullParsedDataModel.
			self.fullyParsed = fullParsedDataModel.get()

		else:
			""" """
			from contest.packages.queues.RawJsonDumpWorker import rawJsonDumpWorker

			raw = rawJsonDumpWorker(mode='redis')
			raw.enqueue(message)


if __name__ == '__main__':
	""" """
