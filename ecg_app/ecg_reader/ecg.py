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
    fileRoute = ""
    fileName = ""
    typeECG = ""
    header = []
    signal = []
    annt = []
    
    def __init__(self, fileRoute):        
        self.fileRoute = fileRoute
        self.fileName = fileRoute.split("/")[-1]
        
    def getFileName(self):
        return self.fileName
    
    def getTypeECG(self):
        return self.typeECG
    
    def getHeader(self):
        return self.header
    
    def getSignal(self):
        return self.signal
    
    def getAnnotations(self):
        return self.annt
    
    def printECG(self, sampleFrom, sampleTo):
        return self.printECG(sampleFrom, sampleTo)
    
    ""
    " Imprime la informacion de los datos de la señal "
    ""
    def printInfoECG(self):
        return self.printInfoECG()
    
    # Metodo de testing para ver si el objeto se ha creado correctamente
    def printTestECG(self):
        print("********************************************************\n")
        print("************ T E S T - E C G - B E G I N ***************\n")
        print("********************************************************\n")
        print("[TEST][ECG] - fileName: %s" %self.fileName)
        print("[TEST][ECG] - fileRoute: %s" %self.fileRoute)
        print("[TEST][ECG] - typeECG : %s\n" %self.typeECG)
        print("[TEST][ECG] - header - printInfo method called\n")
        self.header.printInfo()
        print("\n[TEST][ECG] - header - printInfo method ended\n")
        print("\n[TEST][ECG] - annotations - printInfo method called\n")
        self.annt.printInfo()
        print("\n[TEST][ECG] - annotations - printInfo method ended\n")
        print("\n[TEST][ECG] - signal - printInfo method called\n")
        self.printInfoECG()
        print("\n[TEST][ECG] - header - printInfo method ended\n")
        print("********************************************************\n")
        print("************** T E S T - E C G - E N D *****************\n")
        print("********************************************************\n")
         
