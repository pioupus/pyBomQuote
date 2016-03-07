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

def getPriceWithoutOptimization(qty,pricelist,pricebreaks):
    pindex = 0
    for pb in pricebreaks: 
        if float(qty) < pb:
            break;
        pindex = pindex+1;
    if pindex == 0:
        pindex =1;
    price = pricelist[pindex-1]
    return qty*price
    
def getRealPrice(qtyOrig,minVPE,pricelist,pricebreaks,pku):
    #pricebreak =[2,3,20]
    #pricelist =[0.5,0.3,0.25]
    pindex = 0;
    realPrice = [{'price':0,'qty':1},{'price':0,'qty':1}]

    if 1:
        qtyOrig = float(qtyOrig)
        minVPE = float(minVPE)

            
        qty = math.ceil(qtyOrig/minVPE)
        qty = qty*minVPE
        qty = math.ceil(qty/pku)        
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

def quotesEqual(a,b):
    result = 1;
    if len(a) == len(b):
        for index,elementA in enumerate(a):
            if len(elementA) == len(b[index]):
                for index_inner,elementA_inner in elementA.iteritems():
                    if index_inner == 'node':
                        continue
                    if index_inner == 'opt_price':
                        continue                    
                    if index_inner == 'opt_qty':
                        continue   
                    if index_inner == 'stock':
                        continue                       
                    if index_inner == 'description':
                        continue                         
                    #print(str(index_inner)+': '+str(elementA[index_inner])+' = '+str(b[index][index_inner]))
                    if elementA[index_inner] != b[index][index_inner]:
                        print('Quote #'+str(index)+' / field '+str(index_inner)+' is Unequal. A: "'+str(elementA[index_inner])+'" != B: "'+ str(b[index][index_inner])+'"')
                        result = 0
            else:
                result = 0
                break
    else:
        result = 0
    return result;
    

class BOMQuoteData():
    def __init__(self, csvPath=None, parent=None):
        self.bomData = []
        if csvPath is not None:
            self.loadFromCSV(csvPath)
            
    
    def getBomData(self):
        return self.bomData
    
    def clear(self):
        self.bomData = []

    def mergeDuplicates(self):
        newList = []
        unequalQuotes = [[],[]]
        if 0:
            for bom in self.bomData:
                print('MPN: '+bom['mpn']) 
                print('menge: '+str(bom['menge'])) 
                print('ref: '+bom['ref']) 
                print('')
                
        for bomAIndex, bomA in enumerate(self.bomData):  
            #print('Menge '+str(bomA['menge']))
            newQty = int(bomA['menge'])
            if newQty == 0:
                #print('skipped')
                continue
            newRefs = bomA['ref']
            
            #print('BomA: '+bomA['mpn'])
            
            for bomB in self.bomData[bomAIndex+1:]:
                qty = int(bomB['menge'])
                if qty > 0:
                    #print('BomB: '+bomB['mpn'])
                    if (bomA['mpn'] == bomB['mpn']) and (bomA['manufacturer'] == bomB['manufacturer']):
                        #print('found duplicate at '+bomB['mpn'])
                        if quotesEqual(bomA['quotes'],bomB['quotes']) == 0:
                            print('but unequal quotes..')
                            print(bomB)
                            print(bomA)
                            unequalQuotes[0].append(bomB)
                            unequalQuotes[1].append(bomA)
                        else:
                            newQty += qty
                            newRefs += ', '+bomB['ref']
                            bomB['menge'] = 0
                    
            bomA['menge'] = newQty
            bomA['ref'] = newRefs
            newList.append(bomA)
        self.bomData = newList
        
        if 0:
            for bom in self.bomData:
                print('MPN: '+bom['mpn']) 
                print('menge: '+str(bom['menge'])) 
                print('ref: '+bom['ref']) 
                print('')
                
            for i,quote in enumerate(unequalQuotes[0]):
                print(quote)
                print(unequalQuotes[1][i])
        return unequalQuotes
        
    def multiplyQuantity(self, factor):
        for bom in self.bomData:        
            qty = bom['menge']
            qty = qty*factor
            bom['menge'] = qty
        self.doPricing()

    def addQtyToCheapParts(self, qtyToAdd,priceThreshold):
        for bom in self.bomData: 
            cheapestQuote = sys.float_info.max
            for quote in bom['quotes']:
                if len(quote['pricebreaks'])>0:
                    if float(quote['pricebreaks'][0]) < cheapestQuote:
                        cheapestQuote = float(quote['pricebreaks'][0])    
                        
            if cheapestQuote <= priceThreshold:
                qty = bom['menge']
                qty = qty+qtyToAdd
                bom['menge'] = qty
                
        self.doPricing()
            
    def doPricing(self):
        for bom in self.bomData:
            qty = bom['menge'];
            for quote in bom['quotes']:
                pb = quote['pricebreaks']
                prices = quote['prices']
                minVPE = quote['minVPE']
                pku = int(quote['pku'])
                realPrice = getRealPrice(qty,minVPE,prices,pb,pku );
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
                sku = row[4]
                supplier = row[1]
                if supplier.lower() == 'rs' and 'P' in sku:
                    continue
                quoteDataSet={}
                quoteDataSet['sku'] = sku
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
                quoteDataSet['pku'] = row[13]
                quoteDataSet['pricebreaks'] = []
                quoteDataSet['prices'] = []
                bricebreaks = row[9].strip('[] ')
                print ('PKU: '+ quoteDataSet['sku']);
                for pb in bricebreaks.split(', '):
<<<<<<< HEAD
                    #print pb
=======
                    print sku +' "'+str(pb)+'"'
>>>>>>> 37dc8b37ed02b0710e4c57d9c1aa3e910dc36684
                    pb = float(pb)
                    quoteDataSet['pricebreaks'].append(float(pb))

                prices = row[10].strip('[] ')
                for price in prices.split(', '):
                    price = float(price)
                    quoteDataSet['prices'].append(float(price))
     
                quoteDataSet['mpn'] = row[5]
                quoteDataSet['node'] = ''
                quoteDataSet['manufacturer'] = row[6]
                quoteDataSet['supplier'] = supplier
                quoteDataSet['checked'] = row[0]
                quoteDataSet['url'] = row[14]
                self.bomData[len(self.bomData)-1]['quotes'].append(quoteDataSet)
        self.doPricing();
        
    