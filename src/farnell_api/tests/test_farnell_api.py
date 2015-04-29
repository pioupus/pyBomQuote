'''
Created on 29.04.2015

@author: arne
'''
import unittest


class Test(unittest.TestCase):


    def testName(self):
        from farnell_api.core import Farnell_api
        farnell = Farnell_api('MC0402B104K160CT',1,0)
        page= farnell.getPage()
        with open("farnell_MC0402B104K160CT.xml", "wb") as myfile:
            myfile.write(page)
        farnell.parse()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()