# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 17:01:24 2015

@author: ak
"""

from PySide import QtCore
from PySide import QtGui
from PySide.QtDeclarative import *
from PySide import QtUiTools
from quote import Quote, ProgressWriter
import os
import datetime

#class Quote():
#    def __init__(self, csvPath=None, csvDelimiter = '|', progressWriter=None):

class dlgBomImport(ProgressWriter):
    
    def __init__(self, parent=None, csvInPath=None, csvDelimiter = '|' ):
        #super(dlgBomImport, self).__init__(parent)
        self.dlg = QtGui.QDialog(parent)
        loader = QtUiTools.QUiLoader()
        self.dlg.ui = loader.load('gui/bomImport.ui') 
        self.dlg.ui.setAttribute(QtCore.Qt.WA_DeleteOnClose); 
        self.dlg.ui.setModal(1);
        self.dlg.ui.show()
        #csvInPath = '..\\boms\\funksonde2\\sg04_btmodul\\bom.txt'
        self.quoter = Quote(csvInPath,csvDelimiter,self)
        fileext = os.path.splitext(csvInPath)
        csvOutPath = fileext[0]+datetime.datetime.now().strftime('%d_%m_%Y')+'.bomQuote'
        print(csvOutPath)
        if os.path.exists(csvOutPath):
            newFile = csvOutPath;
            counter = 0;
            fileext = os.path.splitext(csvOutPath)
            newFile = fileext[0]+'_backup_'+str(counter).zfill(3)+'.bomQuote'
            while os.path.exists(newFile):
                counter += 1;
                newFile = fileext[0]+'_backup_'+str(counter).zfill(3)+'.bomQuote'
            print(newFile)
            os.rename(csvOutPath,newFile)
        self.dlg.ui.btnBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(0)
        self.quoter.doQuote(csvOutPath)
        self.dlg.ui.btnBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(1)
        
    def printMsg(self,msg):
        self.dlg.ui.editLog.append(msg)
        self.dlg.ui.editLog.append('')
        print(msg)
        self.dlg.update();
        self.dlg.repaint();
        QtGui.QApplication.processEvents()
        
    def setProgress(self,progress,total):
        self.dlg.ui.prgProgress.setValue(progress)
        self.dlg.ui.prgProgress.setMaximum(total)
        self.dlg.ui.prgProgress.setMinimum(1)
        self.dlg.ui.editLog.append('')
        print(str(progress)+' of '+str(total))
        QtGui.QApplication.processEvents()