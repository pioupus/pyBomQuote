#!/usr/bin/env python

from PySide import QtCore
from PySide import QtGui
from PySide.QtDeclarative import *
from PySide import QtUiTools

import sys
 
from tools.core import * 
import csv 
import webbrowser

from bomImport_gui import dlgBomImport 

BGN_COLOR_QUOTE_MATCHED_MPN = QtGui.QBrush(QtGui.QColor(112, 219, 112))
BGN_COLOR_QUOTE_EACH_SECOND_LINE = QtGui.QBrush(QtGui.QColor(227, 241, 255))

BGN_COLOR_TOP_NODE_RED = QtGui.QBrush(QtGui.QColor(255, 51, 0))
BGN_COLOR_TOP_NODE = QtGui.QBrush(QtCore.Qt.lightGray)
# Our main window
class MainWindow(QtGui.QMainWindow):
   
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Main Window")
        self.initUI()
        self.URLS = []

    def sigBtnExportClicked(self):
        bqd = self.bomQuoteData.getBomData()
        csv_farnell = csv.writer(open("farnell.csv", "wb"), delimiter="," , quotechar='"', quoting=csv.QUOTE_NONE)
        csv_rs = csv.writer(open("rs.csv", "wb"), delimiter=";" , quotechar='"', quoting=csv.QUOTE_NONE)
        for bom in bqd:
            for quote in bom['quotes']:
                node = QtGui.QTreeWidgetItem();
                node = quote['node']
                if node is not '':
                    tree = QtGui.QTreeWidgetItem();
                    #print(quote['node'])
                    if node.checkState(0) == QtCore.Qt.Checked:
                        if quote['supplier'] == 'Farnell':
                            ref = bom['ref'].replace( ",", "" );
                            row_farnell=[quote['sku'],int(quote['opt_qty']),ref]
                            #print(row_farnell)
                            csv_farnell.writerow(row_farnell)
                        if quote['supplier'] == 'RS':
                            row_rs=[int(quote['opt_qty']),quote['sku'],bom['ref']]
                            #print(row_rs)
                            csv_rs.writerow(row_rs)
                        

    def sigTreeDoubleClicked(self,item, column):
        index=item.toolTip(0).split(';')
        index[0] = int(index[0])
        index[1] = int(index[1])
        bqd = self.bomQuoteData.getBomData()
        print(index)
        quote=bqd[index[0]]['quotes'][index[1]]
        webbrowser.open(quote['url'], new=2, autoraise=True)

    def sigBtnImportQuote(self):
        dialog = QtGui.QFileDialog(self);
        dialog.setNameFilter("Quote Files (*.BomQuote);;All Files (*.*)")
        if dialog.exec_():
            fileName =  dialog.selectedFiles()[0]
            self.bomQuoteData = BOMQuoteData(fileName)
            self.loadBOMQuote(self.bomQuoteData)
        
    def sigBtnImportBOM(self): 
        dialog = QtGui.QFileDialog(self);
        dialog.setNameFilter("Bom Files (*.csv);;All Files (*.*)")
        if dialog.exec_():
            fileName =  dialog.selectedFiles()[0]    
            bomDlg = dlgBomImport(self,csvInPath = fileName)

        
            
    
    def initUI(self): 
        self.statusBar().showMessage('Ready')
        print('init..')
        loader = QtUiTools.QUiLoader()
        #ui_file = 'gui/mainwindow.ui'
        #if fileexists('gui/mainwindow.ui')
        
        self.ui = loader.load('gui/mainwindow.ui')
        
        self.ui.btnExportCarts.clicked.connect(self.sigBtnExportClicked)
        self.ui.btnImportQuote.clicked.connect(self.sigBtnImportQuote)
        self.ui.btnImportBom.clicked.connect(self.sigBtnImportBOM)
        self.ui.treeBOM.itemDoubleClicked.connect(self.sigTreeDoubleClicked)
        self.ui.show()



    def loadBOMQuote(self,bomQuoteData):
        bqd = bomQuoteData.getBomData()
        #bqd = bomQuoteData.bomData;
        tree = QtGui.QTreeWidget();
        tree = self.ui.treeBOM;
        tree.clear();
        tree.setColumnCount(4)
        topNodeindex=-1
        for bom in bqd: 
            topNodeindex += 1
            #anzahl, MPN, Manufacturer, Beschreibung, ref.
            top = QtGui.QTreeWidgetItem()
            top.setText(0, 'MPN: '+bom['mpn']+'\n'+'Manuf.: '+bom['manufacturer']+'\nMenge: '+str(bom['menge'])) 
            top.setFlags(top.flags() | QtCore.Qt.ItemIsUserCheckable)
            top.setCheckState(0,QtCore.Qt.Unchecked);
            top.setBackground(0,BGN_COLOR_TOP_NODE)
            top.setBackground(1,BGN_COLOR_TOP_NODE)
            top.setBackground(2,BGN_COLOR_TOP_NODE)
            top.setBackground(3,BGN_COLOR_TOP_NODE)
            if len(bom['quotes']) == 0:
                top.setBackground(0,BGN_COLOR_TOP_NODE_RED)
            
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
            top.setText(3, bom['description']+'\n'+bom['footprint'])  
                #top.setFirstItemColumnSpanned 
            self.ui.treeBOM.addTopLevelItem(top)
            lowestPrice = sys.maxint
            quoteIndex=-1
            childindex=0
            for quote in bom['quotes']:
                quoteIndex += 1
                if quote['sku'] == '-1':
                    continue
                if quote['usa'] == 1:
                    continue
                
                #should be done with checkbox once
                child = QtGui.QTreeWidgetItem()
                child.setText(0, quote['supplier']) #'supplier'
                child.setText(1, quote['sku']) #'SUK'
                child.setToolTip(0,str(topNodeindex)+';'+str(quoteIndex))
                quote['node'] = child
                USA = quote['usa']
                if USA :
                    USA = '\naus Lager USA'
                else:
                    USA = ''
                #print(quote)
                if childindex % 2 == 0:
                    child.setBackground(1,BGN_COLOR_QUOTE_EACH_SECOND_LINE)
                    child.setBackground(2,BGN_COLOR_QUOTE_EACH_SECOND_LINE)
                    child.setBackground(3,BGN_COLOR_QUOTE_EACH_SECOND_LINE)

                if quote['mpn'] == bom['mpn']:
                    child.setBackground(3,BGN_COLOR_QUOTE_MATCHED_MPN)
                    #child.setBackground(2,BGN_COLOR_QUOTE_MATCHED_MPN)
                    #child.setBackground(3,BGN_COLOR_QUOTE_MATCHED_MPN)
                    
                
                child.setText(2, str(quote['opt_price'])+ 'Eur @ '+str(quote['opt_qty'])+'\nStock: '+quote['stock']+USA) #'first Price'
                child.setText(3, quote['description']+'\nMPN: '+quote['mpn']+'\nManuf.: '+quote['manufacturer']) #'beschreibung+mpn+manufacturer'
                child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
                child.setCheckState(0,QtCore.Qt.Unchecked);
                if lowestPrice > quote['opt_price']:
                    lowestPrice = quote['opt_price']
                    cheapestChild = child
                top.addChild(child)
                top.setExpanded(True)
                childindex+=1
                
            cheapestChild.setCheckState(0,QtCore.Qt.Checked);
            if childindex==0:
                top.setBackground(0,BGN_COLOR_TOP_NODE_RED)


        
if __name__ == '__main__':
    # Create the Qt Application
    
    app = QtGui.QApplication(sys.argv)
    # Create and show the main window
    
    window = MainWindow()
    #window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())
