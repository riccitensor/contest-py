'''
Created on 12.02.2012

@author: christian.winkelmann@plista.com


'''




class HadoopSink():

	path = '/tmp/one_million_test' 
	
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

	hS = HadoopSink()
	hS.save_mode1(1, 2, 1)
	
	
	
	
	