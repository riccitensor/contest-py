"""
Created on 17.01.2012

This parser suits the task to fully interpret and flatten the json message we get

@author: christian.winkelmann@plista.com
@todo: refactor this into sepearte models
"""

import json
from contest.controller.constants import *
import logging

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

        self.logger = logging.getLogger("message_parser:")

    def __str__(self):
        # TODO FINISH This
        val = {"config_team_id" : self.config_team_id,
               "config_limit": self.config_limit }
        return json.dumps(val)

    def parse(self, json_string):
        message = json.loads(json_string)
        self.message = message


        try:
            self.version = float(message[u'version'])
        except:
            self.logger.warning("version not passed")

        if self.version == 1.0:
            try:
                self.message_type = str(message[u'msg'])
            except:
                self.logger.warning("no message type given, probably an error")


            try:
                self.user_id = int(message[u'client'][u'id'])
            except:
                self.logger.warning("no client id given")

            try:
                self.domain_id = int(message[u'domain'][u'id'])
            except:
                self.logger.warning("no domain id given")

            try:
                self.context = message[u'context']
            except:
                self.logger.warning("no context given")

            try: # check for config
                self.config = message[u'config']
            except:
                self.logger.warning("config not set")

            try:
                self.config
                try:
                    self.config_team_id = self.config[u'team'][u'id']
                except:
                    self.logger.warning("team_id doesn't exist")
            except AttributeError:
                self.logger.warning("config not set")


                    ############### message type is IMPRESSION #######################
            if self.message_type == MESSAGE_TYPE_IMPRESSION:

                try:
                    self.message_id = int(message[u'id'])
                except:
                    self.logger.warning("no impression id given")

                try:
                    self.item = message[u'item']

                    try:
                        self.item_id = self.item[u'id']
                    except:
                        """ item title """
                        self.logger.warning("no item id given")

                    try:
                        self.item_title = self.item[u'title']
                    except:
                        """ item title is not set """
                        self.logger.warning("no item title given")
                    try:
                        self.item_url = str(self.item[u'url'])
                    except:
                        """ item url is not set """
                        self.logger.warning("no item url given")

                    try:
                        self.item_created = self.item[u'created']
                    except:
                        """ item created is not set """
                        self.logger.warning("no created title given")

                    try:
                        self.item_text = str(self.item[u'text'])

                    except:
                        """ item text is not set """
                        self.logger.warning("no item text given")

                    try:
                        item_img = self.item[u'img']
                    except:
                        """ item img is not set """
                        self.logger.warning("no img title given")

                    try:
                        self.item_recommendable = bool(self.item[u'recommendable'])
                    except:
                        """ item recommendable is not set """
                        self.logger.warning("no item recommendable given")

                except:
                    """ it seems we have to do the recommendation solely user based """
                    self.logger.warning("no item given")

                if self.config:
                    try:
                        self.config_recommend = self.config[u'recommend']
                    except:
                        self.logger.warning("no recommend config option set")

                    if self.config_recommend:
                        try:
                            self.config_limit = self.config[u'limit']
                        except:
                            self.logger.warning("no limit given")



                                ############### message type is feedback #######################
            elif self.message_type == MESSAGE_TYPE_FEEDBACK:
                """ ok, we have a feedback """
                try:
                    self.source_id = int(message[u'source'][u'id'])
                except:
                    self.logger.warning("no source given")

                try:
                    self.target_id = int(message[u'target'][u'id'])
                except:
                    self.logger.warning("no target given")



                        ############### message type is RESULT #######################
            elif ( self.message_type == 'result'):
                """ ok, we have a result set. This set is not part of the ordinary contest data.
                This is a log of what other teams have sent into the contest """
                self.logger.critical("not implemented yet")



            ############### message type is ERROR #######################
            elif self.message_type == 'error':
                self.logging.info("we have an error")
                try:
                    source = message[u'source']
                except:
                    self.logger.warning("no source given")

            else:
                try:
                    self.error_message = message[u'error']
                    self.error_code = message[u'code']

                except:
                    self.logger.warning("error codes not present")




        else:
            self.logger.critical("wrong version given")


    def _parse_impression(self, message):


        return ""


    def _parse_feedback(self, message):

        return ""

    def _parse_result(self, message):

        return ""

    def __parse_error(self, message):

        return ""



if __name__ == '__main__':
    logging.basicConfig(filename='plista-contest.log',level=logging.DEBUG)
    json_string = '{"msg":"impression","id":37098,"client":{"id":0},"domain":{"id":"418"},"item":{"id":"51072561","title":"Ratlo\\u00adsig\\u00adkeit nach dem Kompro\\u00admiss","url":"http:\\/\\/www.ksta.de\\/html\\/artikel\\/1317623400324.shtml","created":1317745309,"text":"Das Land will Frieden, doch in K\\u00f6ln droht neuer Streit. Denn nach dem Schul\\u00adkom\\u00adpro\\u00admiss auf Landes\\u00adebene kann der Plan der Stadt f\\u00fcr ein \\u201el\\u00e4n\\u00adgeres gemein\\u00adsames Lernen\\u201c jeden\\u00adfalls nicht mehr mit den \\u201eGe\\u00admein\\u00adschafts\\u00adschu\\u00adlen\\u201c umge\\u00adsetzt werden.","img":null},"config":{"timeout":null,"recommend":true,"limit":4},"version":"1.0"}'
    parser = FullContestMessageParser()
    retVal = parser.parse(json_string)

    print parser





