'''
Created on 27.11.2011

@author: christian.winkelmann@plista.com
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
        
        channel.queue_declare(queue='hello_redis')
        
        print ' [*] Waiting for messages. To exit press CTRL+C'
                
        channel.basic_consume(self.callback,
                              queue='hello_redis',
                              no_ack=True)
        
        channel.start_consuming()
        
    def callback(self, ch, method, properties, body):
        #time.sleep(0.5)
        print " [3] received %r" % (body)
        self.enqueue( body )
        
        
    def enqueue(self, _body):
        print "create workload"
       
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()
        
        channel.queue_declare(queue='send_back')
        
        channel.basic_publish(exchange='',
                              routing_key='send_back',
                              body=_body)
        connection.close()
        

        
        
if __name__ == '__main__':
    rw = remoteWorker()
    rw.main()