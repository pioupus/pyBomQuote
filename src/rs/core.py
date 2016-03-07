#!/usr/bin/env python

import urllib2
import re
from bs4 import BeautifulSoup
from string import maketrans
from socket import error as socket_error

import urllib
import urlparse

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



class Rs(object):

    def __init__(self, MPN, lagerndeProdukte,USAProdukte):
        headers = {
            "User-Agent": "Wget/1.13.4 (linux-gnu)",
            "Accept": "*/*",
            "Connection": "keep-alive"
        }
        self.lagerndeProdukte = lagerndeProdukte
        self.USAProdukte = USAProdukte
        self.MPN = MPN
        self.seachURL = ''
        
        self.page = ''
        searchString = MPN;
        
        self.seachURL='http://de.rs-online.com/web/c/?searchTerm='+searchString+'&sra=oss&r=t&sort-by=P_breakPrice1&sort-order=asc&pn=1'
        self.seachURL = url_fix(self.seachURL)
        #print(self.seachURL)
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[],'pku':[],  'ausUSA':[],'URL':[],'supplier':[]}
        for retry in range(3):
            self.downloadOK = 1
            try:
                req = urllib2.Request(self.seachURL, None, headers = headers)
                self.page = urllib2.urlopen(req).read() 
            except socket_error as serr:
                self.downloadOK = 0
                print "DownloadError: "+str(serr)
            if self.downloadOK:
                break


    def getPage(self):
        return self.page

    def getUrl(self):
        return self.seachURL
        
    def parse(self):
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'pku':[], 'ausUSA':[],'URL':[],'supplier':[]}
        if self.downloadOK:
            soup = BeautifulSoup(self.page)
            prodTable = soup.find('table', attrs={'class':'srtnListTbl'})
            if prodTable == None:        
                sku = soup.find('span', attrs={'itemprop':'sku'})
                if sku == None:
                    result = {'ordercode':['-1'], 'manufacturer':['-'], 'mpn':['-'], 'description':['-'], 'stock':[-1], 'pricebreaks':[[-1]], 'prices':[[-1]], 'minVPE':[-1],'pku':[-1],  'ausUSA':[-1],'URL':[self.seachURL],'supplier':['RS']}
                else:
                    sku = sku.contents[0].encode('utf-8').strip()
                    mpn = soup.find('span', attrs={'itemprop':'mpn'})
                    if mpn==None:
                        mpn = '-'
                    else:
                        mpn = mpn.contents[0].encode('utf-8').strip()
                    
                    hersteller = soup.find('span', attrs={'itemprop':'brand'})
                    if hersteller == None:
                        hersteller = 'Nicht verfuegbar'
                    else:
                        hersteller = hersteller.contents[0].encode('utf-8').strip()
                        
                    
                    description = soup.find('div', attrs={'class':'productDetailsContainer floatRight'})
                    if description == None:
                        description = 'Nicht verfuegbar'
                    else:
                        description = description.find('div').contents[0].encode('utf-8').strip()
                        description = description.translate(maketrans('\xbc\xce\xc2\xb1', 'u  +')) 
                    minVPE = soup.find('div', attrs={'class':'addToCartRTQContainer'})
                    if minVPE == None:
                        minVPE = '-1'
                    else: 
                        minVPE = minVPE.find('form')
                        minVPE = minVPE.find('div', attrs={'class':'qty'}).find('input')['value']
                        minVPE = int(minVPE)
                    url = soup.find('link', attrs={'rel':'canonical'})['href']
                    stock = soup.find('div', attrs={'class':'floatLeft stockMessaging availMessageDiv bottom5'})
                    if stock == None:
                        stock = 'Nicht verfuegbar'
                    else:
                        #print(stock)
                        stock = stock.find('link')['href']
                        if stock == "http://schema.org/InStock":
                            stock = 'Lieferbar'
                        else:
                           stock = 'Nicht verfuegbar'                 
                    result['ordercode'].append(sku);
                    result['URL'].append(url);
                    result['manufacturer'].append(hersteller);
                    result['mpn'].append(mpn);
                    result['description'].append(description);
                    result['minVPE'].append(minVPE);
                    result['pku'].append(1);
                    result['stock'].append(stock);
                    result['ausUSA'].append(0);
                    #print(sku)
                    #print(mpn)
                    #print(hersteller)
                    #print(description)
                    #print(minVPE)
                    #print(stock)
                    rows = soup.find('ul', attrs={'class':'breakPricesList'})
                    if rows == None:
                        result['pricebreaks'].append([-1])
                        result['prices'].append([-1])
                        #result = {'ordercode':['-1'], 'manufacturer':['-'], 'mpn':['-'], 'description':['-'], 'stock':[-1], 'pricebreaks':[[-1]], 'prices':[[-1]], 'minVPE':[-1], 'ausUSA':[-1],'URL':[self.seachURL],'supplier':['RS']}                    
                    else:
<<<<<<< HEAD
                        rows = rows.find_all('li', attrs={'itemprop':'priceSpecification'})
=======
                        
                        rows = rows.find_all('li')
>>>>>>> 37dc8b37ed02b0710e4c57d9c1aa3e910dc36684
                        prices_item = []
                        breaks_item = []
                        
                        for row in rows:
<<<<<<< HEAD
                            #print(row)
                            qty = row.find('div', attrs={'itemprop':'eligibleQuantity'})
                            if qty == None:
                                qty = row.find('div', attrs={'class':'qty hide'})
                                if qty == None:
                                    continue
                                qty = qty.find('span').contents[0].encode('utf-8').strip()
                                #print qty
                            else:
