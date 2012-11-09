"""
Created on 21.10.2011
just a draft to generate a test dataset by a gaussian distribution

@author: christian.winkelmann@plista.com
"""
from numpy.matlib import rand
from random import gauss
from algorithm.db_model import dbabstraction

class campaign_vector_training(object):
    
    def __init__(self):
        "create the database connection"
        
        
        
        
    def generate_testdata(self):
        """ lets try to generate plista like campaign data in the form of a dictionary 
        input_vector = 
        { 'browser' : 'firefox',
        'os' : 'linux',
        'publisher' : 'ksta' }
        output_vector = { campaign : 'kia' 
        """
        
        input_vector = { 'browser' : 'firefox', 'os' : 'linux', 'publisher' : 'ksta' }
        
        possible_browsers = [ 'firefox', 'ie', 'opera', 'mobile']
        possible_os = [ 'windows', 'linux', 'iOS' ]
        possible_publishers = ['ksta' , 'spiegel', 'golem', 'heise']
        
        vector_set = [possible_browsers, possible_os, possible_publishers]
        
        random_vector = []
        
        for i in range(5):
            vector = []
            for x in vector_set:
                additive = 0.0
                index = int(round( ( rand(1)+additive ) * ( len(x)-1 ), 0))
                vector.append( x[index] )
            random_vector.append(vector)
            
            print '\n'
                        
        print random_vector
        
                
if __name__ == '__main__':
    tc = campaign_vector_training()
    
    tc.generate_testdata()
        
        
