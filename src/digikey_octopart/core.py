#!/usr/bin/env python

'''
Created on 15.04.2015

@author: arne
'''

import urllib
import urllib2
import urlparse
from bs4 import BeautifulSoup
from api_config_my import *

import json


def getUSDCurrencyValue():
        sock = urllib2.urlopen('http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
        currency_xml = sock.read()
        sock.close();
        soup = BeautifulSoup(currency_xml)
        curency_USD = soup.find('cube', attrs={'currency':'USD'})
        #print soup
        curency_USD = float(curency_USD['rate'])
        print "USD Kurs "+str(curency_USD) 
        return curency_USD


class Digikey_octo(object):
    def __init__(self, MPN, lagerndeProdukte,USAProdukte):

        self.lagerndeProdukte = lagerndeProdukte
        self.USAProdukte = USAProdukte
        self.MPN = MPN
        self.seachURL = ''
        self.downloadOK = 1
        self.page = ''
        searchString = MPN;
           
        queries = [
            {'mpn': MPN,
            # 'seller': '2c3be9310496fffc',
             'reference': 'ref1',
             }
            ]

        self.seachURL = 'http://octopart.com/api/v3/parts/match?queries=%s'   \
            % urllib2.quote(json.dumps(queries))
        self.seachURL += '&apikey='+API_KEY
        self.seachURL += '&pretty_print=true'
        self.seachURL += '&include[]=descriptions'
        

        #self.seachURL = url_fix(self.seachURL)
        
        #print(self.seachURL)
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'ausUSA':[],'URL':[],'supplier':[]}
        try:        
            sock = urllib2.urlopen(self.seachURL)                                    
            self.page = sock.read()
            
            #print self.page
            response = json.loads(self.page)
            
            # print request time (in milliseconds)
            #print response['msec']
            
            # print mpn's
            
            self.digikey_item = []
            for result in response['results']:
                for item in result['items']:
                    offers = []
                    productBypreferredSeller = 0
                    #print "item"
                    for offer in item['offers']:
                        if offer['seller']['name'] == 'Digi-Key':
                            #print "Digikey"
                            productBypreferredSeller = 1
                            offers.append(offer)

                    if productBypreferredSeller:
                        item['offers'] = offers
                        self.digikey_item.append(item)
                        
                        for description in item['descriptions']:
							if description['attribution']['sources'] != None:
								if description['attribution']['sources'][0]['name'] == 'Digi-Key':
									item['descriptions'] = description
									break;
            
            
            #print(self.digikey_item[0]['offers'])
            #print self.digikey_item
                    
            sock.close()
        except urllib2.HTTPError, err:
            print(err)
            self.downloadOK = 0
            with open("digikey_octopart.log", "ab") as logfile:
                logfile.write(str(err)+'\n')
                logfile.write(MPN+'\n')
                logfile.write(self.seachURL+'\n\n')
            
        
    def getPage(self):
        return self.page
    
    def getUrl(self):
        return self.seachURL
    
    def parse(self):
        USD_FACTOR = 0.0;
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'pku':[], 'ausUSA':[],'URL':[],'supplier':[]}
        for product in self.digikey_item:
            #print "product"
            for offer in product['offers']:
                #print "offer"
                #print product
                manufacturer = product['brand']['name'].encode('utf-8')
                mpn = product['mpn']
                description = product['descriptions']['value']

                fromUSA = 0     
                
                sku = offer['sku']
                packSize = 1
                stock = offer['in_stock_quantity']
                if self.lagerndeProdukte and (stock == 0):
                    continue
                if offer["packaging"]=="Custom Reel":
                    description = 'Digi-Reel: '+description
                    stock = str(stock) + ' / Digi-Reel'
                minVPE = offer['moq']

                URL = 'http://www.digikey.de/product-search/de?keywords='+sku
                                           
                prices_item = []
                breaks_item = []
                
                if 'EUR' not in offer['prices']:
                    CURR = 'USD'
                    if USD_FACTOR == 0.0:
                        USD_FACTOR = getUSDCurrencyValue()
                    CURR_FAC = USD_FACTOR
                else:
                    CURR = 'EUR'
                    CURR_FAC = 1.0
                for pricing in offer['prices'][CURR]:
                    qty = int(pricing[0])
                    breaks_item.append(float(qty));
                    price = pricing[1]
                    price = float(price)/CURR_FAC
                    prices_item.append(price)
        
                    
                result['pricebreaks'].append(breaks_item)
                result['prices'].append(prices_item)
                    
                result['ordercode'].append(sku)
                result['manufacturer'].append(manufacturer)
                result['mpn'].append(mpn)
                result['description'].append(description)
                result['stock'].append(stock)
                result['minVPE'].append(minVPE)
                result['pku'].append(packSize)
                result['URL'].append(URL)
                result['ausUSA'].append(fromUSA)
                result['supplier'].append('Digi-Key')
            
        return result
        

