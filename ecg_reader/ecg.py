#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 18:29:54 2018

@author: obarquero
"""


import abc
import ecg_reader
from abc import ABCMeta
#from IPython.display import display


class ECG(object):

    """
    Function that implements an ECG object, which is goin to have basic ECG elements
    indepently of the original format
    """
    def __init__(self, fileIn):
        self.data = ecg_reader.read_ECG(fileIn)

    def __dict__(self):
        self.data.readDataFile()
        


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
    ecg = ECG("sample-data/a103l")
    