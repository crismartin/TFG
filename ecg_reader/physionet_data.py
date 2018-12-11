#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 21:16:26 2018

@author: cristian
"""

#import numpy as np
import wfdb
from IPython.display import display




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
    
def read_header(fileName):
    header = wfdb.rdheader(fileName)
    display('[INFO] Leyendo cabecera fichero physionet %s' %header.__dict__)    
    return header
    
def read_ecg_data(fileName):
    signals = wfdb.rdsamp(fileName, sampfrom=100, sampto=15000)
    print('\n[INFO] Mostrando signal physionet')
    print(signals)
    return signals

def read_physionet_file(fileName):
    
    header = read_header(fileName)
    ecg = read_ecg_data(fileName)
    
    """
    Function that reads Physionet files format
    """
    
    "Read file."
    #return [holter, crcCabecera];
   
    return {'header': header, 'ecg': ecg}


if __name__=="__main__":
    #print(is_Ishne_file("./sample-data/a103l.hea"))
    data_physionet = read_physionet_file("./sample-data/drive02")
    
    