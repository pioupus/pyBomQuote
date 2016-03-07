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
            result = rs.parse() 
            self.assertEqual(result['minVPE'], [200])
            self.assertEqual(result['stock'], ['Lieferbar'] )
            self.assertEqual(result['supplier'], ['RS'])
            self.assertEqual(result['mpn'], ['GRM188R61A105MA61D'])            
            self.assertEqual(result['ausUSA'], [0])
            self.assertEqual(result['ordercode'],  ['815-1361'])
            self.assertEqual(result['prices'], [[0.018, 0.015]])
            self.assertEqual(result['pricebreaks'], [[200,1000]])
            self.assertEqual(result['manufacturer'],  ['Murata'])


    def testSinglePage_ERJ2RKF3162X(self):
        if 1:
            from rs.core import Rs
            rs = Rs("ERJ-2RKF3162X",1,0)
            self.page = rs.getPage()
            with open("rs_ERJ-2RKF3162X.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse() 
            #print result
            self.assertEqual(result['minVPE'], [1])
            self.assertEqual(result['stock'], ['Nicht verfuegbar'] )
            self.assertEqual(result['supplier'], ['RS'])
            self.assertEqual(result['mpn'], ['ERJ-2RKF3162X'])            
            self.assertEqual(result['ausUSA'], [0])
            self.assertEqual(result['ordercode'],  ['871-9279'])
            self.assertEqual(result['prices'], [[154.50]])
            self.assertEqual(result['pricebreaks'], [[1]])
            self.assertEqual(result['manufacturer'],  ['Panasonic'])
            
    def testSinglePage_24AA16T_I_OT(self):
        if 1:
            from rs.core import Rs
            rs = Rs("24AA16T-I/OT",1,0)
            self.page = rs.getPage()
            with open("rs_24AA16T_I_OT.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse() 
            self.assertEqual(result['minVPE'], [1,1,26])
            self.assertEqual(result['stock'], [-1, -1, -1] )
            self.assertEqual(result['supplier'], ['RS','RS','RS'])
            self.assertEqual(result['mpn'], ['24AA16T-I/OT','24AA16T-I/OT','24AA16T-I/OT'])            
            self.assertEqual(result['ausUSA'], [0,0,0])
            self.assertEqual(result['ordercode'],  ['687-9177','687-9177P','2509537378'])
            self.assertEqual(result['prices'], [[0.30], [0.30], [0.54]])
            self.assertEqual(result['pricebreaks'], [[1],[1],[26]])
            self.assertEqual(result['manufacturer'],  ['Microchip','Microchip','Microchip'])
            #print result
        
    def testSinglePage_ERJ3EKF2001V(self):
        if 1:
            from rs.core import Rs
            rs = Rs("ERJ3EKF2001V",1,0)
            self.page = rs.getPage()
            with open("rs_ERJ3EKF2001V.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse()      
            #print result
            
    def testSinglePage_702_002_10_00(self):
        if 1:
            from rs.core import Rs
            rs = Rs("702-002-10-00",1,0)
            self.page = rs.getPage()
            with open("rs_702-002-10-00.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse()  
            self.assertEqual(result['minVPE'], [-1])
            self.assertEqual(result['stock'], [-1] )
            self.assertEqual(result['supplier'], ['RS'])
            self.assertEqual(result['mpn'], ['-'])            
            self.assertEqual(result['ausUSA'], [-1])
            self.assertEqual(result['ordercode'],  ['-1'])
            self.assertEqual(result['prices'], [[-1]])
            self.assertEqual(result['pricebreaks'], [[-1]])
            self.assertEqual(result['manufacturer'],  ['-'])
            #print result

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
            self.assertEqual(result['prices'], [[0.332], [3354.70]])
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
            self.assertEqual(result['minVPE'], [10])
            self.assertIn('Lieferbar' , result['stock'][0])
            self.assertEqual(result['supplier'], ['RS'])
            self.assertEqual(result['mpn'], ['T491B476K010AT'])            
            self.assertEqual(result['ausUSA'], [0])
            self.assertEqual(result['ordercode'],  ['648-0597'])
            self.assertEqual(result['prices'], [[0.82, 0.65]])
            self.assertEqual(result['pricebreaks'], [[10, 50]])
            self.assertEqual(result['manufacturer'],  ['KEMET'])
            
    def testSinglePage_20_313137(self):
        if 1:
            from rs.core import Rs
            rs = Rs("20-313137",1,0)
            self.page = rs.getPage()
            with open("rs_20-313137.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse()   
            #print result
            self.assertEqual(result['minVPE'], [100])
            self.assertIn('Lieferbar' , result['stock'][0])
            self.assertEqual(result['supplier'], ['RS'])
            self.assertEqual(result['mpn'], ['20-313137'])            
            self.assertEqual(result['ausUSA'], [0])
            self.assertEqual(result['ordercode'],  ['508-0685'])
            self.assertEqual(result['prices'], [[0.261]])
            self.assertEqual(result['pricebreaks'], [[100]])
            self.assertEqual(result['manufacturer'],  ['Vero Technologies'])

    def testSinglePage_LIS331DLH(self):
        if 1:
            from rs.core import Rs
            rs = Rs("LIS331DLH",1,0)
            self.page = rs.getPage()
            with open("rs_LIS331DLH.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse()   
            #print result
            self.assertEqual(result['minVPE'], [1])
            self.assertEqual(result['stock'], ['Lieferbar'] )
            self.assertEqual(result['supplier'], ['RS'])
            self.assertEqual(result['mpn'], ['LIS331DLH'])            
            self.assertEqual(result['ausUSA'], [0])
            self.assertEqual(result['ordercode'],  ['714-7910'])
            self.assertEqual(result['prices'], [[2.76,2.12]])
            self.assertEqual(result['pricebreaks'], [[1,10]])
            self.assertEqual(result['manufacturer'],  ['STMicroelectronics'])

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
            self.assertEqual(result['prices'], [[2.452], [18.93]])
            self.assertEqual(result['pricebreaks'], [[5], [1]])
            self.assertEqual(result['manufacturer'],  ['RS Pro', 'RS Pro'])            

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
            self.assertEqual(result['prices'], [[1.515], [1.86]])
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
            self.assertEqual(result['minVPE'], [2])
            self.assertIn('Lieferbar' , result['stock'][0])
            self.assertEqual(result['supplier'], ['RS'])
            self.assertEqual(result['mpn'], ['MCP4921-E/MS'])            
            self.assertEqual(result['ausUSA'], [0])
            self.assertEqual(result['ordercode'],  ['738-6705'])
            self.assertEqual(result['prices'], [[1.97, 1.87]])
            self.assertEqual(result['pricebreaks'], [[2, 10]])
            self.assertEqual(result['manufacturer'],  ['Microchip'])            

    def testSinglePage_MC0603X105K160CT  (self):
        if 1:
            from rs.core import Rs
            rs = Rs("MC0603X105K160CT",1,0)
            self.page = rs.getPage()
            with open("MC0603X105K160CT.xml", "ab") as myfile:
                myfile.write(self.page)
            result = rs.parse()   
            print result 
            
            self.assertEqual(result['minVPE'], -1)

            
                
if __package__ is None:
    from os import sys, path
    searchpath = path.abspath(path.join(path.dirname( __file__ ), '..\\..'))
    sys.path.append(searchpath)

if __name__ == "__main__":
    unittest.main()