#!/usr/bin/env python
 
from rs.core import Rs 
from farnell.core import Farnell
import math

import csv 

excludeRLOrderNumbers = 1;
maxMinVPE = 300

def doQuote(intable):
    cnt = 0;
    #exit();
    if 1:
        for intableItem in intable:
            #print(intableItem)
            cnt = cnt+1;
            if cnt < 67:
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
                    row.append(0)
                    row.append(0)    
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
                #if result['ausUSA']==[-1]:
                #    farnell = Farnell(intableItem['mpn']+'+'+intableItem['manufacturer'],1,0)
                #    result = farnell.parse()                
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
                        row.append(0) 
                        row.append(0)
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
        
    
    
    ##print result[1]
csvreader = csv.reader(open("..\\boms\\funksonde2\\sg04_btmodul\\bom.txt", "rb"), delimiter="|")

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

doQuote(intable)