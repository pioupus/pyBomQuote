'''
Created on 26.04.2015

@author: arne
'''
import math
import sys

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
    