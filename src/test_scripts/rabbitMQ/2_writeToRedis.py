'''
Created on 27.11.2011

@author: christian.winkelmann@plista.com
'''

import pika
import time

class remoteWorker(object):
    '''
    works sent in tasks remotely. But this doesn't have to be.
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
        
        channel.queue_declare(queue='hello')
        
        print ' [*] Waiting for messages. To exit press CTRL+C'
                
        channel.basic_consume(self.callback,
                              queue='hello',
                              no_ack=True)
        
        channel.start_consuming()
        
    def callback(self, ch, method, properties, body):
        #time.sleep(0.5)
        print " [2] Received %r" % (body) + "and written to redis"
        self.enqueue(body)
        
        
    def enqueue(self, _body):
        print "create workload"
       
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()
        
        channel.queue_declare(queue='hello_redis')
        
        channel.basic_publish(exchange='',
                              routing_key='hello_redis',
                              body=_body)
        #print " [2] Sent 'something else!'"
        connection.close()
        

        
        
if __name__ == '__main__':
    rw = remoteWorker()
    rw.main()