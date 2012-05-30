'''
Created on 30.03.2012

@author: christian.winkelmann@plista.com

This is a test case for hyperdex

hyperdex-coordinator --control-port 6970 --host-port 1234 --logging debug

hyperdex-daemon --host 127.0.0.1 --port 1234 --bind-to 127.0.0.2 --data "/media/NIKON D5000/hyperdex"

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
    #hyperclient.Client.insert()
    c = hyperclient.Client('127.0.0.1', 1234)
    print c
    for i in xrange(10000):
        key = 'jsmith' + str(i)
        phonenumber = 15000 + i
        #c.insert('phonebook', key, {'first': 'John', 'last': 'Smith', 'phone': phonenumber})
    
    
    # print c.lookup('phonebook', 'jsmith4' ) # search by primary key
    
    # get a range of phone numbers
    print [ x for x in c.search('phonebook', {'last' : 'Smith', 'phone' : ( 15000, 15014 ) } ) ]
    
    
    
    
        