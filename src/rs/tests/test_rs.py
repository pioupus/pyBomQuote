'''
Created on 20.04.2015

@author: arne
'''
import unittest


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


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
        if 1:
            from rs.core import Rs
            rs = Rs("ERJ3EKF2001V",1,0)
            self.page = rs.getPage()
            with open("rs_ERJ3EKF2001V.xml", "ab") as myfile:
                myfile.write(self.page)
            rs.parse()         
        
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()