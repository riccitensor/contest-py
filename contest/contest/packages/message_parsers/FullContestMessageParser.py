"""
Created on 17.01.2012

This parser suits the task to fully interpret and flatten the json message we get

@author: christian.winkelmann@plista.com
@todo: refactor this into sepearte models
"""

import json
from contest.controller.constants import *

class FullContestMessageParser(object):
    '''
    given the json which comes in from the contest this is the parser which analyses the data and puts it acordingly into cassandra
    '''
    flattenedJson = None


    def __init__(self):

        self.object = None
        self.flattenedJson = dict()

        self.config_team_id = None
        self.config_limit = None
        self.context = None
        self.domain_id = None
        self.item_id = None
        self.item_created = None
        self.message_id = None
        self.message_type = None
        self.text = None
        self.title = None
        self.user_id = None
        self.source_id = None
        self.target_id = None
        self.item_recommendable = None



    def parse(self, json_string):
        debug = False

        message = json.loads(json_string)
        self.message = message


        try:
            self.version = float(message[u'version'])
        except:
            if debug:
                print "no version given"

        if self.version == 1.0:
            try:
                self.message_type = str(message[u'msg'])
                self.flattenedJson['msg'] = str(message[u'msg'])

            except:
                if debug:
                    print "no message type given, probably an error"

            try:
                self.flattenedJson['client_id'] = message[u'client'][u'id']
                self.user_id = int(message[u'client'][u'id'])
            except:
                if debug:
                    print "no client id given"

            try:
                self.domain_id = int(message[u'domain'][u'id'])
                self.flattenedJson['domain_id'] = int(message[u'domain'][u'id'])
            except:
                if debug:
                    print "no domain id given"

            try:
                self.context = message[u'context']
            except:
                if debug:
                    print "no context given"

            try: # check for config
                self.config = message[u'config']
            except:
                if debug:
                    print "config not set"

            try:
                self.config
                try:
                    self.config_team_id = self.config[u'team'][u'id']
                    self.flattenedJson['config_team_id'] = self.config[u'team'][u'id']
                except:
                    if debug:
                        print "config_team_id doesn't exist"
            except AttributeError:
                if debug:
                    print "config not set"


                    ############### message type is IMPRESSION #######################
            if self.message_type == MESSAGE_TYPE_IMPRESSION:
                #from Impression
                try:
                    self.message_id = int(message[u'id'])
                    self.flattenedJson['impression_id'] = int(message[u'id'])
                except:
                    if debug:
                        print "no impression id given"

                try:
                    self.item = message[u'item']

                    try:
                        self.item_id = self.item[u'id']
                        self.flattenedJson['item_id'] = self.item[u'id']
                    except:
                        """ item title """
                        if debug:
                            print "no item id given"

                    try:
                        self.item_title = self.item[u'title']
                        self.flattenedJson['item_title'] = self.item[u'title']
                    except:
                        """ item title is not set """
                        if debug:
                            print "no item title given"
                    try:
                        self.item_url = str(self.item[u'url'])
                        self.flattenedJson['item_url'] = str(self.item[u'url'])
                    except:
                        """ item url is not set """
                        if debug:
                            print "no item url given"

                    try:
                        self.item_created = self.item[u'created']
                        self.flattenedJson['item_created'] = self.item[u'created']
                    except:
                        """ item created is not set """
                        if (debug == True):
                            print "no created title given"

                    try:
                        self.item_text = str(self.item[u'text'])

                    except:
                        """ item text is not set """
                        if (debug == True):
                            print "no item text given"

                    try:
                        item_img = self.item[u'img']
                    except:
                        """ item img is not set """
                        if (debug == True):
                            print "no img title given"

                    try:
                        self.item_recommendable = bool(self.item[u'recommendable'])
                        self.flattenedJson['item_recommendable'] = bool(self.item[u'recommendable'])
                    except:
                        """ item recommendable is not set """
                        if debug:
                            print "no item recommendable given"

                except:
                    """ it seems we have to do the recommendation solely user based """
                    if debug:
                        print "no item given"
                        item = False

                if self.config:
                    try:
                        self.config_recommend = self.config[u'recommend']
                        self.flattenedJson['config_recommend'] = self.config[u'recommend']
                    except:
                        if (debug == True):
                            print "no recommend config option set"

                    if (self.config_recommend == False):
                        "this message can be sent to an async analysing job since no answer is expected"

                        try:
                            config_timeout = self.config[u'timeout']
                        except:
                            if (debug == True):
                                print "no config_timeout given"
                    elif self.config_recommend:
                        try:
                            self.config_limit = self.config[u'limit']
                        except:
                            if debug:
                                print "no limit given"



                                ############### message type is feedback #######################
            elif self.message_type == MESSAGE_TYPE_FEEDBACK:
                """ ok, we have a feedback """
                try:
                    self.source_id = int(message[u'source'][u'id'])
                    self.flattenedJson['source_id'] = int(message[u'source'][u'id'])
                except:
                    if debug:
                        print "no source given"

                try:
                    self.target_id = int(message[u'target'][u'id'])
                    self.flattenedJson['target_id'] = int(message[u'target'][u'id'])
                except:
                    if (debug == True):
                        print "no target given"



                        ############### message type is RESULT #######################
            elif ( self.message_type == 'result'):
                """ ok, we have a result set. This set is not part of the ordinary contest data.
                This is a log of what other teams have sent into the contest """
                self.flattenedJson = None



            ############### message type is ERROR #######################
            elif ( self.message_type == 'error'):
                print " ok, we have an error "
                self.flattenedJson = None
                try:
                    source = message[u'source']
                except:
                    if (debug == True):
                        print "no source given"

            else:
                try:
                    error_message = message[u'error']
                    error_code = message[u'code']

                    #self.flattenedJson['msg'] = 'error'
                    self.flattenedJson['error_message'] = 'error_message'
                    self.flattenedJson['error_code'] = 'error_code'

                except:
                    "something is seriously wrong when we can't even parse an error"

                    #print flattenedJsone




        else:
            print "wrong version"
            self.flattenedJson = None

        return self.flattenedJson


    def _parse_impression(self, message):


        return ""


    def _parse_feedback(self, message):

        return ""

    def _parse_result(self, message):

        return ""

    def __parse_error(self, message):

        return ""



if __name__ == '__main__':
    json_string = '{"msg":"impression","id":37098,"client":{"id":0},"domain":{"id":"418"},"item":{"id":"51072561","title":"Ratlo\\u00adsig\\u00adkeit nach dem Kompro\\u00admiss","url":"http:\\/\\/www.ksta.de\\/html\\/artikel\\/1317623400324.shtml","created":1317745309,"text":"Das Land will Frieden, doch in K\\u00f6ln droht neuer Streit. Denn nach dem Schul\\u00adkom\\u00adpro\\u00admiss auf Landes\\u00adebene kann der Plan der Stadt f\\u00fcr ein \\u201el\\u00e4n\\u00adgeres gemein\\u00adsames Lernen\\u201c jeden\\u00adfalls nicht mehr mit den \\u201eGe\\u00admein\\u00adschafts\\u00adschu\\u00adlen\\u201c umge\\u00adsetzt werden.","img":null},"config":{"timeout":null,"recommend":true,"limit":4},"version":"1.0"}'
    parser = FullContestMessageParser()
    retVal = parser.parse(json_string)
    print retVal




