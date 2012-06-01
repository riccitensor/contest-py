'''
Created on 20.11.2011

basic api functionality

@author: christian.winkelmann@plista.com
'''
import httplib, urllib, json

class api_controll(object):
    """
    """
    api_key = "d83a49fae923b0966e78fa552c109abf"
    contest_server = "contest.plista.com/api/api.php"
    api_address = "/api/api.php" 
    def __init__(self):
        """
        """
        
    def start_receiving_impressions(self):     
        """{
            "msg":"start",
            "apikey":< api_key:string >,
            "version":< version_string:string >
           }
        """
        message = {
            "msg":"start",
            "apikey":self.api_key,
            "version": '1.0'
           } 
        message = json.dumps(message)
        #params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
        #params = urllib.urlencode({message: 'bla'})
        params = message
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        #conn = httplib.HTTPConnection( self.contest_server )
        conn = httplib.HTTPConnection("contest.plista.com")
        conn.request("POST", "/api/api.php", params, headers)
        response = conn.getresponse()
        print response.status, response.reason

        data = response.read()
        print data
        # 'Redirecting to <a href="http://bugs.python.org/issue12524">http://bugs.python.org/issue12524</a>'
        conn.close()
    
    def test_function(self):     
        """{
            "msg":"start",
            "apikey":< api_key:string >,
            "version":< version_string:string >
           }
        """
        
        params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection("bugs.python.org")
        conn.request("POST", "", params, headers)
        response = conn.getresponse()
        print response.status, response.reason

        data = response.read()
        print data
        # 'Redirecting to <a href="http://bugs.python.org/issue12524">http://bugs.python.org/issue12524</a>'
        conn.close()


    
    def stop_receiving_impressions(self):    
        """
        """

        message = {
            "msg":"stop",
            "apikey":self.api_key,
            "version": '1.0'
           } 
        message = json.dumps(message)
        #params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
        #params = urllib.urlencode({message: 'bla'})
        params = message
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        #conn = httplib.HTTPConnection( self.contest_server )
        conn = httplib.HTTPConnection("contest.plista.com")
        conn.request("POST", "/api/api.php", params, headers)
        response = conn.getresponse()
        print response.status, response.reason

        data = response.read()
        print data
        # 'Redirecting to <a href="http://bugs.python.org/issue12524">http://bugs.python.org/issue12524</a>'
        conn.close()
        
    def start_sync(self):
        """
        """
            
    def trigger_message(self):
        """
        """        

if __name__ == '__main__':
    api = api_controll()
    api.start_receiving_impressions()
    
    
    
    