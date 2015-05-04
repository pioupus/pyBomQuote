#!/usr/bin/env python

from PySide import QtCore
from PySide import QtGui
from PySide.QtDeclarative import *
from PySide import QtUiTools
import os
import sys
import subprocess
 
from tools.core import * 
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
        fileext = os.path.splitext(self.quoteFilePath )
        csvFiles = dict()
            
        for bom in bqd:
            for quote in bom['quotes']:
                node = QtGui.QTreeWidgetItem();
                node = quote['node']
                if node is not '':
                    tree = QtGui.QTreeWidgetItem();
                    #print(quote['node'])
                    if node.checkState(0) == QtCore.Qt.Checked:
                        supplier = quote['supplier']
                        if supplier not in csvFiles:
                            csvOutPath = fileext[0]+'_cart_'+supplier+'.txt'
                            #print(csvOutPath)
                            csvFiles[supplier] = open(csvOutPath, "w")
                        qty = quote['opt_qty']
                        if 'overWriteQty' in quote:
                            qty = quote['overWriteQty']
                        if quote['supplier'] == 'Farnell':
                            ref = bom['ref'].replace( ",", "" );
                            line = quote['sku']+','+str(int(qty))+','+ref+'\n'
                            #print(row_farnell)
                            csvFiles[supplier].write(line)
                            
                        if quote['supplier'] == 'RS':
                            ref = bom['ref'].replace( ",", "-" );
                            ref = ref.replace( " ", "" );
                            line=quote['sku']+','+str(int(qty))+','+ref+'\n'
                            #print(row_rs)
                            csvFiles[supplier].write(line)
        for csvfile in csvFiles:
            csvFiles[csvfile].close();
            editor = os.getenv('EDITOR')
            if editor:
                os.system(editor + ' ' + csvFiles[csvfile].name)
            else:
                subprocess.call("start " + csvFiles[csvfile].name, shell=True)
                        
                        

    def getDBIndexFromTooltip(self,toolTip):
        index=toolTip.split(';')
        index[0] = int(index[0])
        index[1] = int(index[1])
        return index

    def getDBIndexFromItem(self,item):
        return self.getDBIndexFromTooltip(item.toolTip(0))
        
    def getDBItemFromTooltip(self,toolTip):
        index = self.getDBIndexFromTooltip(toolTip)
        bqd = self.bomQuoteData.getBomData()
        #print(index)
        bom=bqd[int(index[0])];
        result={}
        result['bom'] = bom        
        if int(index[1]) > -1:
            quote=bom['quotes'][int(index[1])]
            result['quote'] = quote
        else:
            result['quote'] = []
        return result
        
    def getDBItemFromItem(self,item):   
        return self.getDBItemFromTooltip(item.toolTip(0))
            

        
    def sigTreeDoubleClicked(self,item, column):
        quote = self.getDBItemFromItem(item)['quote']
        webbrowser.open(quote['url'], new=2, autoraise=True)

    def sigActionOpen_quote_file(self):
        dialog = QtGui.QFileDialog(self);
        dialog.setNameFilter("Quote Files (*.BomQuote);;All Files (*.*)")
        if dialog.exec_():
            fileName =  dialog.selectedFiles()[0]
            self.bomQuoteData = BOMQuoteData(fileName)
            self.loadBOMQuote(self.bomQuoteData)
            self.quoteFilePath = fileName
        
    def sigActionFind_and_merge_duplicates(self):
        mergeresult = self.bomQuoteData.mergeDuplicates()
        self.loadBOMQuote(self.bomQuoteData)
        if len(mergeresult[0]) > 0:
            st = ''
            for A in mergeresult[0]:
                st += A['mpn']+' '+A['ref']+'\n'
            QtGui.QMessageBox.warning(self, "Quotes of dublicates are not identical.",
                                           'Quotes of dublicates are not identical. You can solve this by quoting BOMs again.\n'+st,
                                           QtGui.QMessageBox.Ok )            
        

    def sigActionAdd_number_to_quantity_of_parts(self):
        dialog = QtGui.QDialog(self);
        loader = QtUiTools.QUiLoader()
        dialog = loader.load('gui/addqty.ui') 
        #dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose); 
        #dialog.setModal(1);
        if dialog.exec_():
            price = dialog.spnPrice.value();
            qty = dialog.spnQty.value();
            self.bomQuoteData.addQtyToCheapParts(qty,price)
            self.loadBOMQuote(self.bomQuoteData)            


    def sigActionMultiplyQuote(self):
        ok = 0        
        factor = QtGui.QInputDialog.getInt(self, "Factor for multiplication",
                                         'Factor for multiplication', value=1, minValue=0, maxValue=100);
        ok = factor[1]
        factor = factor[0]
        if ok:                                 
            #print(factor)
            self.bomQuoteData.multiplyQuantity(factor)
            self.loadBOMQuote(self.bomQuoteData)
            
   
    def sigbtnSetQtyClicked(self): 
        tooltip = self.ui.btnSetQty.toolTip()
        db = self.getDBItemFromTooltip(tooltip)
        self.ui.btnSetQty.setVisible(0)  
        if db['quote'] == []:
            db['bom']['menge'] = self.ui.spnQty.value()
            self.bomQuoteData.doPricing()
        else:
            db['quote']['overWriteQty'] = self.ui.spnQty.value()
        self.loadBOMQuote(self.bomQuoteData)
        self.ui.frmCellInfo.setVisible(0)
            
    def sigSpnQtyChanged(self,i):
        self.ui.btnSetQty.setVisible(1)  
        
    def sigTreeBomSelected(self): 
        self.ui.frmCellInfo.setVisible(1)
        self.ui.txtCellInfo.clear();
        if len(self.ui.treeBOM.selectedItems()) > 0:
            item = self.ui.treeBOM.selectedItems()[0]
            db = self.getDBItemFromItem(item)
            #print(db)
            if db['quote'] == []:
                self.ui.txtCellInfo.appendPlainText('Ref.: '+str(db['bom']['ref']))
                self.ui.txtCellInfo.appendPlainText('MPN: '+str(db['bom']['mpn']))
                self.ui.txtCellInfo.appendPlainText('Manuf.: '+str(db['bom']['manufacturer']))
                self.ui.txtCellInfo.appendPlainText('Descr.: '+str(db['bom']['description']))
                self.ui.lblqty.setVisible(1)
                self.ui.spnQty.setVisible(1)
                qty = int(db['bom']['menge'])
                #print('qty '+str(qty))
                self.ui.spnQty.setMinimum(1)
                self.ui.spnQty.setValue(qty)
                self.ui.spnQty.setSingleStep(1)
                self.ui.btnSetQty.setToolTip(item.toolTip(0))                
            else:            
                self.ui.txtCellInfo.appendPlainText('MPN: '+str(db['quote']['mpn']))
                self.ui.txtCellInfo.appendPlainText('Manuf.: '+str(db['quote']['manufacturer']))
                self.ui.txtCellInfo.appendPlainText('Descr.: '+str(db['quote']['description']))            
                self.ui.txtCellInfo.appendPlainText('SKU.: '+str(db['quote']['sku']))    
                self.ui.lblqty.setVisible(1)
                self.ui.spnQty.setVisible(1)        
                self.ui.spnQty.setValue(int(db['quote']['opt_qty']))
                #self.ui.spnQty.setMinimum(int(db['quote']['minVPE']))
                #self.ui.spnQty.setSingleStep(int(db['quote']['minVPE']))
                self.ui.spnQty.setMinimum(1)
                self.ui.spnQty.setSingleStep(1)
                self.ui.btnSetQty.setToolTip(item.toolTip(0))
            #print('spin '+str(self.ui.spnQty.value()))
        self.ui.btnSetQty.setVisible(0)
        
    def sigActionQuote_bom_into_file(self): 
        dialog = QtGui.QFileDialog(self);
        dialog.setNameFilter("Bom Files (*.csv);;All Files (*.*)")
        if dialog.exec_():
            fileName =  dialog.selectedFiles()[0]    
            dlgBomImport(self,csvInPath = fileName)

    def selectItem(self,node): 
        node.setSelected(1)
        index = self.ui.treeBOM.indexFromItem(node)
        self.ui.treeBOM.scrollTo(index)

    def doSearch(self, indexFrom):
        searchString = self.ui.edtSearch.text()
        bqd = self.bomQuoteData.getBomData()        
        found = 0
        firstrow = 1
        startTop=indexFrom[0]
        if startTop < 0:
            startTop = 0;
        #print('selectindex '+str(indexFrom[0]))
        for bomItem in bqd[startTop:]:
            if firstrow == 0 or indexFrom[0] == -1:
                #print('top: '+str(bomItem)+'\n')
                if searchString in bomItem['mpn']:
                    self.selectItem(bomItem['node'])
                    found = 1
                    break                
                
            startindex = 0
            if firstrow:
                startindex = indexFrom[1]+1
            for quoteItem in bomItem['quotes'][startindex:]:
                #print('child: '+str(quoteItem)+'\n')
                if (searchString in quoteItem['mpn']) or (searchString in quoteItem['sku']):
                    self.selectItem(quoteItem['node'])
                    found = 1
                    break
            firstrow = 0
            if found:
                break
        return found
        
    def sigBtnSearchNext(self): 
        if len(self.ui.treeBOM.selectedItems()) == 0:
            index = [-1,-1]
        else:
            item = self.ui.treeBOM.selectedItems()[0]
            index = self.getDBIndexFromItem(item)
            item.setSelected(0)
            
        found = self.doSearch(index)
        if found == 0:
            pass
        
    def initUI(self): 
        self.statusBar().showMessage('Ready')
        loader = QtUiTools.QUiLoader()

        self.ui = loader.load('gui/mainwindow.ui')
        self.quoteFilePath = ''
        self.ui.btnExportCarts.clicked.connect(self.sigBtnExportClicked)
        self.ui.actionOpen_quote_file.triggered.connect(self.sigActionOpen_quote_file)
        self.ui.actionQuote_bom_into_file.triggered.connect(self.sigActionQuote_bom_into_file)
        self.ui.actionMultiply_part_quantity.triggered.connect(self.sigActionMultiplyQuote)        
        self.ui.actionFind_and_merge_duplicates.triggered.connect(self.sigActionFind_and_merge_duplicates)
        self.ui.actionAdd_number_to_quantity_of_parts.triggered.connect(self.sigActionAdd_number_to_quantity_of_parts)
        self.ui.btnSetQty.clicked.connect(self.sigbtnSetQtyClicked) 
        self.ui.spnQty.valueChanged.connect(self.sigSpnQtyChanged) 
        
        self.ui.btnSearchNext.clicked.connect(self.sigBtnSearchNext)
        self.ui.edtSearch.returnPressed.connect(self.sigBtnSearchNext)
        self.ui.treeBOM.itemSelectionChanged.connect(self.sigTreeBomSelected)
        self.ui.treeBOM.itemDoubleClicked.connect(self.sigTreeDoubleClicked)
        pf = self.ui.frmCellInfo.palette();
        pe = self.ui.txtCellInfo.palette();
        winColor=pf.color(QtGui.QPalette.Window)
        pe.setColor(QtGui.QPalette.Active, QtGui.QPalette.Base, winColor);
        pe.setColor(QtGui.QPalette.Inactive, QtGui.QPalette.Base, winColor);
        self.ui.txtCellInfo.setPalette(pe);
        self.ui.frmCellInfo.setVisible(0)
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
            top.setToolTip(0,str(topNodeindex)+';-1')            
            top.setFlags(top.flags() | QtCore.Qt.ItemIsUserCheckable)
            top.setCheckState(0,QtCore.Qt.Unchecked);
            top.setBackground(0,BGN_COLOR_TOP_NODE)
            top.setBackground(1,BGN_COLOR_TOP_NODE)
            top.setBackground(2,BGN_COLOR_TOP_NODE)
            top.setBackground(3,BGN_COLOR_TOP_NODE)
            bom['node'] = top
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
            cheapestChild = None
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
                    
                qty = quote['opt_qty']
                price = quote['opt_price']
                if 'overWriteQty' in quote:
                    qty_ = quote['overWriteQty']
                    price = getPriceWithoutOptimization(qty_,quote['prices'],quote['pricebreaks'])
                    if qty != qty_:
                        qty =   str(qty_)+' man. changed!'  
                        child.setBackground(2,BGN_COLOR_TOP_NODE_RED)
                        
                child.setText(2, str(price)+ 'Eur @ '+str(qty)+'\nPackung: '+quote['pku']+'\nStock: '+quote['stock']+USA) #'first Price'
                child.setText(3, quote['description']+'\nMPN: '+quote['mpn']+'\nManuf.: '+quote['manufacturer']) #'beschreibung+mpn+manufacturer'
                child.setFlags(child.flags() | QtCore.Qt.ItemIsUserCheckable)
                child.setCheckState(0,QtCore.Qt.Unchecked);
                if lowestPrice > quote['opt_price']:
                    lowestPrice = quote['opt_price']
                    cheapestChild = child
                top.addChild(child)
                top.setExpanded(True)
                childindex+=1
            
            if cheapestChild is not None:
                cheapestChild.setCheckState(0,QtCore.Qt.Checked);
            if childindex==0:
                top.setBackground(0,BGN_COLOR_TOP_NODE_RED)


def startApp():
     # Create the Qt Application
    
    app = QtGui.QApplication(sys.argv)
    # Create and show the main window
    
    window = MainWindow()
    #window.show()
    # Run the main Qt loop
    sys.exit(app.exec_())   
if __name__ == '__main__':
	startApp();
