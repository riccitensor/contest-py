'''
Created on 18.05.2012

central station for all incoming messages

@author: christian.winkelmann@plista.com
'''
from contest.packages.models.rawJsonModel import rawJsonModel
from contest.packages.message_parsers.fullParser import FullContestMessageParser
from contest.packages.queues.RawJsonDumpWorker import rawJsonDumpWorker


class SaveMessage(object):
	''' dump messages into various formats '''
	rawJson = None
	fullyParsed = None

	def __init__(self,message, async = False):
		'''
        get the message, parse it and then save
        '''
		
		if (not async):
			raw = rawJsonModel(message)
			fullParsedDataModel = FullContestMessageParser()
			

			raw.writeback(); 
			self.rawJson = raw.get()
			
			
			fullParsedDataModel.parse( message )
			fullParsedDataModel.writeback()
			self.fullyParse = fullParsedDataModel.get()  
			
		else:
			raw = rawJsonDumpWorker(mode ='redis')
			raw.enqueue(message)
			# fullParsedDataModel.enqueue(message)
			


if __name__ == '__main__':
	
	message = "{\"msg\":\"impression\",\"id\":2,\"client\":{\"id\":1},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"1234\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
	SaveMessage(message, async = True)
	
	message = "{\"msg\":\"impression\",\"id\":3,\"client\":{\"id\":2},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"5678\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
	SaveMessage(message, async = True)
	
	message = "{\"msg\":\"impression\",\"id\":4,\"client\":{\"id\":3},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"9012\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
	SaveMessage(message, async = True)
	
	message = "{\"msg\":\"impression\",\"id\":5,\"client\":{\"id\":4},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"3456\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
	SaveMessage(message, async = True)
