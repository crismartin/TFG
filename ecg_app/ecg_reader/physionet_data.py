#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 21:16:26 2018

@author: cristian
"""

#import numpy as np
import ecg
import wfdb
from IPython.display import display



PHYSIONET_TYPE = "PHYSIONET"


def is_Physionet_file(fileRoute):
    header = None  
    fileRoute = fileRoute.split(".")[0]
    print("[INFO][physionet] fichero a crear: " + fileRoute)
    
    try:
        header = wfdb.rdheader(fileRoute)
    except IOError:
        pass
    
    if (header is None):
        return False
    else:
        return True
    

# Clase Principal ECGPhysionet
class ECGPhysionet(ecg.ECG):
    typeECG = PHYSIONET_TYPE
    
    def __init__(self, fileRoute):
        fileRoute = fileRoute.split(".")[0]
        self.fileName = fileRoute.split("/")[-1]
        self.fileRoute = fileRoute
        self.header = []      
        self.signal = []
        self.lenEcg = 0
        self.__allSignal = [] #Asi tengo todos los datos de la señal
        self.read_physionet_file(fileRoute)        
        
    ""
    " Devuelve el formato de ECG "
    ""
    def getTypeECG(self):
        return self.typeECG
    
    ""
    " Devuelve ls datos de cabecera de la señal "
    ""
    def getHeader(self):
        return self.header
    
    ""
    " Devuelve los datos de la señal "
    ""
    def getSignal(self):
        return self.signal
    
    ""
    " Representa la señal ECG "
    ""
    def printECG(self, sampleFrom, sampleTo):        
        wfdb.plot_wfdb(record=self.__allSignal, 
                       title='Record a103l from Physionet Challenge 2015',
                       time_units='seconds')
    
    ""
    " Imprime la informacion de los datos de la señal "
    ""
    def printInfoECG(self):
        display(self.__allSignal.__dict__)
        
    
    
    class Header():
        def __init__(self, fileRoute):           
            self.otherData = self._read_header(fileRoute) #Aqui tengo todos los datos de la cabecera
            self.nLeads = self.otherData.n_sig
            self.samplingRate = self.otherData.fs
            
        def _read_header(self, fileRoute):
            return wfdb.rdheader(fileRoute)
        
        def printInfo(self):
            display('[INFO] Leyendo cabecera fichero physionet %s' %self.otherData.__dict__)
            
            
    class ECG():
        def _read_ecg_data(self, fileRoute, sampfrom, sampto):
            return wfdb.rdrecord(fileRoute, sampfrom=sampfrom, sampto=sampto)

            
        def printInfo(self):
            print('[INFO] Mostrando signal physionet')
            print(self.signal)
    
    
    def read_physionet_file(self, fileRoute):
        """
        Function that reads Physionet files format
        """        
        self.header = self.Header(fileRoute)
        sig_len = self.header.otherData.sig_len
        self.__allSignal = self.ECG()._read_ecg_data(fileRoute, 0, sig_len-1)       
        self.lenEcg = self.__allSignal.sig_len
        self.signal = []
        auxSignal = self.__allSignal.p_signal
        nLeads = self.__allSignal.n_sig
        for n in range(0, nLeads):
            self.signal.append(auxSignal[:, n])
        
       

if __name__=="__main__":
    #print(is_Ishne_file("./sample-data/a103l.hea"))
    physioECG = ECGPhysionet("/Users/cristian/TFG/datos_prueba/physionet/100")
    physioECG.printECG(100, 15000)        
    display(physioECG.signal)
