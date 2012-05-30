# -*- coding: utf-8 -*-
'''
Created on 08.09.2011

@author: cw@plista.com
@see README.txt for install and run instructions 
@TODO use json for return values instead of this pure text crap

'''
import json


from flask import Flask
from flask import request


from packages.algorithm.gensim_http_api.Training import Training
from packages.algorithm.gensim_http_api.Indexing import Indexing
from packages.algorithm.gensim_http_api.Query import Query 


app = Flask(__name__)


@app.route('/test/hello_world', methods=['GET', 'POST'])
def test_hello_world():
    return json.dumps({ "msg" : 'Hello World!' })


@app.route('/test/http_param_simple', methods=['GET', 'POST'])
def test_http_param_simple():
    if request.method == 'POST':
        return json.dumps({"type" : "POST" })
    if request.method == 'GET':
        return json.dumps({"type" : "GET" })
    
@app.route('/test/http_param_ext', methods=['GET', 'POST'])
def test_http_param_ext():
    if request.method == 'GET':
        text = request.args.get('text', '')
        myid = request.args.get('id', '-1', type=int)
    if request.method == 'POST':
        text = request.form[ 'text' ]
        myid = request.form[ 'id' ]    
    else: return "{ msg: ERROR }"
    
    message = { "msg" : "result", "text" : text }
    return json.dumps(message)

    
@app.route('/test/gensim/available')
def test_gensim_availabe():
    '''
    just test if the instantiation of the objects will work
    '''
    q = Query()
    t = Training()
    
    msg = { "msg" : "ok" }    
    return json.loads(msg)
    
@app.route('/unsupervised/clustering/gensim/initTrainingSet', methods=['GET', 'POST'])
def initGensimTrainingSet():
    '''now the complicated stuff begins
    This is function is supposed to take the initial steps like allocation space for the model etc
    parameters: id=string  
    '''
    if request.method == 'POST':
        id = request.form[ 'training_id' ]  
    if request.method == 'GET':
        id = request.args.get('training_id', '1', type=int)
    
    t = Training(training_id = id, db_location = db_location)
    result = t.init_training_set()
    
    i = Indexing(id, db_location)
    i.init_indexing_set()
         
    """ @todo jsonify the result """     
    return str(result)

@app.route('/unsupervised/clustering/gensim/fillTrainingSet', methods=['GET', 'POST'])
def gensim_train_fillTrainingSet():
        
    if request.method == 'GET':
        document_text = request.args.get('document_text', '0')
        document_id = request.args.get('document_id', '0')
        training_id = request.args.get('training_id', '0')
    if request.method == 'POST':
        document_text = request.form[ 'document_text'] 
        document_id = request.form[ 'document_id']
        training_id = request.form[ 'training_id']
         
         
    t = Training(training_id, db_location)
    t.fill_training_set(document_text, document_id)
    
    msg = { "msg" : 'fill_ok'}
    return json.dumps(msg)

        
@app.route('/unsupervised/clustering/gensim/trainTrainingSet', methods=['GET', 'POST'])
def train_Gensim_TrainingSet():
    '''
    This function is supposed to make it possible to train the classifier with your own 
    documents. I.E. after the clickabilly main server pushed 1000 known documents into this
    then call the startGensimTraining() function. This will train the gensim model
    A Wikipedia training should be possible as well where the training Set is already installed
    parameters: document=<string>,  
    '''
    
    if request.method == 'GET':
        training_id = request.args.get( 'training_id' , '0' )
    if request.method == 'POST':
        training_id = request.form['training_id']
         
    t = Training(training_id, db_location)
    t.commit_training_set()    
    
    msg = {"msg" : "training_ok" }
    return json.dumps( msg )



@app.route('/unsupervised/clustering/gensim/fillIndexingSet', methods=['GET', 'POST'])
def gensim_train_fillIndexingSet():
    '''
    filling the index
    '''
    if request.method == 'POST':
        training_id = request.form['training_id']
        document_text = request.form['document_text']
        document_id = request.form['document_id']
    if request.method == 'GET':
        document_id = request.args.get('document_id', '0')
        training_id = request.args.get('training_id', '0')
        document_text = request.args.get('document_text', '0')
    
     
    q = Indexing(training_id, db_location)
    q.fill_indexing_set(document_text, document_id)
    
    msg = { "msg" : 'fill_ok'}
    return json.dumps(msg)

@app.route('/unsupervised/clustering/gensim/indexSet', methods=['GET', 'POST'])
def Gensim_IndexSet():
    '''
    start the indexing with formally done filled items
    '''
    
    if request.method == 'GET':
        training_id = request.args.get( 'training_id' , '0' )
    if request.method == 'POST':
        training_id = request.form['training_id']
         
    i = Indexing(training_id, db_location)
    i.commit_indexing_set()    
    
    msg = { "msg" : 'indexing_ok'}
    return json.dumps(msg)


@app.route('/unsupervised/clustering/gensim/deleteIndexSet', methods=['POST', 'GET'])
def delete_Gensim_IndexSet():
    '''after Indexing there might be no need to keep the indexed items   
    '''
    
    if request.method == 'GET':
        training_id = request.args.get( 'training_id' , '0' )
    if request.method == 'POST':
        training_id = request.form['training_id']
         
    i = Indexing(training_id, db_location)
    i.delete_set()    
    
    """ @todo jsonify the result """
    return 'deleting index ok\n'


@app.route('/unsupervised/clustering/gensim/deleteTrainingSet', methods=['POST', 'GET'])
def delete_Gensim_TrainingSet():
    '''after Indexing there might be no need to keep the indexed   
    '''
    
    if request.method == 'GET':
        training_id = request.args.get( 'training_id' , '0' )
    if request.method == 'POST':
        training_id = request.form['training_id']
         
    i = Training(training_id, db_location)
    i.delete_set()    
    
    """ @todo: jsonify the result """ 
    return 'deleting training cache ok\n'


@app.route('/unsupervised/clustering/gensim/queryById', methods=['POST', 'GET'])
def query_Gensim_byId():
    '''
    Query functions
    '''
    
    if request.method == 'GET':
        training_id = request.args.get('training_id', '0')
        document_id = request.args.get('document_id', '0')
    if request.method == 'POST':
        training_id = request.form['training_id']
        document_id = request.form['document_id']
    
     
    q = Query(str(training_id), db_location)
    result = q.queryById( str( document_id ) )
    
    return json.dumps( result )
    
"""
@todo: currently unfunctional, fix
@app.route('/unsupervised/clustering/gensim/queryByText')
def query_Gensim_byText():
    '''
    Query functions
    
    '''
    training_id = request.args.get('training_id', '0')
    document_text = request.args.get('document_text', '0')
     
    q = Query(training_id, db_location)
    q.query(document_text)

    return 'ok'
"""
"""
def to_unicode_or_bust( obj, encoding='utf-8'):
    "
    @todo: this seems to be unused, check and delete
    " 
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj
"""


db_location = './models/gensim/'
#db_location = '/tmp/ramdisk/linguisticModel/'

app.debug = True
app.run(host='127.0.0.1', port=5002)        
