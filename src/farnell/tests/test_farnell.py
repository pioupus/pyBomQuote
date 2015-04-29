#!/usr/bin/env python

'''
Created on 15.04.2015

@author: arne
'''
import unittest
import urllib2

class Test(unittest.TestCase):


    def test_downloadPage(self):
        if 1:
            from farnell.core import Farnell
            farnell = Farnell("GRM188R61H105KAALD",1,0)

            #self.page = farnell.getPage()
            #with open("farnell_nicht_USA.xml", "ab") as myfile:
            #    myfile.write(self.page)
            result = farnell.parse()
            #self.assertEqual(result['minVPE'], [10, 150])
            #self.assertEqual(result['stock'], ['14308', '14308'] )
            #self.assertEqual(result['supplier'], ['Farnell','Farnell'])
            #self.assertEqual(result['mpn'], ['GRM188R61H105KAALD', 'GRM188R61H105KAALD'])            
            #self.assertEqual(result['ausUSA'], [0,0])
            #self.assertEqual(result['ordercode'], ['1845736', '1845736RL'])
            #self.assertEqual(result['prices'], [[0.16, 0.112, 0.097, 0.086], [0.097, 0.086, 0.079]])
            #self.assertEqual(result['pricebreaks'], [[10.0, 50.0, 100.0, 500.0], [100.0, 500.0, 1000.0]])

    def test_downloadPageUSABestand(self):
        if 1:
            from farnell.core import Farnell
            farnell = Farnell("TNPW0805101KBETA",1,0)
            #self.page = farnell.getPage()
            #with open("farnell_aus_usa.xml", "ab") as myfile:
            #    myfile.write(self.page)
            result = farnell.parse()  
            #self.assertEqual(len(result['ausUSA']), 2)
            #self.assertEqual(result['minVPE'], [1, 5000])
            #self.assertEqual(result['stock'], ['3583', '10000'] )
            #self.assertEqual(result['supplier'], ['Farnell','Farnell'])
            #self.assertEqual(result['mpn'], ['TNPW0805101KBETA','TNPW0805101KBETA'])            
            #self.assertEqual(result['ausUSA'], [1,1])
            #self.assertEqual(result['ordercode'], ['1872050','2371656'])
            #self.assertEqual(len(result['prices']), 2)
            #self.assertEqual(len(result['pricebreaks']), len(result['prices']))
            #self.assertEqual(result['prices'], [[0.6], [0.6]])
            #self.assertEqual(result['pricebreaks'], [[1.0], [5000.0]])

              
    def test_downloadDetailPage(self):
        if 1:
            from farnell.core import Farnell
            farnell = Farnell("1653195",1,0)
            #self.page = farnell.getPage()
            #with open("farnell_einfach_nicht_usa.xml", "ab") as myfile:
            #    myfile.write(self.page)
            result = farnell.parse()  
            self.assertEqual(len(result['ausUSA']), 1)
            self.assertEqual(result['minVPE'][0], 1)
            self.assertEqual(result['stock'][0], '7698' )
            self.assertEqual(result['supplier'][0], 'Farnell')
            self.assertEqual(result['mpn'][0], 'CRCW20101K20FKEF')            
            self.assertEqual(result['ausUSA'][0], 0)
            self.assertEqual(result['ordercode'][0], '1653195')
            self.assertEqual(len(result['prices'][0]), 5)
            self.assertEqual(len(result['pricebreaks'][0]), len(result['prices'][0]))
            self.assertEqual(result['prices'][0][0], 0.138)
            self.assertEqual(result['pricebreaks'][0][0], 1.0)
            
            self.assertEqual(result['prices'][0][1], 0.122)
            self.assertEqual(result['pricebreaks'][0][1], 25)
            
            self.assertEqual(result['prices'][0][4], 0.0363)
            self.assertEqual(result['pricebreaks'][0][4], 500)
                        

        
    def test_downloadDetailPageUSABestand(self):
        if 1:
            from farnell.core import Farnell
            farnell = Farnell("1872050",1,0)
            #self.page = farnell.getPage()
            #with open("farnell_einfach_usa.xml", "ab") as myfile:
            #    myfile.write(self.page)
            print farnell.getUrl()
            result = farnell.parse()  
            self.assertEqual(len(result['ausUSA']), 1, '')
            self.assertEqual(result['ausUSA'][0], 1, '')
            self.assertEqual(result['ordercode'][0], '1872050', '')
            self.assertEqual(result['prices'][0][0], 0.6, '')
            self.assertEqual(result['pricebreaks'][0][0], 1.0, '')
            self.assertEqual(result['minVPE'][0], 1, '')
            self.assertEqual(result['stock'][0], '3583', '')
            self.assertEqual(result['supplier'][0], 'Farnell', '')
            self.assertEqual(result['mpn'][0], 'TNPW0805101KBETA', '')
        
    def test_downloadDetailABI(self):
        if 1:
            from farnell.core import Farnell
            farnell = Farnell("ABI-042-RC",1,0)
            print farnell.getUrl()
            #self.page = farnell.getPage()
            #with open("farnell_ABI-042-RC.xml", "ab") as myfile:
            #    myfile.write(self.page)
            result = farnell.parse()  
            self.assertEqual(result['minVPE'], [1])
            self.assertEqual(result['stock'], ['674'] )
            self.assertEqual(result['supplier'], ['Farnell'])
            self.assertEqual(result['mpn'], ['ABI-042-RC'])            
            self.assertEqual(result['ausUSA'], [0])
            self.assertEqual(result['ordercode'], ['1827949'])
            self.assertEqual(result['prices'], [[2.39, 2.2, 2.1, 2.0]])
            self.assertEqual(result['pricebreaks'], [[1.0, 10.0, 50.0, 100.0]])  
    
    def test_downloadDetailC1608X5R0J106M(self):
        if 1:
            from farnell.core import Farnell
            farnell = Farnell("C1608X5R0J106M%2BTDK",1,0)
            #self.page = farnell.getPage()
            #with open("farnell_ABI-042-RC.xml", "ab") as myfile:
            #    myfile.write(self.page)
            result = farnell.parse()  
            self.assertEqual(result['minVPE'], [0])
            self.assertEqual(result['stock'], ['Wirdnichtmehrhergestellt'] )
            self.assertEqual(result['supplier'], ['Farnell'])
            self.assertEqual(result['mpn'], ['C1608X5R0J106M'])            
            self.assertEqual(result['ausUSA'], [0])
            self.assertEqual(result['ordercode'], ['2112705'])
            self.assertEqual(result['prices'], [[0.107, 0.092, 0.075, 0.063, 0.051]])
            self.assertEqual(result['pricebreaks'], [[1.0, 250.0, 500.0, 1000.0, 5000.0]])   
            
    def test_downloadDetail20_2136_Vero(self):
        if 1:
            from farnell.core import Farnell
            farnell = Farnell("20-2136 Vero",1,0)
            print farnell.getUrl()
            #self.page = farnell.getPage()
            #with open("20-2136.xml", "ab") as myfile:
            #    myfile.write(self.page)
            result = farnell.parse()  
            self.assertEqual(result['minVPE'], [1])
            self.assertEqual(result['stock'], ['1445'] )
            self.assertEqual(result['supplier'], ['Farnell'])
            self.assertEqual(result['mpn'], ['20-2136'])            
            self.assertEqual(result['ausUSA'], [0])
            self.assertEqual(result['ordercode'], ['8731195'])
            self.assertEqual(result['prices'], [[21.47, 16.95, 12.58, 10.9]])
            self.assertEqual(result['pricebreaks'], [[1.0, 5.0, 10.0, 50.0]])                  
    
    def test_downloadDetail_FT230XS(self):
        if 1:
            from farnell.core import Farnell
            farnell = Farnell("FT230XS",1,0)
            self.page = farnell.getPage()
            with open("farnell_FT230XS.xml", "ab") as myfile:
                myfile.write(self.page)
            result = farnell.parse()  
            #print result
            if 1:
                self.assertEqual(result['minVPE'], [1])
                self.assertEqual(result['stock'], ['Lieferungwirderwartet'] )
                self.assertEqual(result['supplier'], ['Farnell'])
                self.assertEqual(result['mpn'], ['FT230XS'])            
                self.assertEqual(result['manufacturer'], ['FTDI'])
                self.assertEqual(result['ausUSA'], [0])
                self.assertEqual(result['ordercode'], ['2081321'])
                self.assertEqual(result['prices'], [[1.9, 1.83, 1.76, 1.3]])
                self.assertEqual(result['pricebreaks'], [[1.0, 25.0, 100.0, 1000.0]])  
                
    def test_downloadDetail_MCP4921_E_MS(self):
        if 1:
            from farnell.core import Farnell
            farnell = Farnell("MCP4921-E/MS",1,0)
            self.page = farnell.getPage()
            with open("farnell_MCP4921_E_MS.xml", "ab") as myfile:
                myfile.write(self.page)
            result = farnell.parse()  
            #print result
            if 1:
                self.assertEqual(result['minVPE'], [1])
                self.assertEqual(result['stock'], ['Lieferungwirderwartet'] )
                self.assertEqual(result['supplier'], ['Farnell'])
                self.assertEqual(result['mpn'], ['MCP4921-E/MS'])            
                self.assertEqual(result['manufacturer'], ['MICROCHIP'])
                self.assertEqual(result['ausUSA'], [0])
                self.assertEqual(result['ordercode'], ['1834916'])
                self.assertEqual(result['prices'], [[1.92, 1.47, 1.38]])
                self.assertEqual(result['pricebreaks'], [[1.0, 10.0, 100.0]])       
                
    def test_downloadDetail_744028220(self):
        if 1:
            from farnell.core import Farnell
            farnell = Farnell("744028220 W\xc3rth",1,0)
            self.page = farnell.getPage()
            print farnell.getUrl()
            with open("farnell_744028220.xml", "ab") as myfile:
                myfile.write(self.page)
            result = farnell.parse()  
            print result
            if 0:
                self.assertEqual(result['minVPE'], [1])
                self.assertEqual(result['stock'], ['Lieferungwirderwartet'] )
                self.assertEqual(result['supplier'], ['Farnell'])
                self.assertEqual(result['mpn'], ['MCP4921-E/MS'])            
                self.assertEqual(result['manufacturer'], ['MICROCHIP'])
                self.assertEqual(result['ausUSA'], [0])
                self.assertEqual(result['ordercode'], ['1834916'])
                self.assertEqual(result['prices'], [[1.92, 1.47, 1.38]])
                self.assertEqual(result['pricebreaks'], [[1.0, 10.0, 100.0]])                   
        
if __package__ is None:
    from os import sys, path
    searchpath = path.abspath(path.join(path.dirname( __file__ ), '..\\..'))
    sys.path.append(searchpath)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    print("start")
    unittest.main() 