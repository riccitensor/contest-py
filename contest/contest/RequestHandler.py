# -*- coding: utf-8 -*-
'''
Created on 16.11.2011
This web service provides the basic api functions needed for the plista contest 
It will delegate the work to other places


@author: christian.winkelmann@plista.com
'''

from flask import Flask
from flask import request
import logging
from contest.controller.ProcessMessage import ProcessMessage

logging.basicConfig(filename='Request_Handler.log',level=logging.DEBUG)


app = Flask(__name__)


@app.route('/test/hello_world')
def test_hello_world():
    """ just a test function """
    return 'Hello World!\n'



@app.route('/test/http_param_ext', methods=['GET', 'POST'])
def test_http_param_ext():
    if request.method == 'GET':
        text = request.args.get('text', '')
        myid = request.args.get('id', '-1', type=int)
    if request.method == 'POST':
        text = request.form[ 'text' ]
        myid = request.form[ 'id' ]    
    else: return "ERROR" 
    return 'text: ' + text + ' str: ' + str(myid) + '\n'



@app.route('/contest/incoming_message', methods=['POST','GET'])
def incoming_contest_call():
    """
    this accepts the contest messages
    """
    import json
    """
    if request.method == 'POST':

        logging.debug("request.data: " + str(request.data))
        logging.debug("request.form: " + str(request.form))

        if len(request.data):
            return str(request.data)
        else: return str(request.form)
    """

    if request.method == 'POST':
        import urllib
        print "test"
        if len(request.data):
            message = str(request.data)
        else: message = str(request.form)
        print message
        logging.info('incoming before unquote:' + message)
        message = urllib.unquote(message).decode('utf8')
        logging.info('incoming message:' + message)
        logging.info('json decode ===================:' + json.loads(message) )
        #print json.loads(message)

        # processing the message
        pM = ProcessMessage(message)
        result = pM.recommend(message)

        " now we have to save the raw message first, lets use an async worker for it "
        #messageSaver = SaveMessage(message, async = True)
        #df = default_parser()
        #recommendations_message = df.default_parse(message)

        logging.debug('recommendation message:' + str(result))
        if result is None : return "{error : result_is_empty}"
        else: return result



app.debug = True
app.run(host='0.0.0.0', port=5001)
