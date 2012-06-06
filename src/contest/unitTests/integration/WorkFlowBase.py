import unittest
import _mysql
from contest.config import config_local
from contest.packages.controller.http_connector import http_connector

__author__ = 'karisu'


class WorkFlowBase():

	debug = True


	def setUp(self):
		self.connectMySQL()


	def tearDown(self):
		# todo disconnect from db
		pass

	def connectMySQL(self):
		mysql_host = config_local.mysql_host
		user = config_local.mysql_user
		password = config_local.mysql_password
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
