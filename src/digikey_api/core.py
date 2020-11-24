#!/usr/bin/env python

'''
Created on 15.04.2015

@author: arne
'''


#from api_config_my import *
import digikey_api.api_config_my

import os
import digikey
from digikey.v3.productinformation import KeywordSearchRequest

from urllib.request import urlopen
from urllib.request import HTTPError

from bs4 import BeautifulSoup


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

    


class Digikey_api(object):
    def __init__(self, MPN, lagerndeProdukte,USAProdukte):
        self.lagerndeProdukte = lagerndeProdukte
        self.USAProdukte = USAProdukte
        searchString = MPN;
        os.environ['DIGIKEY_CLIENT_ID'] = digikey_api.api_config_my.DIGIKEY_CLIENT_ID
        os.environ['DIGIKEY_CLIENT_SECRET'] = digikey_api.api_config_my.DIGIKEY_CLIENT_SECRET
        os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
        os.environ['DIGIKEY_STORAGE_PATH'] = '.'

		# Query product number
       # dkpn = '296-6501-1-ND'
      #  part = digikey.product_details(dkpn)

		# Search for parts 
        search_request = KeywordSearchRequest(keywords=MPN, record_count=10)
        self.page_result = digikey.keyword_search(body=search_request)

        for product in self.page_result.products:
            print(product.manufacturer.value)
            print(product.manufacturer_part_number)
            print(product.digi_key_part_number)
            if product.detailed_description != None:
                print(product.product_description + "     " +product.detailed_description)
            else:
                print(product.product_description)
            print(product.quantity_available)
            
            prices_item = []
            breaks_item = []
            
            for pricing in product.standard_pricing:
                qty = pricing.break_quantity
                qty = int(qty)
                breaks_item.append(float(qty))

                price = pricing.unit_price
                price = float(price)
                prices_item.append(float(price))
            
            print(breaks_item)
            print(prices_item)
            
        self.seachURL = ""
        #print("result:")
        #print(result)
        #result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'ausUSA':[],'URL':[],'supplier':[]}


            
        
    def getPage(self):
        return ""
    
    def getUrl(self):
        return self.seachURL
    
    def parse(self):
        USD_FACTOR = 0.0
        currency = self.page_result.search_locale_used.currency
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'pku':[], 'ausUSA':[],'URL':[],'supplier':[], 'packaging':[]}
        for product in self.page_result.products:
            #print product
            packaging = product.packaging.value
            minVPE = product.minimum_order_quantity
            minVPE = int(minVPE)
            if "Digi-Reel" in packaging:
                continue
            if minVPE >= 100:
                continue                
            sku = product.digi_key_part_number
            manufacturer = product.manufacturer.value
            mpn = product.manufacturer_part_number
            if product.detailed_description != None:
                description = product.detailed_description
            else:
                description = product.product_description
            stock = product.quantity_available

            
            prices_item = []
            breaks_item = []
            
            if "US" in currency:
                if USD_FACTOR == 0.0:
                    USD_FACTOR = getUSDCurrencyValue()
                    CURR_FAC = 1.0
            elif "EUR" in currency:
                    CURR_FAC = 1.0
                    
            for pricing in product.standard_pricing:
                qty = pricing.break_quantity
                qty = int(qty)
                breaks_item.append(float(qty))

                price = pricing.unit_price
                price = float(price)/CURR_FAC
                prices_item.append(float(price))
                

            packSize = minVPE
            URL = product.product_url
            fromUSA = 0            
            

            result['pricebreaks'].append(breaks_item)
            result['prices'].append(prices_item)
                
            result['ordercode'].append(sku)
            result['manufacturer'].append(manufacturer)
            result['mpn'].append(mpn)
            result['packaging'].append(packaging)
            result['description'].append(description)
            result['stock'].append(stock)
            result['minVPE'].append(minVPE)
            result['pku'].append(packSize)
            result['URL'].append(URL)
            result['ausUSA'].append(fromUSA)
            result['supplier'].append('Digikey')
            
        return result
        

