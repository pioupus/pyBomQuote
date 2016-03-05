'''
Created on 29.04.2015

@author: arne
'''
import unittest


class Test(unittest.TestCase):


    def testSN74LS74AD(self):
        if 1:
            from digikey_octopart.core import Digikey_octo
            digikey = Digikey_octo('SN74LS74AD',1,0)
            page= digikey.getPage()
            #print page
            with open("SN74LS74AD.xml", "wb") as myfile:
                myfile.write(page)
            result = digikey.parse()
            print(result)

    def testLT6220CS5(self):
        if 1:
            from digikey_octopart.core import Digikey_octo
            digikey = Digikey_octo('LT6220CS5#TRMPBF',1,0)
            page= digikey.getPage()
            #print page
            with open("LT6220CS5.xml", "wb") as myfile:
                myfile.write(page)
            result = digikey.parse()
            print(result)
           

if __package__ is None:
    from os import sys, path
    searchpath = path.abspath(path.join(path.dirname( __file__ ), '..\\..'))
    sys.path.append(searchpath)
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()