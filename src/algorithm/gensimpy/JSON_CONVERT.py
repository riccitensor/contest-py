'''
Created on 12.10.2011

small helper class to convert gensim results into json 

@author: christian.winkelmann@plista.com
'''

import json

class JSON_DATA_SIMILAR( ):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        constuctor
        '''
             
    def castNumpyFloats(self, simList):
        '''
        because the return value of the similarity from gensim is numpy float we need to invest some time 
        for converting it.
        @todo: pythonify the loop with a generator  
        
        '''
        jsonlist = {}
        import numpy
        for item in simList:
            #print type(simList)
            #print type(item)
            #item = list(item)
            
            if isinstance(item[1], numpy.float32):
                #print "yes"
                #item[1] = float(item[1])
                #jsonlist.append(item)
                #jsonlist[float(item[1])] = item[2]
                jsonlist[item[0]] = float( item[1] )
                
                
                
        # jsonlist = jsonlist
        return jsonlist

        

if __name__ == '__main__':
    import json
    # import Query
    from packages.algorithm.gensimpy.Query import Query 
    
    
    
    q = Query(5)
    simList = q.queryById('doc2')
    
    klm = [7 +1j, 4 + 4j]
    #json.dumps(klm,  cls=JSON_DATA)
    
    caster = JSON_DATA_SIMILAR()
    print caster.castNumpyFloats(simList)

    import numpy
    json.dumps(q.queryById('doc2'), )
    
    
    
    
    
        