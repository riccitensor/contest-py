'''
Created on 04.11.2011

@author: christian.winkelmann@plista.com
'''
class scrapy_base(object):
    '''
        crawling class for crawling websites and return the full/main text if it does exist

        @author: cw@plista.com
    '''


    def __init__(self):
        """set up"""
    
    
    
    
if __name__ == '__main__':
    """
    ksta_crawler = scrapy_base()
    test_url = "http://ksta.de/html/artikel/1318243866302.shtml"
    ksta_text = ksta_crawler.getContentsByUrl(test_url)
    print ksta_text + "\n"
    
    test_url = "http://ksta.de/html/artikel/1319813681424.shtml"    
    ksta_text = ksta_crawler.getContentsByUrl(test_url)
    print ksta_text + "\n"
    
    print "the difference of text length\n"
    print str(len(ksta_text))
    """
    