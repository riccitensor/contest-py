__author__ = 'karisu'
import json

class Message(object):
    def __init__(self, message):
        """ constuctor """
        debug = False


        message = json.loads(str(message))
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
                if debug == True:
                    print "no domain id given"

            try:
                self.context = message[u'context']
            except:
                if (debug == True):
                    print "no context given"

            try: # check for config
                self.config = message[u'config']
            except:
                if (debug == True):
                    print "config not set"

            try:
                self.config
                try:
                    self.config_team_id = self.config[u'team'][u'id']
                    self.flattenedJson['config_team_id'] = self.config[u'team'][u'id']
                except:
                    if(debug):
                        print "config_team_id doesn't exist"
            except AttributeError:
                if(debug == True):
                    print "config not set"


    def factory(self, className, *args):
        aClass = getattr(__import__(__name__), className)
        return apply(aClass, args)

if __name__ == '__main__':
    """ main """