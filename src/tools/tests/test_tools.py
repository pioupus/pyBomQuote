'''
Created on 26.04.2015

@author: arne
'''
import unittest


class Test(unittest.TestCase):


    def testOptPrices0(self):
        from tools.core import *
        pricebreak = [1.0, 25.0, 100.0, 250.0, 500.0, 2000.0, 5000.0, 20000.0] 
        pricelist = [0.119, 0.11, 0.104, 0.0968, 0.0917, 0.0817, 0.0806, 0.0723]
        qty = 57
        minVPE = 10
        result = getRealPrice(qty,minVPE,pricelist,pricebreak);
        self.assertEqual(result[0]['price'], 6.6)
        self.assertEqual(result[0]['qty'], 60)
        
        self.assertEqual(result[1]['price'], 10.4)
        self.assertEqual(result[1]['qty'], 100)
                
        print(result)

    def testOptPrices1(self):
        if 1:
            from tools.core import *
            pricebreak = [1.0] 
            pricelist = [0.5]
            qty = 1
            minVPE = 2
            result = getRealPrice(qty,minVPE,pricelist,pricebreak);
            self.assertEqual(result[0]['price'], 1)
            self.assertEqual(result[0]['qty'], 2)
            
            self.assertEqual(result[1]['price'], 1)
            self.assertEqual(result[1]['qty'], 2)
                    
            print(result)
        
    def testOptPrices3(self):
        if 1:
            from tools.core import *
            pricebreak = [10.0] 
            pricelist = [0.5]
            qty = 1
            minVPE = 2
            result = getRealPrice(qty,minVPE,pricelist,pricebreak);
            self.assertEqual(result[0]['price'], 5)
            self.assertEqual(result[0]['qty'], 10)
            
            self.assertEqual(result[1]['price'], 5)
            self.assertEqual(result[1]['qty'], 10)
                    
            print(result)        
            
    def testOptPrices4(self):
        if 1:
            from tools.core import *
            pricebreak = [1.0, 5, 10, 1000] 
            pricelist = [0.5,0.25,0.20,0.1]
            qty = 2000
            minVPE = 3
            result = getRealPrice(qty,minVPE,pricelist,pricebreak);
            self.assertEqual(result[0]['price'], 200.1)
            self.assertEqual(result[0]['qty'], 2001)
            
            self.assertEqual(result[1]['price'], 200.1)
            self.assertEqual(result[1]['qty'], 2001)
                    
            print(result)     

                    
            print(result)             
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()