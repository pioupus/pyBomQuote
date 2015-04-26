from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from PySide import QtUiTools
import csv 
import math

import sys
from tools.core import * 


class BOMQuoteData():
    def __init__(self, parent=None):
        self.bomData = []
    
    def getBomData(self):
        return self.bomData
    
    def doPricing(self):
        for bom in self.bomData:
            qty = bom['menge'];
            for quote in bom['quotes']:
                pb = quote['pricebreaks']
                prices = quote['prices']
                minVPE = quote['minVPE']
                realPrice = getRealPrice(qty,minVPE,prices,pb);
                opt_price = getBestPrice(realPrice, tolerance=0.5)
                if 0:
                    print('sku: '+str(quote['sku']))
                    print('prces: '+str(quote['prices']))         
                    print('pbs:' + str(quote['pricebreaks']))
                    print('qty:' + str(qty))                  
                    print('minVPE:' + str(minVPE))
                    print(opt_price)
                    print('\n')
                quote['opt_price'] = opt_price['price']
                quote['opt_qty'] = opt_price['qty']
                
    def loadFromCSV(self,path):
        csvreader = csv.reader(open("bomquote_farnell_rs.csv", "rb"), delimiter="|")
        for row in csvreader: 
            bomDataSet = {}
            if row[0] == 'orig':
                bomDataSet['menge'] = int(row[1])
                bomDataSet['mpn'] = row[3]
                bomDataSet['manufacturer'] = row[4]
                bomDataSet['ref'] = row[2]
                bomDataSet['description'] = row[5]
                bomDataSet['quotes'] = []
                self.bomData.append(bomDataSet);
            else:
                quoteDataSet={}
                quoteDataSet['sku'] = row[4]
                stock = row[11]
                if stock.isdigit():
                    stock = int(stock);
                    stock = str(stock)
                quoteDataSet['stock'] = stock
                USA = row[12]
                if USA == 'nichtAusUSA':
                    quoteDataSet['usa'] = 0
                else:
                    quoteDataSet['usa'] = 1
                quoteDataSet['description'] = row[7]
                quoteDataSet['minVPE'] = row[8]
                quoteDataSet['pricebreaks'] = []
                quoteDataSet['prices'] = []
                bricebreaks = row[9].strip('[] ')
                
                for pb in bricebreaks.split(', '):
                    pb = float(pb)
                    quoteDataSet['pricebreaks'].append(float(pb))
                    

                prices = row[10].strip('[] ')
                for price in prices.split(', '):
                    price = float(price)
                    quoteDataSet['prices'].append(float(price))
     
                quoteDataSet['mpn'] = row[5]
                quoteDataSet['manufacturer'] = row[6]
                quoteDataSet['supplier'] = row[1]
                quoteDataSet['checked'] = row[0]
                quoteDataSet['url'] = row[13]
                self.bomData[len(self.bomData)-1]['quotes'].append(quoteDataSet)
        self.doPricing();
        
# Our main window
class MainWindow(QMainWindow):
   
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Main Window")
        self.initUI()
        self.URLS = []
    
        
    def initUI(self): 
        self.statusBar().showMessage('Ready')
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load('gui/mainwindow.ui')
        #treeWidget = QTreeWidget()
        #treeWidget.setColumnCount(1)
        if 0:
            BOMEintries = []
            for i in range(10):
                item = QTreeWidgetItem(['hallo','hallo2'])
                BOMEintries.append(item)
            child = QTreeWidgetItem(['child1','child2']);
            child.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            child.setCheckState(0,Qt.Checked);
            BOMEintries[0].addChild(child);
    
            self.ui.treeBOM.insertTopLevelItems(0, BOMEintries)
        self.loadBOMQuote('')
        self.ui.show()



    def loadBOMQuote(self,filePath):
        bqd_ = BOMQuoteData(filePath);
        bqd_.loadFromCSV(filePath);
        bqd = bqd_.getBomData()
        tree = QTreeWidget();
        tree = self.ui.treeBOM;
        tree.clear();
        tree.setColumnCount(5)
        for bom in bqd: 
            #anzahl, MPN, Manufacturer, Beschreibung, ref.
            top = QTreeWidgetItem()
            top.setText(0, 'MPN: '+bom['mpn']+'\n'+'Manuf.: '+bom['manufacturer']+'\nMenge: '+str(bom['menge'])) 
            refs = ''
            kommacounter=0
            for ref in bom['ref'].split(', '):
                kommacounter += 1
                if kommacounter>10:
                    kommacounter=0
                    refs=refs+',\n'+ref
                else:
                    if refs == '':
                        refs = ref
                    else:
                        refs = refs+', '+ref

            top.setText(2, refs)
            top.setText(3, bom['description'])  
                #top.setFirstItemColumnSpanned 
            self.ui.treeBOM.addTopLevelItem(top)
            lowestPrice = sys.maxint
            #cheapestChild = None
            for quote in bom['quotes']:
                if quote['sku'] == '-1':
                    continue
                #print(quote)
                child = QTreeWidgetItem()
                child.setText(0, quote['supplier']) #'supplier'
                child.setText(1, quote['sku']) #'SUK'
                USA = quote['usa']
                if USA :
                    USA = '\naus Lager USA'
                else:
                    USA = ''

                child.setText(2, str(quote['opt_price'])+ 'Eur @ '+str(quote['opt_qty'])+'\nStock: '+quote['stock']+USA) #'first Price'
                child.setText(3, quote['description']+'\nMPN: '+quote['mpn']+'\nManuf.: '+quote['manufacturer']) #'beschreibung+mpn+manufacturer'
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setCheckState(0,Qt.Unchecked);
                if lowestPrice > quote['opt_price']:
                    lowestPrice = quote['opt_price']
                    cheapestChild = child
                top.addChild(child)
                top.setExpanded(True)
            
            cheapestChild.setCheckState(0,Qt.Checked);

                    

                

        
        
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the main window
    window = MainWindow()
    #window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
