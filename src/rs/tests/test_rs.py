'''
Created on 20.04.2015

@author: arne
'''
import unittest


class Test(unittest.TestCase):

   # def testSinglePage(self):
    #    from rs.core import Rs
     #   rs = Rs("GRM188R61H105KAALD",1,0)
      #  self.assertFalse('Foo'.isupper())
       # self.page = rs.getPage()
        #with open("rs_auswahlliste.xml", "ab") as myfile:
        #    myfile.write(self.page)
        #rs.parse()
        
    #def testMultipleResults(self):
    #    from rs.core import Rs
    #    rs = Rs("GRM188R61A",1,0)
    #    self.page = rs.getPage()
    #    with open("rs_mulresults.xml", "ab") as myfile:
    #        myfile.write(self.page)
    #    rs.parse()        
        
    def testSinglePage_nichtlieferbar(self):
        if 1:
            from rs.core import Rs
            rs = Rs("815-1361",1,0)
            self.page = rs.getPage()
            with open("rs_singleresult_nichtlieferbar.xml", "ab") as myfile:
                myfile.write(self.page)
            rs.parse() 

    def testSinglePage_24AA16T_I_OT(self):
        if 1:
            from rs.core import Rs
            rs = Rs("24AA16T-I/OT",1,0)
            self.page = rs.getPage()
            with open("rs_24AA16T_I_OT.xml", "ab") as myfile:
                myfile.write(self.page)
            rs.parse() 
        
    def testSinglePage_ERJ3EKF2001V(self):
        if 1:
            from rs.core import Rs
            rs = Rs("ERJ3EKF2001V",1,0)
            self.page = rs.getPage()
            with open("rs_ERJ3EKF2001V.xml", "ab") as myfile:
                myfile.write(self.page)
            rs.parse()      
            
    def testSinglePage_702_002_10_00(self):
        if 1:
            from rs.core import Rs
            rs = Rs("702-002-10-00",1,0)
            self.page = rs.getPage()
            with open("rs_702-002-10-00.xml", "ab") as myfile:
                myfile.write(self.page)
            rs.parse()           

    def testSinglePage_FSM4JSMA(self):
        if 1:
            from rs.core import Rs
            rs = Rs("FSM4JSMA",1,0)
            self.page = rs.getPage()
            with open("FSM4JSMA.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse()    
            self.assertEqual(result['minVPE'], [5,1])
            self.assertEqual(result['stock'], [-1, -1] )
            self.assertEqual(result['supplier'], ['RS','RS'])
            self.assertEqual(result['mpn'], ['FSM4JSMATR','FSM4JSMA'])            
            self.assertEqual(result['ausUSA'], [0,0])
            self.assertEqual(result['ordercode'],  ['718-2455','875-0598'])
            self.assertEqual(result['prices'], [[0.322], [3256.99]])
            self.assertEqual(result['pricebreaks'], [[5],[1]])
            self.assertEqual(result['manufacturer'],  ['TE Connectivity','TE Connectivity'])
            
    def testSinglePage_T491B476K010A(self):
        if 1:
            from rs.core import Rs
            rs = Rs("T491B476K010A",1,0)
            self.page = rs.getPage()
            with open("rs_T491B476K010A.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse()   
            self.assertEqual(result['minVPE'], ['10'])
            self.assertIn('Lieferbar' , result['stock'][0])
            self.assertEqual(result['supplier'], ['RS'])
            self.assertEqual(result['mpn'], ['T491B476K010AT'])            
            self.assertEqual(result['ausUSA'], [0])
            self.assertEqual(result['ordercode'],  ['648-0597'])
            self.assertEqual(result['prices'], [[0.796, 0.631]])
            self.assertEqual(result['pricebreaks'], [[10, 50]])
            self.assertEqual(result['manufacturer'],  ['KEMET'])
            

    def testSinglePage_LIS331DLH(self):
        if 1:
            from rs.core import Rs
            rs = Rs("LIS331DLH",1,0)
            self.page = rs.getPage()
            with open("rs_LIS331DLH.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse()   
            #print result
            self.assertEqual(result['minVPE'], [1, 1])
            self.assertEqual(result['stock'], [-1, -1] )
            self.assertEqual(result['supplier'], ['RS', 'RS'])
            self.assertEqual(result['mpn'], ['LIS331DLH', 'STEVAL-MKI089V1'])            
            self.assertEqual(result['ausUSA'], [0,0])
            self.assertEqual(result['ordercode'],  ['714-7910', '717-3751'])
            self.assertEqual(result['prices'], [[2.4], [24.69]])
            self.assertEqual(result['pricebreaks'], [[1], [1]])
            self.assertEqual(result['manufacturer'],  ['STMicroelectronics', 'STMicroelectronics'])

    def testSinglePage_572_0500(self):
        if 1:
            from rs.core import Rs
            rs = Rs("572-0500",1,0)
            self.page = rs.getPage()
            with open("rs_572_0500.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse()   
            #print result
            self.assertEqual(result['minVPE'], [5, 1])
            self.assertEqual(result['stock'], [-1, -1] )
            self.assertEqual(result['supplier'], ['RS', 'RS'])
            self.assertEqual(result['mpn'], ['-', '-'])            
            self.assertEqual(result['ausUSA'], [0,0])
            self.assertEqual(result['ordercode'],  ['103-6555', '381-4745'])
            self.assertEqual(result['prices'], [[2.38], [18.38]])
            self.assertEqual(result['pricebreaks'], [[5], [1]])
            self.assertEqual(result['manufacturer'],  ['RS', 'RS'])            

    def testSinglePage_HirschmannTestMeasurement  (self):
        if 1:
            from rs.core import Rs
            rs = Rs("Hirschmann Test & Measurement",1,0)
            self.page = rs.getPage()
            with open("rs_HirschmannTestMeasurement.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse()   
            self.assertTrue(len(result['ausUSA']) > 10)
            #print result

    def testSinglePage_FT230XS  (self):
        if 1:
            from rs.core import Rs
            rs = Rs("FT230XS",1,0)
            self.page = rs.getPage()
            with open("rs_FT230XS.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse()   
            self.assertEqual(result['minVPE'], [10,2])
            self.assertEqual(result['stock'], [-1, -1] )
            #self.assertIn('Lieferbar' , result['stock'],[0,0])
            self.assertEqual(result['supplier'], ['RS', 'RS'])
            self.assertEqual(result['mpn'], ['FT230XS-U', 'FT230XS-R'])            
            self.assertEqual(result['ausUSA'], [0,0])
            self.assertEqual(result['ordercode'],  ['888-8710', '757-0010'])
            self.assertEqual(result['prices'], [[1.901], [1.935]])
            self.assertEqual(result['pricebreaks'], [[10],[2 ]])
            self.assertEqual(result['manufacturer'],  ['FTDI Chip','FTDI Chip'])            
 
            #print result

    def testSinglePage_MCP4921_E_MS  (self):
        if 1:
            from rs.core import Rs
            rs = Rs("MCP4921-E/MS",1,0)
            self.page = rs.getPage()
            with open("rs_MCP4921_E_MS.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse()   
            #print result 
            self.assertEqual(result['minVPE'], ['2'])
            self.assertIn('Lieferbar' , result['stock'][0])
            self.assertEqual(result['supplier'], ['RS'])
            self.assertEqual(result['mpn'], ['MCP4921-E/MS'])            
            self.assertEqual(result['ausUSA'], [0])
            self.assertEqual(result['ordercode'],  ['738-6705'])
            self.assertEqual(result['prices'], [[1.97, 1.87]])
            self.assertEqual(result['pricebreaks'], [[2, 10]])
            self.assertEqual(result['manufacturer'],  ['Microchip'])            

            
                
if __package__ is None:
    from os import sys, path
    searchpath = path.abspath(path.join(path.dirname( __file__ ), '..\\..'))
    sys.path.append(searchpath)

if __name__ == "__main__":
    unittest.main()