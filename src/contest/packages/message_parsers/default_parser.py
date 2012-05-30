'''
Created on 16.11.2011

@author: karisu
'''
#from packages.recommenders import semantic_similarity


from contest.packages.recommenders.fallback_random import fallback_random
from contest.packages.statistics.userStats import UserStats
import pika

import logging
import json

class default_parser(object):
    '''
    standard parser for the contest messages which redirects all tasks to the corresponding functions
    '''
    # just some default values
    team_id = 22
    limit = 4
    fp = fallback_random()
    #ss = semantic_similarity.semantic_similarity()


    def __init__(self):
        '''
        Constructor
        '''
        logging.debug('default parser' )
        
    def impression_parser(self, message):
        """@param message: the message already as a dictionary
        """
        # we got an impression message
        id = message[u'id']
        user_id = message[u'client'][u'id']
    
        if ( u'item' in message): item = message[u'item'] 
        else: item = False
        
        if (( u'config' in message) ):
            if ( u'team' in message[u'config'] ):
                if ( u'limit' in message[u'config'] ):
                    self.limit = message[u'config'][u'limit']
                if ( u'team' in message[u'config'] ):
                    self.team_id = message[u'config'][u'team'][u'id']                  
            
        
        version =  message[u'version']
        
        if ( item != False ):
             if ( (u'recommendable' in item ) and bool(item[u'recommendable']) == True ):
                logging.debug("default parser: ask for a recommendation")
                """ this item can be recommended later and therefore should added to an index """
                text = item[u'text']
                item_id = item[u'id']
                
                """  save the statistics, this is very important because it will prevent showing the same items again and again 
                """
                us = UserStats(user_id, item_id)
                """ save this item as recommendable """
                self.fp.set_recommendables(str(item_id))
                
                text = item[u'text']
                #self.ss.set_recommendables(str(item_id), text )
            
        if ( bool( message[u'config'][u'recommend']) == True):
            """  get recommendation from the fallback random algorithm """
            recs = self.fp.get_recommendation(N=self.limit, userid = user_id)
            
            #recs2 = self.ss.get_recommendation( 5, item_id )
            
            """ generate a dictionary with our recommendations """
            recommendations = list( {"id": x} for x in recs)
            return_val = {
            "msg":"result",
            "items": recommendations,
            "team":{
                "id":self.team_id
            },
            "version":version
            }
            
            
            
            return json.dumps( return_val )
        else: 
            logging.debug("default parser: DO NOT ask for a recommendation")
            return None
        
    
    
    def feedback_parser(self, message):
        pass
        
        
    def default_parse(self, message):
        """
        @param string message a json encoded dictionary
        @todo: implement this function
        """
        
    def enqueue(self, message):
        print "create workload"
       
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()
        
        channel.queue_declare(queue='hello')
        
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=message)
        print " [1] " + message
        connection.close()
        
        #message = json.dumps(message)
        message = json.loads(message)  
               
        type = message[u'msg']
        if type=='impression':
            return self.impression_parser(message)
                    
            
        elif type=='feedback':
            # we got a feedback message
            return self.feedback_parser(message)
            logging.debug("got a feedback" + str(message))
            return None
            
        elif type=='result':
            logging.debug("got a result" + str(message))
            return None
            #we have result
            
        elif ( len(message[u'error']) > 0 ):
            # we have found an error 
            logging.warning("an error happened" + str(message))
            return None
            
        
        #ret_message = "{\"msg\": \"result\", \"items\": [\"46327129\", \"56043896\", \"49327097\", \"50450029\"], \"version\": \"1.0\", \"team\": {\"id\": \"22\"} "
         
        #ret_test = "{\"msg\":\"result\",\"items\":[{\"id\":\"46327129\"}, {\"id\":\"1234\"}],\"team\":{\"id\":22},\"version\":\"1.0\"}" 
         
        


