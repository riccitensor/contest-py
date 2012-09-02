'''
Created on 20.05.2012

@author: christian.winkelmann@plista.com
'''
import unittest
from contest.packages.models.rawJsonModel import rawJsonModel
import time

class TestRawJsonModel(unittest.TestCase):


	def setUp(self):
		pass


	def tearDown(self):
		pass


	def testRawJsonModel_GETN_Cassandra(self):
		message = "{\"msg\":\"impression\",\"id\":2,\"client\":{\"id\":1},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"1234\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
		raw = rawJsonModel(json_string = message)
		raw.save() 
		
		self.assertEqual(len(raw.getN(N=1)), 1, "the result has the wrong length")

		# self.assertNotEqual(len(raw.getN(N=1000)), 1000, "the result has the wrong length")
		for i in xrange(100):		
			raw = rawJsonModel(json_string = message)
			raw.save()
		
		self.assertEqual(len(raw.getN(N=100)), 100, "the result has the wrong length")  

	def _testRawJsonModel_GETN_Redis(self):
		''' @fixme: this is broken '''
		message = "ABC"
		raw = rawJsonModel(json_string = message, mode = 'redis')
		raw.save() 
		
		self.assertEqual(len(raw.getN(N=1)), 1, "the result has the wrong length")

		#self.assertNotEqual(len(raw.getN(N=1000)), 1000, "the result has the wrong length")
		for i in xrange(5):		
			raw = rawJsonModel(json_string = message, mode = 'redis')
			time.sleep(1)
			print raw.save()
		
		print raw.getN(N=5)
		#self.assertEqual(len(raw.getN(N=100)), 100, "the result has the wrong length")  



if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testRawJsonModel']
	unittest.main()