#!/usr/bin/env python3

'''
Created on 15.04.2015

@author: arne
'''

import requests

import mouser_api.api_config_my



class Mouser_api(object):
    def __init__(self, MPN, lagerndeProdukte,USAProdukte):
        self.lagerndeProdukte = lagerndeProdukte
        self.USAProdukte = USAProdukte
        self.MPN = MPN
        self.seachURL = ''
        self.downloadOK = 1
        self.page = ''
        searchString = MPN;
        url = 'https://api.mouser.com/api/v1.0/search/partnumber'
        data = {"SearchByPartRequest": {"mouserPartNumber":MPN, "partSearchOptions": ""}}
        params = {'apiKey': mouser_api.api_config_my.API_KEY}

        
        response = requests.post(url, params=params, json=data)
        self.page_result = response.json()
        self.page = response.text
        

            
        
    def getPage(self):
        return self.page
    
    def getUrl(self):
        return self.seachURL
    
    def parse(self):

        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'pku':[], 'ausUSA':[],'URL':[],'supplier':[]}
        #print(self.page_result)
        for product in self.page_result["SearchResults"]["Parts"]:
            #print product
            sku = product["MouserPartNumber"].encode('utf-8').strip()
            manufacturer = product["Manufacturer"].encode('utf-8').strip()
            mpn = product["ManufacturerPartNumber"].encode('utf-8').strip()
            description = product["Description"].encode('utf-8').strip()
            stock = product["Availability"].encode('utf-8').strip()
            minVPE = product["Min"].encode('utf-8').strip()
            minVPE = int(minVPE)
            packSize =product["Mult"].encode('utf-8').strip()
            URL = product["ProductDetailUrl"].encode('utf-8').strip() 

            prices_item = []
            breaks_item = []
            
            for pricing in product["PriceBreaks"]:
                qty = pricing["Quantity"] 
                qty = int(qty)
                breaks_item.append(float(qty))

                price = pricing["Price"] #'0,085 \xe2\x82\xac'
                price = price.split(" ",1)[0] 
                price = price.replace(",",".")
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
            result['ausUSA'].append(0)
            result['supplier'].append('Mouser')
            
        return result
        

