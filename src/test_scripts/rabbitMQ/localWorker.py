'''
Created on 27.11.2011

@author: karisu
'''

import pika
import time

class localWorker(object):
    '''
    1. stop in the pipeline of 4 steps
    
     
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def main(self):    
        """ main function """

        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()
        
        channel.queue_declare(queue='hello_sent_back')
        
        print ' [*] Waiting for messages. To exit press CTRL+C'
                
        channel.basic_consume(self.callback,
                              queue='hello_sent_back',
                              no_ack=True)
        
        channel.start_consuming()
        
    def callback(self, ch, method, properties, body):
        time.sleep(2.5)
        print " [x] Received %r" % (body)
        
        
if __name__ == '__main__':
    lw = localWorker()
    lw.main()