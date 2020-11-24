#!/usr/bin/env python

from rs.core import Rs 
from farnell_api.core import Farnell_api
from digikey_api.core import Digikey_api
from mouser_api.core import Mouser_api
import math



import csv 

class ProgressWriter():
    def __init__(self):
        pass

    def printMsg(self,msg):
        print(msg)
        
    def setProgress(self,progress,total):
        print(str(progress)+' of '+str(total))

class Quote():
    def __init__(self, csvPath=None, csvDelimiter = '|', progressWriter=None):
        self.csvPath = csvPath
        self.progressWriter = progressWriter
        self.intable = []
        self.excludeRLOrderNumbers = 1;
        self.maxMinVPE = 300
        csvreader = csv.reader(open(self.csvPath, "r"), delimiter=csvDelimiter)
        for row in csvreader: 
            intableItem = {'qty':[],'designator':[],'mpn':[],'manufacturer':[],'description':[],'libID':[]}
            intableItem['qty']=row[1]
            intableItem['designator'] = row[2]
            intableItem['mpn'] = row[3]
            if row[3] == '':
                intableItem['mpn'] = row[5]
            intableItem['manufacturer'] = row[4]
            intableItem['libID'] = row[5]
            intableItem['footprint'] = row[6]
            intableItem['description'] = row[7]
            self.intable.append(intableItem)
        
    def doQuote(self,writePath):
        cnt = 0;
        #exit();
        if 1:
            csvwriter = csv.writer(open(writePath, "w",  newline='', encoding='utf-8'), delimiter="|" , quotechar='"', quoting=csv.QUOTE_ALL)
            for intableItem in self.intable:
                #print(intableItem)
                cnt = cnt+1;
                if cnt < 0:
                    continue
                self.progressWriter.printMsg(intableItem['mpn'])
                self.progressWriter.setProgress(cnt,len(self.intable))
                #print str(cnt) + ' of '+str(len(self.intable))
                row = []
                row.append('0')
                row.append('orig')
                row.append(intableItem['qty'])
                row.append(intableItem['designator'])
                row.append(intableItem['mpn'])
                row.append(intableItem['manufacturer'])
                row.append(intableItem['description'])
                row.append(intableItem['footprint'])
                csvwriter.writerow(row)
                if 0:
                    rs = Rs(intableItem['mpn'],1,0)
                    self.progressWriter.printMsg(rs.getUrl())
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
                        row.append(result['pku'][i])
                        row.append(result['URL'][i])
                        csvwriter.writerow(row)    
                if 1:
                    farnell_api = Farnell_api(intableItem['mpn'],1,0)
                    self.progressWriter.printMsg(farnell_api.getUrl())
                    result = farnell_api.parse()
                    #if result['ausUSA']==[-1]:
                    #    farnell_api = farnell_api(intableItem['mpn']+'+'+intableItem['manufacturer'],1,0)
                    #    result = farnell_api.parse()   
                    
                    for i in range(len(result['ordercode'])):
                        addLine=0; 
                        #print(result['ordercode'][i])
                        if self.excludeRLOrderNumbers == 0:
                            addLine=1;
                        else:
                            #print(result['ordercode'])
                            #print(i)
                            #print(result['ordercode'][i])
                            if (str(result['ordercode'][i]).find('RL') == -1):
                                addLine=1;
                            else:
                                pass
                        if self.maxMinVPE <= int(result['minVPE'][i]):
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
                            row.append(result['pku'][i])
                            row.append(result['URL'][i])
                            csvwriter.writerow(row)    
                if 1:
                    digikey__api = Digikey_api(intableItem['mpn'],1,0)
                    self.progressWriter.printMsg(digikey__api.getUrl())
                    result = digikey__api.parse()
                    #if result['ausUSA']==[-1]:
                    #    farnell_api = farnell_api(intableItem['mpn']+'+'+intableItem['manufacturer'],1,0)
                    #    result = farnell_api.parse()   
                    
                    for i in range(len(result['ordercode'])):
                        addLine=1; 
 
                        if (str(result['stock'][i]).find('Reel') == -1):
                            addLine=1;
                        else:
                            addLine=0;
                        
                        if self.maxMinVPE <= int(result['minVPE'][i]):
                            addLine = 0

                        if addLine:
                            row = []
                            row.append('0')
                            row.append('DigiKey')
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
                            row.append(result['pku'][i])
                            row.append(result['URL'][i])
                            csvwriter.writerow(row)     
                if 1:
                    mouser_api = Mouser_api(intableItem['mpn'],1,0)
                    self.progressWriter.printMsg(mouser_api.getUrl())
                    result = mouser_api.parse()
                    #if result['ausUSA']==[-1]:
                    #    farnell_api = farnell_api(intableItem['mpn']+'+'+intableItem['manufacturer'],1,0)
                    #    result = farnell_api.parse()   
                    
                    for i in range(len(result['ordercode'])):
                        addLine=1; 
 
                        if (str(result['stock'][i]).find('Reel') == -1):
                            addLine=1;
                        else:
                            addLine=0;
                        
                        if self.maxMinVPE <= int(result['minVPE'][i]):
                            addLine = 0

                        if addLine:
                            row = []
                            row.append('0')
                            row.append('Mouser')
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
                            row.append(result['pku'][i])
                            row.append(result['URL'][i])
                            csvwriter.writerow(row)    							


        
        
#quote = Quote("..\\boms\\funksonde2\\sg04_btmodul\\bom.txt")
#quote.doQuote('..\\boms\\funksonde2\\sg04_btmodul\\bom_test.bomQuote')