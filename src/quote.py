#!/usr/bin/env python
 
from rs.core import Rs 
from farnell.core import Farnell
import math

#from PySide.QtCore import *
#from PySide.QtGui import *
#from PySide.QtDeclarative import *
import csv 

excludeRLOrderNumbers = 1;
maxMinVPE = 100;


def getTotalPrice(qty,pricelist,pricebreak):
    #pricebreak =[2,3,20]
    #pricelist =[0.5,0.3,0.25]
    pindex = 0;
    priceresult = {'firstprice':[0.0,0.0],'secprice':[0.0,0.0]}
    if not qty.isdigit():
        return priceresult
    else:
        qty = float(qty)
        #print qty
        for pbreak in pricebreak:
        #print pbreak
            if float(qty) < pbreak:
                break;
            pindex = pindex+1;
        if pindex == 0:
            pindex =1;
        print pricebreak;
        print qty;
        pb = pricebreak[pindex-1]
        if isinstance(pb, basestring):
            if pb.isdigit():
                pb = int(pb)
            
        corrqty = pb/pricebreak[pindex-1]
        corrqty = math.ceil(corrqty)*pricebreak[pindex-1]
        #print corrqty
        firsttotalprice = pricelist[pindex-1]*corrqty
    
        priceresult['firstprice'] = [corrqty,round(firsttotalprice,2)]
        priceresult['secprice'] = priceresult['firstprice']
      # print 'firstprice '+str(firsttotalprice)
        if len(pricebreak) > pindex:
            secondtotalprice = pricelist[pindex]*pricebreak[pindex]
            priceresult['secprice'] = [pricebreak[pindex],round(secondtotalprice,2)]
        
    
        #print pricelist
        #print pricebreak
        #print priceresult
    return priceresult
    
csvreader = csv.reader(open("bomtest1.csv", "rb"), delimiter="|")

csvwriter = csv.writer(open("bomquote.csv", "wb"), delimiter="|" , quotechar='"', quoting=csv.QUOTE_ALL)
intable = []

for row in csvreader: 
    intableItem = {'qty':[],'designator':[],'mpn':[],'manufacturer':[],'description':[],'libID':[]}
    intableItem['qty']=row[1]
    intableItem['designator'] = row[2]
    intableItem['mpn'] = row[3]
    if row[3] == '':
        intableItem['mpn'] = row[5]
    intableItem['manufacturer'] = row[4]
    intableItem['libID'] = row[5]
    intableItem['description'] = row[7]
    intable.append(intableItem)
  
#print intable     

result=[]




#rsParser.doRSQuote('0034.1506',1,1);

  #result['ordercode']
  #result['manufacturer']
  #result['mpn']
  #result['description'],
  #result['stock'],  -1 wenn nicht ermittelbar
  #result['pricebreaks']
  #result['prices']
  #result['minVPE'] -1 wenn fehler zb Nicht mehr auf Lager
  #result['ausUSA'] immer 0
  #result['URL']
  #result['supplier']=Farnell
  
#result = farnellParser.doFarnellQuote('1384631',0,0);
#result = rsParser.doRSQuote('0034.1506',0,0); 
#print result
def doQuote():
    cnt = 0;
    #exit();
    if 1:
        for intableItem in intable:
            cnt = cnt+1;
            if cnt == 1:
                continue
    
            print str(cnt) + ' of '+str(len(intable))
            print intableItem['mpn']
            row = []
            row.append('orig')
            row.append(intableItem['qty'])
            row.append(intableItem['designator'])
            row.append(intableItem['mpn'])
            row.append(intableItem['manufacturer'])
            row.append(intableItem['description'])
            csvwriter.writerow(row)
            if 1:
                rs = Rs(intableItem['mpn'],1,0)
                result = rs.parse() 
                #result = rsParser.doRSQuote(intableItem['mpn'],1,1);
        
                for i in range(len(result['ordercode'])):
                    #print i
                    #print len(result['ordercode'])
                    #print result
                    row = []
                    row.append('0')
                    row.append('RS')
                    price1total = []
                    price1total = getTotalPrice(intableItem['qty'],result['prices'][i],result['pricebreaks'][i])
                    #print price1total
                    if price1total['firstprice'][1] < price1total['secprice'][1]:
                        row.append(price1total['firstprice'][0])
                        row.append(price1total['firstprice'][1])
                    else:
                        row.append(price1total['secprice'][0])
                        row.append(price1total['secprice'][1])    
                    row.append(result['ordercode'][i])
                    row.append(result['mpn'][i])
                    row.append(result['manufacturer'][i])
                    row.append(result['description'][i])
                    row.append(result['minVPE'][i])
                    row.append(result['pricebreaks'][i])
                    row.append(result['prices'][i])
                    row.append(result['stock'][i])
                    if result['ausUSA'][i]:
                        row.append('ausUSA')
                    else:
                        row.append('nichtAusUSA')
                    row.append(result['URL'][i])
                    csvwriter.writerow(row)    
            if 1:
                farnell = Farnell(intableItem['mpn'],1,0)
                result = farnell.parse()
                if result['ausUSA']==[-1]:
                    farnell = Farnell(intableItem['mpn']+'+'+intableItem['manufacturer'],1,0)
                    result = farnell.parse()                
                for i in range(len(result['ordercode'])):
                    addLine=0; 
                    if excludeRLOrderNumbers == 0:
                        addLine=1;
                    else:
                        #print result['ordercode'][i].find('RL')
                        if (result['ordercode'][i].find('RL') == -1):
                            addLine=1;
                    if maxMinVPE <= result['minVPE'][i]:
                        addLine = 0
                    if addLine:
                        row = []
                        row.append('0')
                        row.append('Farnell')
              
                        price1total = getTotalPrice(intableItem['qty'],result['prices'][i],result['pricebreaks'][i])
                        if price1total['firstprice'][1] < price1total['secprice'][1]:
                            row.append(price1total['firstprice'][0])
                            row.append(price1total['firstprice'][1])
                        else:
                            row.append(price1total['secprice'][0])
                            row.append(price1total['secprice'][1])
                        row.append(result['ordercode'][i])
                        row.append(result['mpn'][i])
                        row.append(result['manufacturer'][i])
                        row.append(result['description'][i])
                        row.append(result['minVPE'][i])
                        row.append(result['pricebreaks'][i])
                        row.append(result['prices'][i])
                        row.append(result['stock'][i])
                        #if cnt > 5:
                        #  exit()
                        if result['ausUSA'][i]:
                            row.append('ausUSA')
                        else:
                            row.append('nichtAusUSA')
                        row.append(result['URL'][i])
                        csvwriter.writerow(row)    
          
    
    
    print result
    ##print result[1]