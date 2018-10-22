#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 21:16:26 2018

@author: cristian
"""
from IPython.display import display
#import numpy as np
import wfdb

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
    
    

def read_physionet_file(fileName):
    
    header = read_header(fileName)
    """
    Function that reads Physionet files format
    """
    
    "Read file."
    #return [holter, crcCabecera];
   
    return {'header': header, 'ecg' : 'holter.ecg'}


if __name__=="__main__":
    #print(is_Ishne_file("./sample-data/a103l.hea"))
    data_physionet = read_physionet_file("./sample-data/s0010_re")
    
    