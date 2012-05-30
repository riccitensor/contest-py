'''
Created on 18.10.2011

@author: karisu
'''
from algorithm.db_model.dbabstraction import dbabstraction
from algorithm.db_model.sql_py import sql_py

class SampleClassification(object):
    '''
    classdocs
    '''
    sample_id = ''
    db = object

    def __init__(self):
        '''
        Constructor
        '''
        
        
    def init_classification_samples(self, sample_id):    
        ''' init sample database '''
        self.sample_id = sample_id
        from algorithm.db_model import dbabstraction
        
        #self.db = dbabstraction('sqlite', sample_id)
         
        
        
    def fill_classification_samples_id_label(self, document_id, label):
        ''' @todo: this is just a dummy 
        fill samples by id and label '''
        print self.sample_id + document_id
        
        
        return 'filling id-label pair ok'
        
    def fill_classification_samples_text_label(self, text, label):
        ''' @todo: this is just a dummy 
        fill samples by text and label '''
        
        


if __name__ == '__main__':
    db_location = '../linguisticModel/'
    sq = SampleClassification()

    db = dbabstraction('sqlite', '5')

    #from algorithm.db_model import sql_py
    sql = sql_py()

    sq.init_classification_samples('5')
    
    sq.fill_classification_samples_id_label('doc_0', 'topic1')
    sq.fill_classification_samples_id_label('doc_1', 'topic1')
    sq.fill_classification_samples_id_label('doc_2', 'topic1')
    
    sq.fill_classification_samples_id_label('doc_3', 'topic2')
    sq.fill_classification_samples_id_label('doc_4', 'topic2')
    sq.fill_classification_samples_id_label('doc_5', 'topic2')
    sq.fill_classification_samples_id_label('doc_6', 'topic2')
    
    
    
    print  '\n'
            