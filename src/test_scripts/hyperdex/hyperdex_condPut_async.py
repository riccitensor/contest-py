'''
Created on 30.03.2012

@author: christian.winkelmann@plista.com

This is a test case for hyperdex

hyperdex-coordinator --control-port 6970 --host-port 1234 --logging debug

hyperdex-daemon --host 127.0.0.1 --port 1234 --bind-to 127.0.0.2 --data "/media/NIKON D5000/hyperdex"
for advanced tests
hyperdex-daemon --host 127.0.0.1 --port 1234 --bind-to 127.0.0.2 --data "/media/NIKON D5000/hyperdex2"
hyperdex-daemon --host 127.0.0.1 --port 1234 --bind-to 127.0.0.2 --data "/media/NIKON D5000/hyperdex3"

hyperdex-coordinator-control --host 127.0.0.1 --port 6970 add-space << EOF
space phonebook
dimensions username, first, last, phone (uint64)
key username auto 1 3
subspace first, last, phone auto 2 3
EOF

'''

class Hyperdex_Test(object):

    def __init__(self,params):
        '''
        Constructor
        '''
        
        
        
if __name__ == '__main__':
    """
    """
    import hyperclient
    import time
    #hyperclient.Client.insert()
    c = hyperclient.Client('127.0.0.1', 1234)
    print c
    N = 10000
    
    for i in xrange(N):
        key = 'jsmith' + str(i)
        phonenumber = 15000 + i
        #c.insert('phonebook', key, {'first': 'John', 'last': 'Smith', 'phone': phonenumber})
        d = c.async_remove('phonebook', key)
        #d = None
        print d.wait()
        
    print "delete done"
    
    t = time.time()
    d = c.async_insert('phonebook', 'bla', {'first': 'John', 'last': 'Smith', 'phone': 1})
    for i in xrange(N):
        key = 'jsmithb' + str(i)
        phonenumber = 15000 + i
        #c.insert('phonebook', key, {'first': 'John', 'last': 'Smith', 'phone': phonenumber})
        d = c.async_insert('phonebook', key, {'first': 'John', 'last': 'Smith', 'phone': phonenumber})
        #d = None
        #d.wait()
    
    d.wait()
    t = time.time() - t
    print "time diff: " + str(t)
    
    if (True):
        #do_work()
        #print d
        #print d.wait()
        d2 = c.async_lookup('phonebook', 'jsmithb1')
        print "d.wait()"
        print d2
        #time.sleep(2)
        print d2.wait()
        # print c.lookup('phonebook', 'jsmith4' ) # search by primary key
        
        
    
    
        