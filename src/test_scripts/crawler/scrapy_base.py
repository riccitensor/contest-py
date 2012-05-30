'''
Created on 04.11.2011

Due to limitations in urllib/beautyfullsoup scrapy should now be used to crawl websites


@author: karisu
'''



from scrapy.item import Item, Field

class Torrent(Item):
    url = Field()
    name = Field()
    description = Field()
    size = Field()
              
              
              
class MininovaSpider(CrawlSpider):

    name = 'mininova.org'
    allowed_domains = ['mininova.org']
    start_urls = ['http://www.mininova.org/today']
    rules = [Rule(SgmlLinkExtractor(allow=['/tor/\d+']), 'parse_torrent')]

    def parse_torrent(self, response):
        x = HtmlXPathSelector(response)

        torrent = TorrentItem()
        torrent['url'] = response.url
        torrent['name'] = x.select("//h1/text()").extract()
        torrent['description'] = x.select("//div[@id='description']").extract()
        torrent['size'] = x.select("//div[@id='info-left']/p[2]/text()[2]").extract()
        return torrent
              
    