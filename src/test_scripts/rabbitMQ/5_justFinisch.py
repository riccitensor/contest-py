'''
Created on 27.11.2011

@author: karisu
'''

import pika
import time

class remoteWorker(object):
    '''
    now get data from redis and index that 
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
        
        channel.queue_declare(queue='write_back')
        
        print ' [*] Waiting for messages. To exit press CTRL+C'
                
        channel.basic_consume(self.callback,
                              queue='write_back',
                              no_ack=True)
        
        channel.start_consuming()
        
    def callback(self, ch, method, properties, body):
        #time.sleep(0.5)
        print " [5] received %r" % (body)
        print "finally I am done"
        

        
        
if __name__ == '__main__':
    rw = remoteWorker()
    rw.main()