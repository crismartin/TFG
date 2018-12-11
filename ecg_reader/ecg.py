#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 18:29:54 2018

@author: obarquero
"""


import abc
import ecg_reader
import matplotlib.pyplot as plt
from abc import ABCMeta
#from IPython.display import display

class ECG(object):

    """
    Function that implements an ECG object, which is goin to have basic ECG elements
    indepently of the original format
    """
    def __init__(self, fileIn):
        aux = ecg_reader.read_ECG(fileIn)
        self.signal = aux.data['ecg']
        self.header = aux.data['header']

    def __dict__(self):
        self.data.readDataFile()
        
    def showECG(self):
        plt.plot(self.signal[100:2000])
        plt.ylabel('ECG signal ISHNE format')
        plt.grid(True)
        plt.show()

#Factoria Abstracta
class Data(object):
    __metaclass__ = ABCMeta
    
    @abc.abstractmethod 
    def getData(self):
        pass
    
    
#Factoria concreta para Ficheros ISHNE
class DataIshne(Data):
    
    def __init__(self):
        Data.__init__(self)
    
    def getData(self):
        return DataFileISHNE();


# Clase abstracta para ficheros de datos
class AbstractFileData(object):
    __metaclass__ = ABCMeta
    """
    Declare an interface for a type of file data object.
    """

    @abc.abstractmethod
    def readDataFile(self):
        pass

# Clase concreta para ficheros de datos con formato ISHNE
class DataFileISHNE(AbstractFileData):

    def readDataFile(self):
        print("[INFO] leyendo datos de fichero ISHNE")

# Factoria Concreta para Ficheros de Physionet
class DataPhysionet(Data):
    
    def __init__(self):
        Data.__init__(self)
    
    def getData(self):
        return DataFilePhysionet();

# Clase concreta para ficheros de datos de Physionet
class DataFilePhysionet(AbstractFileData):
    
    def readDataFile(self):
        print("[INFO] Leyendo datos de fichero Physionet")


if __name__ == "__main__":
    print('** Ejecutando como programa principal **')
    ##sample-data/a103l
    #ecg = ECG("./matlab_ishne_code/ishne.ecg")
    ecg = ECG("./sample-data/drive02")
    
    
    