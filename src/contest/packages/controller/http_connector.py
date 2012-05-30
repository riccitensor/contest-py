'''
Created on 26.11.2011

@author: karisu
'''
import httplib, urllib

class http_connector(object):
    
    connection = None
    baseurl = None
    headers = None
    
    def __init__(self, baseurl):
        """ 
        @param baseurl: the url and port to the server, like localhost:5002 
        """ 
        self.baseurl = baseurl
        self.headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    def  fetch(self, dictionary, url_endpoint):
            """
            generate POST requests
            @param a dictionary with the parameters which should be sent to the server
            @param url_endpoint: the url endpoint to send the data to: like /test/hello_world 
            """
            
            # params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
            params = urllib.urlencode(dictionary)
            
            
            self.connection = httplib.HTTPConnection( self.baseurl )
            self.connection.request("POST", url_endpoint, params, self.headers)
            response = self.connection.getresponse()
            #print response.status, response.reason
    
            data = response.read()
            # print data
    
            self.connection.close()
            
            return data
    
    def send(self, url_endpoint, params):
        self.headers = {"Content-type": "application/json", "Accept": "text/plain"}
        self.connection = httplib.HTTPConnection( self.baseurl )
        self.connection.request("POST", url_endpoint, params, self.headers)
        response = self.connection.getresponse()
        print response.status, response.reason
    
        data = response.read()
        #print data
    
        self.connection.close()
            
        #return data
    
        