if __name__ == '__main__':
    df = default_parser()
    message = {
        "msg": "impression",
        "id": '1234',
        "client":{
            "id": 111
        },
        "domain":{
            "id": 222
        },
        "item":{
            "id":77772,
            "title":'wow, das ist ein titel',
            "url":'www.ksta.da/artikel',
            "created":'34:34',
            "text":'artikeltext und noch mehr text',
            "img":'url',
            "recommendable":'false'
        },
        "context":{
            "category":{
                "id":123
            }
        },
        "config":{
            "team":{
                "id":234
            },
            "timeout":'4.321',
            "recommend":'false',
            "limit":4
        },
        "version":'1.0'
        }
         
    # this is a message as it comes from the server      
    #message = "{\"msg\":\"impression\",\"id\":940291,\"client\":{\"id\":99291445},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"56302351\",\"title\":\"Die 198. Ausgabe von \\\\u201eWetten, dass\\\\u2026?\\\\u201c\",\"url\":\"http:\\\\/\\\\/www.ksta.de\\\\/html\\\\/fotolines\\\\/1320495972678\\\\/rahmen.shtml?1\",\"created\":1320941226,\"text\":\"Zum vorletzten Mal mode\\\\u00adriert Thomas Gott\\\\u00adschalk die Sendung. (Bild: dapd)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1},\"version\":\"1.0\"}"
    #message = ([('{"msg":"impression","id":1157847,"client":{"id":606501885},"domain":{"id":"418"},"item":{"id":"57884510","title":"Guin\\u00adness World Records Tag","url":"http:\\/\\/www.ksta.de\\/html\\/fotolines\\/1321373161454\\/rahmen.shtml?1","created":1321527880,"text":"Zum Guin\\u00adness World Records Tag an diesem Donnerstag werden wieder neue Welt\\u00adre\\u00adkorde in unge\\u00adw\\u00f6hn\\u00adli\\u00adchen Diszi\\u00adplinen verzeichnet. Am 30. Oktober 2011 haben 14 345 Chinesen ein Bad in den hei\\u00dfen Quellen Chong\\u00adqings im S\\u00fcd\\u00adwesten Chinas genommen, um den.","img":null,"recommendable":true},"config":{"timeout":null,"recommend":true,"limit":4,"team":{"id":"15"}},"version":"1.0"}', u'')])
    #print str(df.default_parse(message))
    #test case do not recommend
    #message =  "{\"msg\":\"impression\",\"id\":1299911,\"client\":{\"id\":0},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"58572466\",\"title\":\"Rhein mit nied\u00adrigem Pegel\u00adstand\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273954\/rahmen.shtml?1\",\"created\":1321985498,\"text\":\"(Bild: Ralf Johenen)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":false,\"limit\":1},\"version\":\"1.0\"}"
    #print str(df.default_parse(message))
    #test case: recomend only one item
    message = "{\"msg\":\"impression\",\"id\":1300277,\"client\":{\"id\":565639045},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"58509770\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":1,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
    print str(df.default_parse(message))
    
    message = "{\"msg\":\"impression\",\"id\":1300277,\"client\":{\"id\":565639045},\"domain\":{\"id\":\"418\"},\"item\":{\"id\":\"58509770\",\"title\":\"Inter\u00adna\u00adtional Emmy-Awards\",\"url\":\"http:\/\/www.ksta.de\/html\/fotolines\/1321650273296\/rahmen.shtml?1\",\"created\":1321957664,\"text\":\"Talkshow-Mode\u00adra\u00adtorin Wendy Williams bei den 39. inter\u00adna\u00adtio\u00adnalen Emmy-Awards. (Bild: AFP)\",\"img\":null,\"recommendable\":true},\"config\":{\"timeout\":null,\"recommend\":true,\"limit\":4,\"team\":{\"id\":\"22\"}},\"version\":\"1.0\"}"
    print str(df.default_parse(message))
    # for testing we create a json string     
    import json     
    #print str(message)
    
    #message = json.dumps(message)
    #message = json.loads(message)
    
    #print message['domain']
    
    
    
    
    
   