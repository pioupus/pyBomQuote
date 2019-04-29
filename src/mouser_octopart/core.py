#!/usr/bin/env python3

'''
Created on 15.04.2015

@author: arne
'''

import pprint
import octopart_module.core

class Mouser_octo(object):
    def __init__(self, MPN, lagerndeProdukte,USAProdukte):
        self.octo = octopart_module.core.octopart(MPN, lagerndeProdukte,USAProdukte,'Mouser')
        
    def getPage(self):
        return self.octo.getPage()
    
    def getUrl(self):
        return self.octo.seachURL
    
    def parse(self):
        result = self.octo.parse()
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(result)			
        index = 0
        result['URL'] = []
        for packaging in result["packaging"]:
            if packaging=="Custom Reel":
                result["description"][index] = 'Digi-Reel: '+result["description"][index]
                result['stock'][index] = str(result['stock'][index]) + ' / Digi-Reel'
            result['URL'].append('https://www.mouser.de/mvc/header/search?keyword='+result['ordercode'][index])
            index = index+1

        return result