from pylab import *
import math
import random


'''
Created on 02.12.2011

@author: christian.winkelmann@plista.com
'''



class Plot_Helper(object):

	def __init__( self ):
		''' '''


	def make_plot(self, list):
		t = []
		s = []
		for k,l in list:
			t.append(k)
			s.append(l)

		plot(s, t, linewidth=1.0)

		xlabel('time (s)')
		ylabel('voltage (mV)')
		title('About as simple as it gets, folks')
		grid(True)
		show()


	def make_plot_2(self, list):

		t = []
		s = []
		for k,l in list:
			t.append(k)
			s.append(l)
		area = 5 # 0 to 10 point radiuses
		scatter(s,t,s=area, marker='^', c='r')

		show()





the_list = [('1', 3.0), ('2', 2.0), ('4', 1.0)]
