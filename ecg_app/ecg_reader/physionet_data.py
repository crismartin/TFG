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
        self.header = []      
        self.signal = []
        self.annt = None
        self.__allSignal = [] #Asi tengo todos los datos de la señal
        
        fileRoute = fileRoute.split(".")[0]
        self.fileName = fileRoute.split("/")[-1]
        self.fileRoute = fileRoute
       
        self.read_physionet_file(fileRoute)
        
    ""
    " Devuelve el formato de ECG "
    ""
    def getTypeECG(self):
        return self.typeECG
    
    ""
    " Devuelve los datos de cabecera de la señal "
    ""
    def getHeader(self):
        return self.header
    
    ""
    " Devuelve los datos de anotaciones de la señal "
    ""
    def getAnnotations(self):
        return self.annt
    
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
        
    
    def printSignalData(self):
        print("[INFO][Physionet] Signal - len:  %s" %str(len(self.signal)))
        print("[INFO][Physionet] Signal - data: %s" %str(self.signal))
        
    
    class Header():
        def __init__(self, fileRoute):           
            self.otherData = self._read_header(fileRoute) # Aqui tengo todos los datos de la cabecera
            self.nLeads = self.otherData.n_sig
            self.samplingRate = self.otherData.fs
            self.signal_len = self.otherData.sig_len
            
        def _read_header(self, fileRoute):
            return wfdb.rdheader(fileRoute)
        
        def printInfo(self):
            display('[INFO][Physionet] Header - otherData: \n%s' %self.otherData.__dict__)
            print("[INFO][Physionet] Header - nLeads: %s" %str(self.nLeads))
            print("[INFO][Physionet] Header - samplingRate: %s" %str(self.samplingRate))
            print("[INFO][Physionet] Header - signal_len: %s" %str(self.signal_len))
            
            
    class ECG():
        def _read_ecg_data(self, fileRoute, sampfrom, sampto):
            return wfdb.rdrecord(fileRoute, sampfrom=sampfrom, sampto=sampto)
            
        def printInfo(self):
            print('[INFO] Mostrando signal physionet')
            print(self.signal)
    
    
    class Annotations:
        def __init__(self, fileRoute, sampfrom, sampto):
            self.otherData = self._read_annt(fileRoute, sampfrom, sampto)
            
            self.ann_len = self.otherData.ann_len if self.otherData is not None else 0
            self.sample = self.otherData.sample if self.otherData is not None and self.otherData.sample != [] else None
            self.symbol = self.otherData.symbol if self.otherData is not None and self.otherData.symbol != [] else None
            
        def _read_annt(self, fileRoute, sampfrom, sampto):
            data_ant = None
            try:
                data_ant = wfdb.rdann(fileRoute, 'atr', sampfrom=sampfrom, sampto=sampto)
            except IOError:
                print('[WARN] No existe fichero de anotaciones para %s' %fileRoute)
            finally:
                return data_ant

        def printInfo(self):
            display('[INFO][Physionet] Mostrando resumen datos ANOTACIONES')
            display('[INFO][Physionet] Annt - ann_len: %s' %self.ann_len)
            display('[INFO][Physionet] Annt - samples: %s' %self.sample)
            #display('[INFO] symbols: %s' %self.symbol)
            #display('[INFO] Leyendo cabecera fichero physionet %s' %self.otherData.__dict__)


    def read_physionet_file(self, fileRoute):
        """
        Function that reads Physionet files format
        """        
        self.header = self.Header(fileRoute)
        
    
    def read_signal(self, sampFrom, sampTo):
        if self.header == []:
            print('[ERROR][Physionet] No se puede leer datos. Cabecera errónea para fichero "%s"' %self.fileRoute)
            return
        
        fileRoute = self.fileRoute
        sig_len = self.header.otherData.sig_len
        
        if (sampTo >= 0 and sampTo <= sig_len) and (sampFrom < sampTo):
            self.__allSignal = self.ECG()._read_ecg_data(fileRoute, sampFrom, sampTo)
            self.lenEcg = self.__allSignal.sig_len
            self.signal = []
            auxSignal = self.__allSignal.p_signal
            nLeads = self.__allSignal.n_sig
            for n in range(0, nLeads):
                self.signal.append(auxSignal[:, n])
        else:
            print('[ERROR][Physionet] No se puede leer datos de la señal. Intervalo de muestras erróneo')
            
    
    
    def read_annotations(self, sampFrom, sampTo):        
        if self.header == []:
            print('[ERROR][Physionet] No se puede leer anotaciones. Cabecera errónea (vacía) para fichero "%s"' %self.fileRoute)
            return
        
        sig_len = self.header.signal_len
        if(sampTo >= 0 and sampTo <= sig_len) and (sampFrom < sampTo):
            self.annt = self.Annotations(self.fileRoute, sampFrom, sampTo)
        else:
            print('[ERROR][Physionet] No se puede leer anotaciones. Intervalo de muestras erróneo')    
    
        
    
    
if __name__=="__main__":
    
    physioECG = ECGPhysionet("/Users/cristian/TFG/datos_prueba/physionet/100")
    physioECG.read_signal(3000, 100000)
    physioECG.read_annotations(3000, 100000)    
    physioECG.printTestECG()
    aux = physioECG.signal[0]
    print("signal[0] size: " + str(len(aux)))
    print("signal[0]: " + str(aux))
