'''
Created on 29.04.2015

@author: arne
'''
import unittest


class Test(unittest.TestCase):


    def testName(self):
        if 1:
            from digikey_api.core import Digikey_api
            digikey = Digikey_api('LT6220CS5#TRMPBF',1,0)
            page= digikey.getPage()
            result = digikey.parse()
            print(result)
        
        


if __package__ is None:
    from os import sys, path
    searchpath = path.abspath(path.join(path.dirname( __file__ ), '..\\..'))
    sys.path.append(searchpath)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()