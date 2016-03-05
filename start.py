#!/usr/bin/env python
from os import sys, path
searchpath = path.abspath(path.join(path.dirname( __file__ ), 'src\\'))
sys.path.append(searchpath)
	
import os

class cd:
    """Context manager for changing the current working directory"""
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
	

with cd('src\\'):
		
	from quote_gui import *
			
	startApp()