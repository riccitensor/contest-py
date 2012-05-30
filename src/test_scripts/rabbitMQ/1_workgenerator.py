'''
Created on 27.11.2011

@author: karisu
'''
import pika
import time

class workGenerator(object):
    '''
    this is the equivalent to the team message hanler i.e. the Flask Server 
    it will add work to a queue which will
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
        
        
    def enqueue(self, _body):
        print "create workload"
       
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        channel = connection.channel()
        
        channel.queue_declare(queue='hello')
        
        channel.basic_publish(exchange='',
                              routing_key='hello',
                              body=_body)
        print " [1] " + _body
        connection.close()
        
        
        
if __name__ == '__main__':
    print "send out some work"
    wg = workGenerator()
    for i in xrange(10000):
        wg.enqueue(str(i))
        time.sleep(0.01)
        """ wg.enqueue("keks")
        wg.enqueue("bla")
        
        wg.enqueue("whitehorse")
        wg.enqueue("whitehorse") """
        
    