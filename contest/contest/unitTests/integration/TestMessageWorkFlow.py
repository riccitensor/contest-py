import unittest
import _mysql
from contest.controller import http_connector

__author__ = 'karisu'


class histogramTest(unittest.TestCase):

	debug = True


	def setUp(self):
		pass


	def tearDown(self):
		pass

	def connectMySQL(self):
		self.mysql_host = config_local.mysql_host
		self.user = config_local.mysql_user
		self.password = config_local.mysql_password
		self.db=_mysql.connect(host=mysql_host,user=user,
							   passwd=password,db="db_youfilter")


	def mockMysqlResults(self, LIMIT = 10):
		# ( id, sth., sth. , json )
		message1 = "{\"msg\":\"impression\",\"id\":1300277,\"client\":{\"id\":1},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"123\",\"title\":\"TEXT1\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
		message2 = "{\"msg\":\"impression\",\"id\":1300277,\"client\":{\"id\":2},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"456\",\"title\":\"TEXT2\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
		message3 = "{\"msg\":\"impression\",\"id\":1300277,\"client\":{\"id\":3},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"789\",\"title\":\"TEXT3\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"


		return (
			(1, "metadata1", "metadata2", message1),
			(2, "metadata1", "metadata2", message2),
			(3, "metadata1", "metadata2", message3),
		)

	def getResults(self):
		# todo fix the way of getting the testing data
		'''
		'''
		if self.debug:
			return self.mockMysqlResults(start_id = 0, end_id = None, limit = None, type = 'impression')
		else :
			self.db.query("""SELECT id, type, timestamp, json, response_time, response_id FROM contest.contest_messages c \
				WHERE ( type = 'impression' ) AND LIMIT 10000 """)
			r=db.use_result()
		result = r

	def test_train_recommender_with_impressions_only(self):


		if not self.debug:
			self.getResults()
			n_maxrows = 10 #amount of items fetched for training
			result = r.fetch_row(maxrows = n_maxrows) # fetch N row maximum
		else:
			result = self.mockMysqlResults()


		while (result):
			for result_item in result:
				'''
				the_id = result_item[0]
				userid = int(result_item[0])
				itemid = int(result_item[1])
				timestamp = str(result_item[2])
				domainid = 	int(result_item[3])
				'''
				json_string = result_item[3]


				http_conn = http_connector('localhost:5001')
				http_conn.send('/contest/incoming_message', json_string)


		# todo sleep for a short while

		# todo get a recommendation now