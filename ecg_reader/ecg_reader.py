#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 18:24:24 2018

Module with differente ECG read options

@author: obarquero
"""



import ishne_data
import physionet_data

    
class read_ECG(object):
    """
    Class that implements differente types or ECG formats.
    
    """
    
    def __init__(self, fileIn):
        self.fileIn = fileIn
        self.data = self.get_data_file()
    
    def get_data_file(self):
        if(ishne_data.is_Ishne_file(self.fileIn)):
            return self.read_ECG_ishne()
        elif(physionet_data.is_Physionet_file(self.fileIn)):
            return self.read_ECG_physionet()
            
    
    def read_ECG_physionet(self):
        """
        Function that allows to read ECG in physionet format
        Vamos a utilizar este modulo
        
        References
        https://pypi.python.org/pypi/wfdb
        www.physionet.org
        """
        """
        print ("[INFO] Reading with WFDB Library from Physionet")
        record2 = wfdb.rdrecord(self.fileIn)
        print("[INFO] Record readed with wfdb: \n%s")
        display(record2.__dict__)
        
        print("[INFO] Read Header from WFDB\n")
        header = wfdb.rdheader(self.fileIn)
        display(header.__dict__)
        print("[INFO] fileName: %s" %header.file_name)
        
        if hasattr(header, 'magicNum'):
            print("[INFO] El fichero es ISHNE")
        else:
            print("[INFO] El fichero es Physionet")
        """
        
    def read_ECG_ishne(self):
        return ishne_data.read_ishne_file(self.fileIn)
                
        #TO_DO
        
        #implement this from the MATLAB file I give to you and the code.
        #There is a viewer that we can check how was built.
    
if __name__ == "__main__":
    print('Ejecutando como programa principal')
    # physionet file: sample-data/a103l
    mivariable = read_ECG("./matlab_ishne_code/ishne.ecg")   
    