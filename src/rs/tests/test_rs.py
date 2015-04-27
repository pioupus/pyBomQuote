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
        if 0:
            from rs.core import Rs
            rs = Rs("815-1361",1,0)
            self.page = rs.getPage()
            with open("rs_singleresult_nichtlieferbar.xml", "ab") as myfile:
                myfile.write(self.page)
            rs.parse() 

    def testSinglePage_24AA16T_I_OT(self):
        if 0:
            from rs.core import Rs
            rs = Rs("24AA16T-I/OT",1,0)
            self.page = rs.getPage()
            with open("rs_24AA16T_I_OT.xml", "ab") as myfile:
                myfile.write(self.page)
            rs.parse() 
        
    def testSinglePage_ERJ3EKF2001V(self):
        if 0:
            from rs.core import Rs
            rs = Rs("ERJ3EKF2001V",1,0)
            self.page = rs.getPage()
            with open("rs_ERJ3EKF2001V.xml", "ab") as myfile:
                myfile.write(self.page)
            rs.parse()      
            
    def testSinglePage_702_002_10_00(self):
        if 0:
            from rs.core import Rs
            rs = Rs("702-002-10-00",1,0)
            self.page = rs.getPage()
            with open("rs_702-002-10-00.xml", "ab") as myfile:
                myfile.write(self.page)
            rs.parse()           

    def testSinglePage_T491B476K010A(self):
        if 1:
            from rs.core import Rs
            rs = Rs("T491B476K010A",1,0)
            self.page = rs.getPage()
            with open("rs_T491B476K010A.xml", "ab") as myfile:
                myfile.write(self.page)
            rs.parse()   
            
    def testSinglePage_LIS331DLH(self):
        if 1:
            from rs.core import Rs
            rs = Rs("LIS331DLH",1,0)
            self.page = rs.getPage()
            with open("rs_LIS331DLH.xml", "ab") as myfile:
                myfile.write(self.page)
            rs.parse()               

              
                
if __package__ is None:
    from os import sys, path
    searchpath = path.abspath(path.join(path.dirname( __file__ ), '..\\..'))
    sys.path.append(searchpath)

if __name__ == "__main__":
    unittest.main()