#!/usr/bin/env python

'''
Created on 15.04.2015

@author: arne
'''

import urllib
import urllib2
import urlparse
from bs4 import BeautifulSoup
import api_config

def url_fix(s, charset='utf-8'):
    """Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:

    >>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklarung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    :param charset: The target charset for the URL if the url was
                    given as unicode string.
    """
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))


FARNELLSTORE = 'de.farnell.com'

class Farnell_api(object):
    def __init__(self, MPN, lagerndeProdukte,USAProdukte):
        self.lagerndeProdukte = lagerndeProdukte
        self.USAProdukte = USAProdukte
        self.MPN = MPN
        self.seachURL = ''
        self.downloadOK = 1
        self.page = ''
        searchString = MPN;
        self.seachURL = 'http://api.element14.com/catalog/products'+\
            '?callInfo.responseDataFormat=XML'+\
            '&term=any%3A'+MPN+\
            '&storeInfo.id='+FARNELLSTORE+\
            '&callInfo.apiKey='+API_KEY+\
            '&resultsSettings.offset=0'+\
            '&resultsSettings.numberOfResults=10'+\
            '&resultsSettings.refinements.filters='+\
            '&resultsSettings.responseGroup=Prices%2CInventory'
            
        self.seachURL = 'http://api.element14.com/catalog/products'+\
            '?term=any:'+MPN+\
            '&storeInfo.id=de.farnell.com'+\
            '&callInfo.omitXmlSchema=false'+\
            '&callInfo.responseDataFormat=xml'+\
            '&callInfo.callback='+\
            '&callInfo.apiKey='+API_KEY+\
            '&resultsSettings.offset=0'+\
            '&resultsSettings.numberOfResults=20'+\
            '&resultsSettings.refinements.filters='+\
            '&resultsSettings.responseGroup=prices,inventory'

#http://api.element14.com/catalog/products?term=any%3Afuse&&storeInfo.id=de.farnell.com&callInfo.omitXmlSchema=false&callInfo.responseDataFormat=json&callInfo.callback=&callInfo.apiKey=szrm7kzwd28w5ce5s828gzvm&resultsSettings.offset=0&resultsSettings.numberOfResults=1&resultsSettings.refinements.filters=&resultsSettings.responseGroup=prices
#http://api.element14.com/catalog/products?term=any%3Afuse&storeInfo.id=uk.farnell.com&resultsSettings.offset=0&resultsSettings.numberOfResults=1&resultsSettings.refinements.filters=&resultsSettings.responseGroup=prices&callInfo.omitXmlSchema=false&callInfo.callback=&callInfo.responseDataFormat=json&callinfo.apiKey=gd8n8b2kxqw6jq5mutsbrvur

        self.seachURL = url_fix(self.seachURL)
        
        print(self.seachURL)
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'ausUSA':[],'URL':[],'supplier':[]}
        try:        
            sock = urllib2.urlopen(self.seachURL)                                    
            self.page = sock.read()
            sock.close()
        except urllib2.HTTPError, err:
            print(err)
            self.downloadOK = 0
            
        
    def getPage(self):
        return self.page
    
    def getUrl(self):
        return self.seachURL
    
    def parse(self):
        soup = BeautifulSoup(self.page)
        products = soup.find_all('ns1:products')
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'ausUSA':[],'URL':[],'supplier':[]}
        for product in products:
            sku = product.find('<ns1:sku>')
            print 'test'


