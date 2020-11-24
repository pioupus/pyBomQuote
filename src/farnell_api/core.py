#!/usr/bin/env python3

'''
Created on 15.04.2015

@author: arne
'''

import urllib
from urllib.request import urlopen
from urllib.request import HTTPError

from urllib.parse import urlsplit, urlunsplit, quote, urlunparse, quote_plus

from bs4 import BeautifulSoup
import farnell_api.api_config_my

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
    scheme, netloc, path, qs, anchor = urllib.parse.urlsplit(s)
    path = urllib.parse.quote(path, '/%')
    qs = urllib.parse.quote_plus(qs, ':&=')
    result = urllib.parse.urlunsplit((scheme, netloc, path, qs, anchor))
    result = result.replace('#','%23')
    return result;
    


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
            '?term=any:'+MPN+\
            '&storeInfo.id='+farnell_api.api_config_my.API_STORE+\
            '&callInfo.omitXmlSchema=false'+\
            '&callInfo.responseDataFormat=xml'+\
            '&callInfo.callback='+\
            '&callInfo.apiKey='+farnell_api.api_config_my.API_KEY+\
            '&resultsSettings.offset=0'+\
            '&resultsSettings.numberOfResults=20'+\
            '&resultsSettings.refinements.filters='+\
            '&resultsSettings.responseGroup=prices,inventory'

#http://api.element14.com/catalog/products?term=any%3Afuse&&storeInfo.id=de.farnell.com&callInfo.omitXmlSchema=false&callInfo.responseDataFormat=json&callInfo.callback=&callInfo.apiKey=szrm7kzwd28w5ce5s828gzvm&resultsSettings.offset=0&resultsSettings.numberOfResults=1&resultsSettings.refinements.filters=&resultsSettings.responseGroup=prices
#http://api.element14.com/catalog/products?term=any%3Afuse&storeInfo.id=uk.farnell.com&resultsSettings.offset=0&resultsSettings.numberOfResults=1&resultsSettings.refinements.filters=&resultsSettings.responseGroup=prices&callInfo.omitXmlSchema=false&callInfo.callback=&callInfo.responseDataFormat=json&callinfo.apiKey=gd8n8b2kxqw6jq5mutsbrvur
        print("Farnell request for part: "+MPN)
        self.seachURL = url_fix(self.seachURL)
        
        #print(self.seachURL)
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'ausUSA':[],'URL':[],'supplier':[]}
        try:        
            sock = urlopen(self.seachURL)                                    
            self.page = sock.read()
            sock.close()
        except HTTPError as err:
            print(err)
            self.downloadOK = 0
            with open("farnell_api.log", "ab") as logfile:
                logfile.write(str(err)+'\n')
                logfile.write(MPN+'\n')
                logfile.write(self.seachURL+'\n\n')
        print("Farnell request finished")    
        
    def getPage(self):
        return self.page
    
    def getUrl(self):
        return self.seachURL
    
    def parse(self):
        print("Parsing for Farnell Part: "+self.MPN)
        soup = BeautifulSoup(self.page)
        products = soup.find_all('ns1:products')
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'pku':[], 'ausUSA':[],'URL':[],'supplier':[]}
        for product in products:
            #print product
            sku = product.find('ns1:sku').contents[0].encode('utf-8').strip()
            manufacturer = product.find('ns1:brandname').contents[0].encode('utf-8').strip()
            mpn = product.find('ns1:translatedmanufacturerpartnumber').contents[0].encode('utf-8').strip()
            description = product.find('ns1:displayname').contents[0].encode('utf-8').strip()
            stock = product.find('ns1:inv').contents[0].encode('utf-8').strip()
            minVPE = product.find('ns1:translatedminimumorderquality').contents[0].encode('utf-8').strip()
            minVPE = int(minVPE)
            packSize = product.find('ns1:packsize').contents[0].encode('utf-8').strip()
            URL = str(farnell_api.api_config_my.API_STORE)+'/'+str(sku)
            fromUSA = 1            
            for region in product.find('ns1:stock').find_all('ns1:regionalbreakdown'):
                lvl = int(region.find('ns1:level').contents[0].encode('utf-8').strip())
                warehouse = region.find('ns1:warehouse').contents[0].encode('utf-8').strip()
                #print(str(lvl) + '@'+warehouse)
                if warehouse.lower() != 'us' and lvl > 0:
                    fromUSA = 0
                    
            prices_item = []
            breaks_item = []
            
            for pricing in product.find_all('ns1:prices'):
                qty = pricing.find('ns1:from').contents[0].encode('utf-8')
                qty = int(qty)
                breaks_item.append(float(qty))

                price = pricing.find('ns1:cost').contents[0].encode('utf-8')
                price = float(price)
                prices_item.append(float(price))
                #print(price)
                
            result['pricebreaks'].append(breaks_item)
            result['prices'].append(prices_item)
                
            result['ordercode'].append(sku.decode())
            result['manufacturer'].append(manufacturer.decode())
            result['mpn'].append(mpn.decode())
            result['description'].append(description.decode())
            result['stock'].append(stock.decode())
            result['minVPE'].append(minVPE)
            result['pku'].append(packSize.decode())
            result['URL'].append(URL)
            result['ausUSA'].append(fromUSA)
            result['supplier'].append('Farnell')
        print("Part parsing Farnell finished")         
        return result
        

