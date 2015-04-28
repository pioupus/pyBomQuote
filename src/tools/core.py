'''
Created on 26.04.2015

@author: arne
'''
import math
import sys
import csv 

def getBestPrice(realPrice,tolerance=0.0):
    if realPrice[0]['price']+tolerance < realPrice[1]['price']:
        return realPrice[0]
    else:
        return realPrice[1]
    
def getRealPrice(qtyOrig,minVPE,pricelist,pricebreaks):
    #pricebreak =[2,3,20]
    #pricelist =[0.5,0.3,0.25]
    pindex = 0;
    realPrice = [{'price':0,'qty':1},{'price':0,'qty':1}]

    if 1:
        qtyOrig = float(qtyOrig)
        minVPE = float(minVPE)

            
        qty = math.ceil(qtyOrig/minVPE)
        qty = qty*minVPE
        if qty < pricebreaks[0]:
            qty = pricebreaks[0]
        for pb in pricebreaks: 
            if float(qty) < pb:
                break;
            pindex = pindex+1;
        
        if pindex == 0:
            pindex =1;
       
        pb = pricebreaks[pindex-1]
        
        if (minVPE < 0) or (qty < 0) or (pricelist[0] < 0) or pricebreaks[0] < 0:
            realPrice[0]['price'] = sys.maxint
            realPrice[0]['qty'] = qty
            realPrice[1]['price'] =         realPrice[0]['price']
            realPrice[1]['qty'] =    realPrice[0]['qty']
        else:
            realPrice[0]['price'] = round(pricelist[pindex-1]*qty,2)
            realPrice[0]['qty'] = qty
            realPrice[1]['price'] =         realPrice[0]['price']
            realPrice[1]['qty'] =    realPrice[0]['qty']

        #print(optPrice)
        #print(len(pricebreaks))
        if len(pricebreaks) > pindex:
            secondtotalprice = pricelist[pindex]*pricebreaks[pindex]
            realPrice[1]['price'] = round(secondtotalprice,2)
            realPrice[1]['qty'] = pricebreaks[pindex]

    return realPrice



class BOMQuoteData():
    def __init__(self, csvPath=None, parent=None):
        self.bomData = []
        if csvPath is not None:
            self.loadFromCSV(csvPath)
            
    
    def getBomData(self):
        return self.bomData
    
    def doPricing(self):
        for bom in self.bomData:
            qty = bom['menge'];
            for quote in bom['quotes']:
                pb = quote['pricebreaks']
                prices = quote['prices']
                minVPE = quote['minVPE']
                realPrice = getRealPrice(qty,minVPE,prices,pb);
                opt_price = getBestPrice(realPrice, tolerance=0.5)
                if 0:
                    print('sku: '+str(quote['sku']))
                    print('prces: '+str(quote['prices']))         
                    print('pbs:' + str(quote['pricebreaks']))
                    print('qty:' + str(qty))                  
                    print('minVPE:' + str(minVPE))
                    print(opt_price)
                    print('\n')
                quote['opt_price'] = opt_price['price']
                quote['opt_qty'] = opt_price['qty']
                
    def loadFromCSV(self,path):
        csvreader = csv.reader(open(path, "rb"), delimiter="|")
        for row in csvreader: 
            bomDataSet = {}
            if row[1] == 'orig':
                bomDataSet['checked'] = int(row[0])
                bomDataSet['menge'] = int(row[2])
                bomDataSet['mpn'] = row[4]
                bomDataSet['manufacturer'] = row[5]
                bomDataSet['ref'] = row[3]
                bomDataSet['description'] = row[6]
                bomDataSet['footprint'] = row[7]
                bomDataSet['quotes'] = []
                self.bomData.append(bomDataSet);
            else:
                quoteDataSet={}
                quoteDataSet['sku'] = row[4]
                stock = row[11]
                if stock.isdigit():
                    stock = int(stock);
                    stock = str(stock)
                quoteDataSet['stock'] = stock
                USA = row[12]
                if USA == 'nichtAusUSA':
                    quoteDataSet['usa'] = 0
                else:
                    quoteDataSet['usa'] = 1
                quoteDataSet['description'] = row[7]
                quoteDataSet['minVPE'] = row[8]
                quoteDataSet['pricebreaks'] = []
                quoteDataSet['prices'] = []
                bricebreaks = row[9].strip('[] ')
                
                for pb in bricebreaks.split(', '):
                    pb = float(pb)
                    quoteDataSet['pricebreaks'].append(float(pb))
                    

                prices = row[10].strip('[] ')
                for price in prices.split(', '):
                    price = float(price)
                    quoteDataSet['prices'].append(float(price))
     
                quoteDataSet['mpn'] = row[5]
                quoteDataSet['node'] = ''
                quoteDataSet['manufacturer'] = row[6]
                quoteDataSet['supplier'] = row[1]
                quoteDataSet['checked'] = row[0]
                quoteDataSet['url'] = row[13]
                self.bomData[len(self.bomData)-1]['quotes'].append(quoteDataSet)
        self.doPricing();
        
    