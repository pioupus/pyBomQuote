'''
Created on 29.04.2015

@author: arne
'''
import unittest


class Test(unittest.TestCase):


    def testName(self):
        if 0:
            from mouser_api.core import Mouser_api
            mouser = Mouser_api('RC0402FR-071M2L',1,0)
            page= mouser.getPage()
           # with open("farnell_MC0402B104K160CT.xml", "wb") as myfile:
           #     myfile.write(page)
            result = mouser.parse()
            print(result)
            
    def testName1(self):
        if 1:
            from mouser_api.core import Mouser_api
            mouser = Mouser_api('PESD5V0L4UW',1,0)
            page= mouser.getPage()
           # with open("farnell_MC0402B104K160CT.xml", "wb") as myfile:
           #     myfile.write(page)
            result = mouser.parse()
            print(result)  
            
    def testName2(self):
        if 0:
            from mouser_api.core import Mouser_api
            mouser = Mouser_api('BAT60AE6327',1,0)
            page= mouser.getPage()
           # with open("farnell_MC0402B104K160CT.xml", "wb") as myfile:
           #     myfile.write(page)
            result = mouser.parse()
            print(result)    
             
    def testName3(self):
        if 0:
            from mouser_api.core import Mouser_api
            mouser = Mouser_api('1PS79SB30,115',1,0)
            page= mouser.getPage()
           # with open("farnell_MC0402B104K160CT.xml", "wb") as myfile:
           #     myfile.write(page)
            result = mouser.parse()
            print(result)

          
        
    


if __package__ is None:
    from os import sys, path
    searchpath = path.abspath(path.join(path.dirname( __file__ ), '..\\..'))
    sys.path.append(searchpath)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()