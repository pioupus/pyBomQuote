#!/usr/bin/env python3

'''
Created on 15.04.2015

@author: arne
'''

import urllib

import pprint
from urllib.request import urlopen
from urllib.request import HTTPError

from bs4 import BeautifulSoup

import octopart_module.api_config_my

import json


def getUSDCurrencyValue():
    sock = urlopen('http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml')
    currency_xml = sock.read()
    sock.close();
    soup = BeautifulSoup(currency_xml)
    curency_USD = soup.find('cube', attrs={'currency':'USD'})
    #print soup
    curency_USD = float(curency_USD['rate'])
    print("USD Kurs "+str(curency_USD))
    return curency_USD

def findDescription(descriptions, seller):
    if '__class__' in descriptions:
        return descriptions['value']

    seller = seller.lower().strip()
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(descriptions)
    for description in descriptions:
        #pp.pprint(description)
        #if 'attribution' not in description:
            #continue
            #print('attribution not found in')
            #pp = pprint.PrettyPrinter(indent=4)
            #pp.pprint(description)
        if 'sources' not in description['attribution']:
            continue			
        if description['attribution']['sources'] == None:
            continue			
			
        for source in description['attribution']['sources']:
            if source['name'].lower().strip() == seller:
                #print ("found description")
                return description['value']
    return descriptions[0]['value']

class octopart(object):
    def __init__(self, MPN, lagerndeProdukte,USAProdukte,vendor):

        self.lagerndeProdukte = lagerndeProdukte
        self.USAProdukte = USAProdukte
        self.MPN = MPN
        self.seachURL = ''
        self.downloadOK = 1
        self.page = ''
        self.vendor = vendor
        searchString = MPN;
           
        queries = [
            {'mpn': MPN,
            # 'seller': '2c3be9310496fffc',
             'reference': 'ref1',
             }
            ]

        self.seachURL = 'http://octopart.com/api/v3/parts/match?queries=%s'   \
            % urllib.parse.quote(json.dumps(queries))
        self.seachURL += '&apikey='+octopart_module.api_config_my.API_KEY
        self.seachURL += '&pretty_print=true'
        self.seachURL += '&include[]=descriptions'
        

        #self.seachURL = url_fix(self.seachURL)
        
        print(self.seachURL)
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'ausUSA':[],'URL':[],'supplier':[]}
        try:        
            sock = urlopen(self.seachURL)                                    
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
                        if offer['seller']['name'] == self.vendor:
                            #print "Digikey"
                            productBypreferredSeller = 1
                            offers.append(offer)

                    if productBypreferredSeller:
                        item['offers'] = offers
                        self.digikey_item.append(item)
                        
                        for description in item['descriptions']:
                            if description['attribution']['sources'] != None:
                                if description['attribution']['sources'][0]['name'] == self.vendor:
                                    item['descriptions'] = description
                                    break;
            
            
            #print(self.digikey_item[0]['offers'])
            #print self.digikey_item
                    
            sock.close()
        except HTTPError as err:
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
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'packaging':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'pku':[], 'ausUSA':[],'URL':[],'supplier':[]}
        for product in self.digikey_item:
            #print "product"
            for offer in product['offers']:
                #pp = pprint.PrettyPrinter(indent=4)
                #pp.pprint(offer)
                manufacturer = product['brand']['name'].encode('utf-8')
                mpn = product['mpn']
                description = findDescription(product['descriptions'],self.vendor)

                fromUSA = 0     
                
                sku = offer['sku']
                packSize = 1
                stock = offer['in_stock_quantity']
                if self.lagerndeProdukte and (stock == 0):
                    continue
            
                minVPE = offer['moq']
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
                result['manufacturer'].append(manufacturer.decode())
                result['mpn'].append(mpn)
                result['description'].append(description)
                result['stock'].append(stock)
                result['minVPE'].append(minVPE)
                result['pku'].append(packSize)
                result['ausUSA'].append(fromUSA)
                result['packaging'].append(offer["packaging"])
                result['supplier'].append(self.vendor)
            
        return result
        

