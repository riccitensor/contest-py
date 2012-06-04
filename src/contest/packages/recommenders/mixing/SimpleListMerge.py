'''
Created on 04.05.2012

Simple Method of Merging at Least two ResultSet Lists

@author: christian.winkelmann@plista.com
'''


class SimpleListMerge(object):

	''' temporary testing variables '''



	def __init__(self):
		''' '''
		self.recList_stash = {}

	def recomend(self):
		random_recommender = fallback_random()
		list1 = random_recommender.getRecommendation()

		if ( len(list1) < 5 ):
			random_recommender.train()


	def add(self, id, recList):
		self.recList_stash[id] = recList


	def merge(self, factors):
		''' merge the list we added
		'''
		if len(factors) != len(self.recList_stash):
			# TODO throw a good exception
			return -1


		print "-----------------------------"
		tmp_list = self.recList_stash
		tmp_list_2 = {}
		print tmp_list

		mergedList = {}

		factorSum = 0
		for key, factor in factors.items():
			factorSum =+ factor
			tmp_list_2[key] = []
			for value in tmp_list[key]:
				#print value[0]
				tmp_list_2[key].append( (value[0],factor*value[1] ) )
				if value[0] not in mergedList:
					mergedList[value[0]] = 0
				else:
					mergedList[value[0]] =+




		print tmp_list
		return mergedList







