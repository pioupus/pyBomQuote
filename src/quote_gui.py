from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtDeclarative import *
from PySide import QtUiTools

import sys
 
from tools.core import * 
import csv 
from debian.changelog import cvs_keyword
from gi.overrides.keysyms import doubbaselinedot
import webbrowser

# Our main window
class MainWindow(QMainWindow):
   
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Main Window")
        self.initUI()
        self.URLS = []

    def sigBtnExportClicked(self):
        bqd = self.bomQuoteData.getBomData()
        csv_farnell = csv.writer(open("farnell.csv", "wb"), delimiter=";" , quotechar='"', quoting=csv.QUOTE_NONE)
        csv_rs = csv.writer(open("rs.csv", "wb"), delimiter=";" , quotechar='"', quoting=csv.QUOTE_NONE)
        for bom in bqd:
            for quote in bom['quotes']:
                node = QTreeWidgetItem();
                node = quote['node']
                if node is not '':
                    tree = QTreeWidgetItem();
                    #print(quote['node'])
                    if node.checkState(0) == Qt.Checked:
                        if quote['supplier'] == 'Farnell':
                            row_farnell=[int(quote['opt_qty']),quote['sku'],bom['ref']]
                            print(row_farnell)
                            csv_farnell.writerow(row_farnell)
                        if quote['supplier'] == 'RS':
                            row_rs=[int(quote['opt_qty']),quote['sku'],bom['ref']]
                            print(row_rs)
                            csv_rs.writerow(row_rs)
                        

    def sigTreeDoubleClicked(self,item, column):
        index=item.toolTip(0).split(';')
        index[0] = int(index[0])
        index[1] = int(index[1])
        bqd = self.bomQuoteData.getBomData()
        print(index)
        #bqd[index[0]]['qotes'][index[1]]
        quote=bqd[index[0]]['quotes'][index[1]]
        #print()
        #import webbrowser  
        webbrowser.open(quote['url'], new=2, autoraise=True)

    def initUI(self): 
        self.statusBar().showMessage('Ready')
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load('gui/mainwindow.ui')
        self.ui.btnExportCarts.clicked.connect(self.sigBtnExportClicked)
        self.ui.treeBOM.itemDoubleClicked.connect(self.sigTreeDoubleClicked)
        
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
        self.bomQuoteData = BOMQuoteData("bomquote_farnell_rs.csv")
        self.loadBOMQuote(self.bomQuoteData)
        self.ui.show()



    def loadBOMQuote(self,bomQuoteData):
        bqd = bomQuoteData.getBomData()
        #bqd = bomQuoteData.bomData;
        tree = QTreeWidget();
        tree = self.ui.treeBOM;
        tree.clear();
        tree.setColumnCount(4)
        topNodeindex=-1
        for bom in bqd: 
            topNodeindex += 1
            #anzahl, MPN, Manufacturer, Beschreibung, ref.
            top = QTreeWidgetItem()
            top.setText(0, 'MPN: '+bom['mpn']+'\n'+'Manuf.: '+bom['manufacturer']+'\nMenge: '+str(bom['menge'])) 
            top.setFlags(top.flags() | Qt.ItemIsUserCheckable)
            top.setCheckState(0,Qt.Unchecked);
            top.setBackground(0,QBrush(Qt.lightGray))
            top.setBackground(1,QBrush(Qt.lightGray))
            top.setBackground(2,QBrush(Qt.lightGray))
            top.setBackground(3,QBrush(Qt.lightGray))
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
            childindex=-1
            for quote in bom['quotes']:
                childindex += 1
                if quote['sku'] == '-1':
                    continue
                if quote['usa'] == 1:
                    continue
                #should be done with checkbox once
                child = QTreeWidgetItem()
                child.setText(0, quote['supplier']) #'supplier'
                child.setText(1, quote['sku']) #'SUK'
                child.setToolTip(0,str(topNodeindex)+';'+str(childindex))
                quote['node'] = child
                USA = quote['usa']
                if USA :
                    USA = '\naus Lager USA'
                else:
                    USA = ''
                #print(quote)
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
