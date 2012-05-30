import urllib2
import json
import re
import time
from BeautifulSoup import BeautifulSoup
"""@todo
it is buggy: if you use 100 as a threshold then you won't get the full text.
downsizing to 70 won't result in much bigger resultset but it will add the textblock
'nun auch eine kleine Regenbogenfahne wehen' a second time
"""


class LoadContentFromUrl(object):
    '''
        crawling class for crawling websites and return the full/main text if it does exist

        @author: de@plista.com
    '''


    def __init__(self):
        '''
        constructor
        '''

    def getContentsByUrl(self, url):
        """ main crawler function

        """

        #fetch html
        c = urllib2.urlopen(url)
        soup = BeautifulSoup(c.read())

        # get fullText in html
        contentFinder = soup("div", { "class" : "ArtikelText" })
        contentString = ''
        for item in contentFinder[0].contents:
            if item.string and len(item) > 40:
                contentString += item.string

        # get timestamp from html
        dateString = ""
        dateSoup	 = soup.find("p", { "class" : "ArtikelAutor" })
        if dateSoup:
            m = re.match(".*?(?P<DAY>[0-9]{2}).(?P<MONTH>[0-9]{2}).(?P<YEAR>[0-9]{2}),&nbsp;(?P<HOUR>[0-9]{2}):(?P<MIN>[0-9]{2})h.*?", dateSoup.string)
            if not m is None:
                day		 = int(m.group('DAY'))
                month	 = int(m.group('MONTH'))
                year		 = int(m.group('YEAR'))
                hour		 = int(m.group('HOUR'))
                min		 = int(m.group('MIN'))
                dateString = str(int(time.mktime((year, month, day, hour, min, 0, 0, 0, 0))))

        # find title in html
        titleString = ""
        titleSoup = soup.find("h1", { "class" : "ArtikelTitel" })
        if titleSoup:
            titleString = titleSoup.string

        return json.dumps({ "title" : titleString , "dateCreated" : dateString, "content" : contentString })


    def getContentsByUrlWithIntroText(self, url, text):
        """ main crawler function
            originally copied from de's codes by vh. but not nothing has happened in a while. 
            Currently cw's version.
            
            Some approaches will be followed:
            * 1. in the full text search for the snipped and then extend outwards

        """

        #fetch html
        c = urllib2.urlopen(url)
        full_html = c.read()
        soup = BeautifulSoup( full_html )
        soup_string = soup.string
        soup_string = soup.text
        
        m = re.search('(?<=script )\*', full_html)
        
        
        print m.group(0)


        # get fullText in html
        contentString = ""
        for p in soup('p'):
            if p.string and len(p.string) > 60:
                contentString += p.string
        #for p in soup('div'):
        #    if p.string and len(p.string) > 40:
        #        contentString += p.string


                


        # get timestamp from html
        dateString = ""
        dateSoup	 = soup.find("p", { "class" : "ArtikelAutor" })
        if dateSoup:
            m = re.match(".*?(?P<DAY>[0-9]{2}).(?P<MONTH>[0-9]{2}).(?P<YEAR>[0-9]{2}),&nbsp;(?P<HOUR>[0-9]{2}):(?P<MIN>[0-9]{2})h.*?", dateSoup.string)
            if not m is None:
                day		 = int(m.group('DAY'))
                month	 = int(m.group('MONTH'))
                year	 = int(m.group('YEAR'))
                hour	 = int(m.group('HOUR'))
                min		 = int(m.group('MIN'))
                dateString = str(int(time.mktime((year, month, day, hour, min, 0, 0, 0, 0))))

        # find title in html
        titleString = ""
        titleSoup = soup.find("h1", { "class" : "ArtikelTitel" })
        if titleSoup:
            titleString = titleSoup.string
            
        articleTeaser = ""
        teaserSoup = soup.find("h2", { "class" : "ArtikelTeaser" })
        if teaserSoup:
            titleString = teaserSoup.string    
            
            

        return json.dumps({ "title" : titleString , "dateCreated" : dateString, "content" : contentString })
	
    
    def extractKeyWords(self, url):
        """ KSTA provides keywords inside the html which can be easily crawled and later used for automatic text categorization 
        """
        
	
	
if __name__ == '__main__':
    
    ksta_crawler = LoadContentFromUrl()
    test_url = "http://ksta.de/html/artikel/1318243866302.shtml"
    ksta_text = ksta_crawler.getContentsByUrlWithIntroText(test_url, "polen")
    print ksta_text + "\n"
    
    test_url = "http://ksta.de/html/artikel/1319813681424.shtml"    
    ksta_text = ksta_crawler.getContentsByUrlWithIntroText(test_url, "polen")
    print ksta_text + "\n"
    
    print "the difference of text length\n"
    print str(len(ksta_text))
              
    
