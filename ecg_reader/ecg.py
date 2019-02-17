#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 18:29:54 2018

@author: obarquero
"""

#from IPython.display import display

class ECG(object):
    """
    Function that implements an ECG object, which is goin to have basic ECG elements
    indepently of the original format
    """
    fileName = ""
    typeECG = ""
    header = []
    signal = []
    
    def __init__(self, fileName):
        self.fileName = fileName
        
    def getTypeECG(self):
        return self.typeECG
    
    def getHeader(self):
        return self.header
    
    def getSignal(self):
        return self.signal
    
    # Metodo de testing para ver si el objeto se ha creado correctamente
    def printTestECG(self):
        print("********************************************************\n")
        print("************ T E S T - E C G - B E G I N ***************\n")
        print("********************************************************\n")
        print("[TEST][ECG] - fileName: %s\n" %self.fileName)
        print("[TEST][ECG] - typeECG : %s\n" %self.typeECG)
        print("[TEST][ECG] - header - printInfo method called\n")
        self.header.printInfo()
        print("\n[TEST][ECG] - header - printInfo method ended\n")
        print("\n[TEST][ECG] - signal - printInfo method called\n")
        self.signal.printInfo()
        print("\n[TEST][ECG] - header - printInfo method ended\n")
        print("********************************************************\n")
        print("************** T E S T - E C G - E N D *****************\n")
        print("********************************************************\n")
         
        
