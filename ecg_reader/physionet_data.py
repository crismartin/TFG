#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 21:16:26 2018

@author: cristian
"""

#import numpy as np
import ecg
import wfdb
import matplotlib.pyplot as plt
from IPython.display import display


PHYSIONET_TYPE = "PHYSIONET"


def is_Physionet_file(fileName):
        header = None
        
        try:
            header = wfdb.rdheader(fileName)
        except IOError:
            pass
        
        if (header is None):
            return False
        else:
            return True

# Clase Principal ECGPhysionet
class ECGPhysionet(ecg.ECG):
    typeECG = PHYSIONET_TYPE
    
    def __init__(self, fileName):
        self.fileName = fileName
        self.header = []
        self.signal = []
        self.read_physionet_file(fileName)
        
    def getTypeECG(self):
        return self.typeECG
    
    def getHeader(self):
        return self.header
    
    def getSignal(self):
        return self.signal
    
    def printECG(self, sampleFrom, sampleTo):        
        wfdb.plot_wfdb(record=self.signal.signal, 
                       title='Record a103l from Physionet Challenge 2015',
                       time_units='seconds')

    
    class Header():
        def __init__(self, fileName):
            self.header = self._read_header(fileName)
            
        def _read_header(self, fileName):
            header = wfdb.rdheader(fileName)
            return header
        
        def printInfo(self):
            display('[INFO] Leyendo cabecera fichero physionet %s' %self.header.__dict__)
            
            
    class ECG():
        def __init__(self, fileName):
            self.signal = self._read_ecg_data(fileName)
        
        def _read_ecg_data(self, fileName):
            signal = wfdb.rdrecord(fileName, sampfrom=100, sampto=4000)
            return signal
        
        def printInfo(self):
            print('[INFO] Mostrando signal physionet')
            print(self.signal)
    
    
    def read_physionet_file(self, fileName):
        """
        Function that reads Physionet files format
        """        
        self.header = self.Header(fileName)
        self.signal = self.ECG(fileName)
       

if __name__=="__main__":
    #print(is_Ishne_file("./sample-data/a103l.hea"))
    physioECG = ECGPhysionet("./sample-data/100")
    physioECG.printTestECG()
    physioECG.printECG(100, 15000)
    
    
