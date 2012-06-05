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


	def merge_naive(self, factors):
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
					mergedList[value[0]] =+ 1




		print tmp_list
		return mergedList

	def merge_dictionary_naive(self, list_of_dicts, list_of_weights = (0.5, 0.5)):
		worker1 = { 1 : 0.4, 	2 : 0.5 				}
		worker2 = { 			2 : 0.4, 	3 : 0.5 	}

		list_of_dicts = { 	'worker1' : worker1,
					   		'worker2' : worker2 }






		desiredResult = { 1 : 0.4, 2 : 0.45, 3 : 0.5 }





	def merge_plista(self):
		worker1 = { 1 : 0.4, 	2 : 0.5 				}
		worker2 = { 			2 : 0.4, 	3 : 0.5 	}
		worker3 = { 			2 : 0.2, 	3 : 0.5 	}

		# define the merge weights
		weights = {'worker1' : 0.4,
				   'worker2' : 0.5,
				   'worker3' : 0.1
				}

		# creating a dictionary of the results
		resultList = { 'worker1' : worker1,
					   'worker2' : worker2,
					   'worker3' : worker3

			}

		result = {}
		weights = {}