=======
                            if row['id'] == "emptyBox":
                                continue
                            #print(row)
                            qty = row.find('div', attrs={'class':'qty hide'})
                            #print qty
                            if qty == None:
                                qty = row.find('div', attrs={'itemprop':'eligibleQuantity'})
                                if qty == None:
                                    continue
>>>>>>> 37dc8b37ed02b0710e4c57d9c1aa3e910dc36684
                                qty = qty.find('meta', attrs={'itemprop':'minValue'})
                                if qty == None:
                                    continue
                                qty = qty["content"]
<<<<<<< HEAD
=======
                            else:
                                qty = qty.find('span').contents[0].encode('utf-8').strip()
                            
>>>>>>> 37dc8b37ed02b0710e4c57d9c1aa3e910dc36684
                            #print(qty)
                            qty = int(qty)
                            breaks_item.append(qty)
                           
                            
                            price = row.find('meta', attrs={'itemprop':'price'})
                            if price == None:
<<<<<<< HEAD
                                price = row.find('span', attrs={'id':'breakUnitPrice'}) 
                                if price == None:
                                    continue
                                #print price     
                                price = price.contents[0].encode('utf-8').strip()
                                                           
=======
                                price = row.find('span', attrs={'id':'breakUnitPrice'})
                                if price == None:
                                    price = '-1'
                                else:
                                    price = price.contents[0].encode('utf-8').strip()
>>>>>>> 37dc8b37ed02b0710e4c57d9c1aa3e910dc36684
                            else:
                                price = price["content"]
                            price = price.strip('\xe2\x82\xac ').replace(',','.')
                            price = price.split(' ',2)[0]
                            price = float(price)
                            #print(price)
                           # print(price)
                            prices_item.append(price)
                        result['pricebreaks'].append(breaks_item)
                        result['prices'].append(prices_item)
                    result['supplier'].append('RS');
            else:
                rows = prodTable.find_all('tr')
                for row in rows:
                    description = row.find('a', attrs={'class':'tnProdDesc'})
                    if description == None:
                        description = row.find('td', attrs={'class':'descColHeader'}).find('div', attrs={'class':'srDescDiv'})
                        description = description.find('a').contents[0].encode('utf-8').strip()
                    else:
                        description = description.contents[0].encode('utf-8').strip()
                    description = description.translate(maketrans('\xbc\xce\xc2\xb1', 'u  +')) 
                    fields = row.find_all('span', attrs={'class':'labelText'})
                    url = '';
                    mpn_found=0
                    for field in fields:
                        content = field.contents[0].encode('utf-8').strip()
                        fieldname=''
                        skufound=False
                        if 'RS Best.' in content:
                            skufound=True
                            fieldname='ordercode'
                        elif 'Marke' == content:
                            fieldname = 'manufacturer'
                        elif 'Herst. Teile' in content:
                            fieldname = 'mpn'
                            mpn_found=1;
                        
                        value = field.parent.find('a')
                        if skufound:
                            url = 'http://de.rs-online.com'+value['href']
                        if value != None:
                            value = value.contents[0].encode('utf-8').strip()
                        else:
                            value = field.parent.find('span',attrs={'class':'defaultSearchText'}).contents[0].encode('utf-8').strip()
                       # print(fieldname+' '+value);
                        if fieldname != '':
                            result[fieldname].append(value);
                        
                    if mpn_found == 0:#happens when Hausmarke RS
                        result['mpn'].append('-');
                        
                    minVPE = row.find().find('div',attrs={'class':'qtyBtn'})
                    if minVPE == None:
                        minVPE = '-1'
                        pb = -1;
                    else:
                        minVPE = minVPE.find('input')['value']
                        minVPE = int(minVPE)
                        pb = minVPE
                    price = row.find('div',attrs={'class':'priceFixedCol'}).find('ul',attrs={'class':'viewDescList'})
                    prices = price.find_all('span')
                    for price_ in prices:
                        #print price_
                        if price_['class'] == 'priceWas':
                            continue
                        if 'price' in price_ ['class']:
                            price = price_
                            break
                    price = price.contents[0].encode('utf-8').strip()
                    price = price.strip('\xe2\x82\xac ').replace(',','.')
                    price = price.split(' ',2)[0]
                    price = price.split('.');# in case we have numbers like 3.256.99
                    price_str = '';
                    for i in range(len(price)-1):
                        price_str = price_str+price[i];
                    price_str = price_str+'.'+price[-1];
                    #print(price_str)
                    price = float(price_str) 
                    result['prices'].append([price])
                    result['pricebreaks'].append([pb])
                    result['description'].append(description);
                    result['minVPE'].append(minVPE);
                    result['pku'].append(1);
                    result['ausUSA'].append(0);
                    result['supplier'].append('RS');
                    result['stock'].append(-1);
                    result['URL'].append(url);
    #                result['manufacturer'].append(hersteller);
        else:
            result = {'ordercode':['-1'], 'manufacturer':['-'], 'mpn':['-'], 'description':['-'], 'stock':[-1], 'pricebreaks':[[-1]], 'prices':[[-1]], 'minVPE':[-1], 'pku':[-1], 'ausUSA':[-1],'URL':[self.seachURL],'supplier':['RS']}
        #print(result)  
        return result