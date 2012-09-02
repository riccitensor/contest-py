## -*- coding: utf-8 -*-
#'''
#Created on 16.11.2011
#This web service provides the basic api functions needed for the plista contest 
#It will delegate the work to other places
#
#
#@author: cw@plista.com
#'''
#
#from flask import Flask
#from flask import request
#
#from packages.message_parsers.default_parser import default_parser
#
#
#import logging
#from packages.rabbitMQ.algorithm.storage.rawJsonDump import rawJsonDump
#logging.basicConfig(filename='output.log',level=logging.DEBUG)
#
#
#app = Flask(__name__)
#"""
#@app.route('/test/crawl/url')
#def test_crawl_url():
#    if request.method == 'GET':
#        url = request.args.get('url', '1', type=str)
#        text = request.args.get('introtext', None, type=str)
#    
#    l = LoadContentFromUrl()
#    
#    if text == None:
#    	return l.getContentsByUrl(url)
#    else:
#		return l.getContentsByUrlWithIntroText(url, text)
#"""
#
#@app.route('/test/hello_world')
#def test_hello_world():
#    """ just a test function """
#    return 'Hello World!\n'
#
#"""
#@app.route('/test/http_param_simple', methods=['GET', 'POST'])
#def test_http_param_simple():
#    if request.method == 'POST':
#        return 'POST'
#    if request.method == 'GET':
#        return 'GET'
#"""
#"""    
#@app.route('/test/http_param_ext', methods=['GET', 'POST'])
#def test_http_param_ext():
#    if request.method == 'GET':
#        text = request.args.get('text', '')
#        myid = request.args.get('id', '-1', type=int)
#    if request.method == 'POST':
#        text = request.form[ 'text' ]
#        myid = request.form[ 'id' ]    
#    else: return "ERROR" 
#    return 'text: ' + text + ' str: ' + str(myid) + '\n'
#"""
#"""
#@app.route('/statistics/ObjectByObject', methods=['GET', 'POST'])
#def test_http_param_ext():
#    if request.method == 'GET':
#        text = request.args.get('text', '')
#        myid = request.args.get('id', '-1', type=int)
#    if request.method == 'POST':
#        text = request.form[ 'text' ]
#        myid = request.form[ 'id' ]    
#    else: return "ERROR" 
#    return 'text: ' + text + ' str: ' + str(myid) + '\n'
#"""
#
#@app.route('/contest/incoming_message', methods=['POST','GET'])
#def incoming_contest_call():
#    """
#    this accepts the contest messages
#    """
#
#    
#    if request.method == 'GET':
#        return "GET"
#    if request.method == 'POST':
#        
#        import json
#        import urllib
#       
#        logging.debug('"POST message\n "')
#       
#        message = request.data
#        #message = request.form
#        #return "the message sent to the server is: " + str(message)
#        #print message
#        
#        if ( len(message) < 5 ): # since the contest sync message is sent differently then the live messages we need to check both ways 
#           message = request.form
#       
#                    
#        #print message     
#        message = urllib.unquote(message).decode('utf8')
#        logging.debug('Flask Server server message (1):' + str(message))
#
#        " now we have to save the raw message first, lets use a  async worker for it "
#        
#        raw = rawJsonDump()
#        enq_msg = raw.enqueue(message)
#        #logging.debug('the enqueuing was successful: ' + str( enq_msg ))
#       
#              
#        df = default_parser()
#
#        recommendations_message = df.default_parse(message)
#
#        logging.debug('recommendation message:' + str(recommendations_message))
#        if ( recommendations_message == None ): return ""
#        else: return recommendations_message
#        
#        return 'OK' #str(message)
#
#app.debug = True
#app.run(host='0.0.0.0', port=5001)
