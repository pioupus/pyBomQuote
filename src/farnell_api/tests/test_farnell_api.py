'''
Created on 29.04.2015

@author: arne
'''
import unittest


class Test(unittest.TestCase):


    def testName(self):
        if 0:
            from farnell_api.core import Farnell_api
            farnell = Farnell_api('MC0402B104K160CT',1,0)
            page= farnell.getPage()
            with open("farnell_MC0402B104K160CT.xml", "wb") as myfile:
                myfile.write(page)
            result = farnell.parse()
            print(result)
        
        
    def test_ausUSA(self):
        if 0:
            from farnell_api.core import Farnell_api
            farnell = Farnell_api('TNPW0805101KBETA',1,0)
            page= farnell.getPage()
            with open("farnell_TNPW0805101KBETA.xml", "wb") as myfile:
                myfile.write(page)
            result = farnell.parse()
            print(result)
            
    def testVero(self):
        if 0:
            from farnell_api.core import Farnell_api
            farnell = Farnell_api('8731128',1,0)
            page= farnell.getPage()
            with open("farnell_8731128.xml", "wb") as myfile:
                myfile.write(page)
            result = farnell.parse()
            print(result)
            
    def testLT6220CS5_TRMPBF(self):
        if 1:
            from farnell_api.core import Farnell_api
            farnell = Farnell_api('LT6220CS5#TRMPBF',1,0)
            page= farnell.getPage()
            with open("farnell_LT6220CS5_TRMPBF.xml", "wb") as myfile:
                myfile.write(page)
            result = farnell.parse()
            print(result)            

if __package__ is None:
    from os import sys, path
    searchpath = path.abspath(path.join(path.dirname( __file__ ), '..\\..'))
    sys.path.append(searchpath)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()