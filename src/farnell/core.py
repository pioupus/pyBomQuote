#!/usr/bin/env python

import urllib2
import re
from bs4 import BeautifulSoup
from string import maketrans

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

class Farnell(object):
    

    
    def __init__(self, MPN, lagerndeProdukte,USAProdukte):
        self.lagerndeProdukte = lagerndeProdukte
        self.USAProdukte = USAProdukte
        self.MPN = MPN
        self.seachURL = ''
        searchString = MPN;
        if lagerndeProdukte:
            if USAProdukte:
                self.seachURL='http://de.farnell.com/jsp/search/browse.jsp?N=0+708+502&Ns=P_PRICE_FARNELL_DE|0&Ntk=gensearch&Ntt='+searchString+'&Ntx=mode+matchallpartial&ref=globalsearch'
            else:
                self.seachURL='http://de.farnell.com/jsp/search/browse.jsp?N=0+708&Ns=P_PRICE_FARNELL_DE|0&Ntk=gensearch&Ntt='+searchString+'&Ntx=mode+matchallpartial&ref=globalsearch'
        elif USAProdukte:
            self.seachURL='http://de.farnell.com/jsp/search/browse.jsp?N=0+502&Ns=P_PRICE_FARNELL_DE|0&Ntk=gensearch&Ntt='+searchString+'&Ntx=mode+matchallpartial&ref=globalsearch'
        else:
            self.seachURL='http://de.farnell.com/jsp/search/browse.jsp?N=0&Ns=P_PRICE_FARNELL_DE|0&Ntk=gensearch&Ntt='+searchString+'&Ntx=mode+matchallpartial&ref=globalsearch'
  
        self.seachURL = url_fix(self.seachURL)
        print(self.seachURL)
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'ausUSA':[],'URL':[],'supplier':[]}
        sock = urllib2.urlopen(self.seachURL)                                    
        self.page = sock.read()
        sock.close()
        
        
    def getPage(self):
        return self.page
    
    def parse(self):
        result = {'ordercode':[], 'manufacturer':[], 'mpn':[], 'description':[], 'stock':[], 'pricebreaks':[], 'prices':[], 'minVPE':[], 'ausUSA':[],'URL':[],'supplier':[]}
        soup = BeautifulSoup(self.page)
        pagetest = soup.find_all('div', attrs={'class':'productDisplay'})
        if pagetest != []:
            details = soup.find('div', attrs={'id':'productDescription'}).find('ul')
            details = details.find_all('li');
            Manufacturer = details[0].find('a').contents[0].encode('utf-8').strip()
            #.find('ul')
            ordercode = details[1].contents[2].encode('utf-8').strip()
            mpn =  details[2].contents[2].encode('utf-8').strip()
            
            description = soup.find('div', attrs={'id':'productHeader'}).find('h1').contents[0].encode('utf-8').strip()
            description = description.translate(None, "\xc2\xa0\n\t\t");
            
                     #           price = pricebreak.find('strong').contents[0].encode('utf-8').strip('\xe2\x82\xac ')
                    #price = price.replace(',','.');
                    
            stock = soup.find('div', attrs={'id':'priceWrap'}).find('p').contents[2].encode('utf-8')
            stock = stock.translate(None, ".\t\n\r \xc2\xa0").strip()


            minVPE = soup.find('div', attrs={'id':'commonInfo'})
            if minVPE == None:
                minVPE = 0
            else:
                minVPE = minVPE.find_all('p')[2].contents[2].encode('utf-8')
                minVPE = minVPE.translate(None, ".\t\n\r \xc2\xa0").strip()
                minVPE = int(minVPE)
            
            
            result['manufacturer'].append(Manufacturer)
            result['ordercode'].append(ordercode)
            result['mpn'].append(mpn)
            result['URL'].append('http://de.farnell.com/'+ordercode);
            result['description'].append(description);
            result['stock'].append(stock);
            result['minVPE'].append(minVPE);
            
            ausUSA = soup.find('div', attrs={'class':'highLightBox'})
            #ausUSA = soup.find('div', attrs={'id':'internalDirectShipTooltip'})
            ausUSA = ausUSA.find('a', text='US-Bestand')
            #print(ausUSA)
            if ausUSA==None:
                result['ausUSA'].append(0)
            else:
                result['ausUSA'].append(1)
            pricing_htm = soup.find('table', attrs={'class':'pricing'}).find('tbody')
            pricing_htm = pricing_htm.find_all('tr');
            prices_item = []
            breaks_item = []
            for pricing_tr in pricing_htm:
                qty = pricing_tr.find('td', attrs={'class':'qty'}).contents[0].encode('utf-8')
                qty = qty.translate(None, "\xc2\xa0\n\t\t+");
                qty = qty.split('-',2)[0]
                qty = int(qty)
                breaks_item.append(float(qty))
                #print(qty)
                
                #price = pricing_tr.find('td', attrs={'class':'threeColTd pdpPriceRightCol'})
                price = pricing_tr.find('td', attrs={'class':'threeColTd'})
                price = price.contents[2].encode('utf-8')
                price = price.strip('\xe2\x82\xac ').replace(',','.')
                price = price.split(' ',2)[0]
                price = float(price)
                prices_item.append(float(price))
                #print(price)
                
            result['pricebreaks'].append(breaks_item)
            result['prices'].append(prices_item)
            result['supplier'].append('Farnell');   
                
        
        else:
            pageresults = soup.find('table', attrs={'id':'sProdList'})
            if pageresults == None:
                result = {'ordercode':['-1'], 'manufacturer':['-'], 'mpn':['-'], 'description':['-'], 'stock':['-1'], 'pricebreaks':[[-1]], 'prices':[[-1]], 'minVPE':[-1], 'ausUSA':[-1],'URL':[self.seachURL],'supplier':['Farnell']}    
            else:
                pageresults = pageresults.find('tbody')
                pageresults = pageresults.find_all('tr');
                #print(pageresults)
                for productrow in pageresults:
                    row = productrow.find('td',attrs={'id':'stock','colspan':'3'})
                    #print (row)
                    if row != None:
                        US = row.find('p')
                        #print(US)
                        if US != None:
                            US = US.find('a',attrs={'class':'tooltipLink'})
                        if US == None:
                            result['ausUSA'].append(0)                        
                        else:
                            US = US.contents[0].encode('utf-8').strip()
                            if US == 'US-Bestand':
                                result['ausUSA'].append(1) 
                        continue
                    row = productrow
                    column = row.find('td',attrs={'class':'description'})
                    Manufacturer = column.find_all('p')[0].contents[0].encode('utf-8').strip()
                    description = column.find_all('p')[1].find('a').contents[0].encode('utf-8').strip()
                    column = row.find('td',attrs={'class':'productImage'})
                    ordercode = column.find('input')['value'].encode('utf-8').strip()
                    column = row.find('td',attrs={'class':'mftrPart'})
                    mpn = column.find('input')['value'].encode('utf-8').strip()
                    column = row.find('td',attrs={'class':'availability'})
                    stockstr = column.find('input')['value'].encode('utf-8').strip()
                    stock = stockstr
                    result['manufacturer'].append(Manufacturer);
                    result['description'].append(description);
                    result['ordercode'].append(ordercode);
                    result['mpn'].append(mpn);
                    result['URL'].append('http://de.farnell.com/'+ordercode);
                    result['stock'].append(stock);
    
    
                    minVPE = row.find('td',attrs={'class':'qty'}).find('div',attrs={'class':'qtyField'})
                    #print(minVPE)
                    if minVPE==None:
                        minVPE='-1'
                    else:
                        minVPE = minVPE.find('input')['value'].encode('utf-8').strip()
                        minVPE = minVPE.translate(None, ".\t\n\r \xc2\xa0").strip()
                        minVPE = int(minVPE)
                    result['minVPE'].append(minVPE);
                    
                    column = row.find('td',attrs={'class':'listPrice'})
                    column = column.find('p',attrs={'class':'price'})
                    pricebreaks_html = row.find_all('span', attrs ={'class':'priceBreak'})
                    pricebreaks_item = []
                    prices_item = []
                    for pricebreak in pricebreaks_html:
                        pricebrk = pricebreak.find('span', attrs ={'class':'qty'}).contents[0].encode('utf-8').strip('+\n ')
                        pricebrk = pricebrk.translate(maketrans("", ""),'.');
                        #print(pricebrk)
                        pricebreaks_item.append(float(pricebrk))
                        
                        price = pricebreak.find('strong').contents[0].encode('utf-8').strip('\xe2\x82\xac ')
                        price = price.replace(',','.');
                        #print(price)
                        prices_item.append(float(price))
                        
                    result['pricebreaks'].append(pricebreaks_item)
                    result['prices'].append(prices_item)
                    
                                             
                                    
                    #if pricebreaks_item == []:
                    #    result['minVPE'].append(-1)
                    #else:
                    #    result['minVPE'].append(pricebreaks_item[0])
     
                    
                    result['supplier'].append('Farnell');
        print(result)
        return result;
    



