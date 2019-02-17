#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 18:24:24 2018

Module with differente ECG read options

@author: obarquero
"""

import ishne_data as ishne
import physionet_data as physionet

    
class ECGFactory():
    """
    Class that implements differente types or ECG formats.
    """
    def create_ECG(self, fileName):
        if(ishne.is_Ishne_file(fileName)):
            print("[INFO][ecgFactory] Es un fichero ISHNE1.0")
            return ishne.ECGIshne(fileName)
        elif(physionet.is_Physionet_file(fileName)):
            print("[INFO][ecgFactory] Es un fichero Pyshionet")
            return physionet.ECGPhysionet(fileName)
        else:
            msg = "Formato de fichero no valido y/o no especificado/implementado\n"
            print("\n[ERROR][ecgFactory] " + msg)
            msg = "Formatos disponibles: ['ISHNE', 'PHYSIONET']"
            raise ValueError(msg, 'fileName')
    
    
if __name__ == "__main__":
    print('Ejecutando como programa principal')
    # ishne file: ./matlab_ishne_code/ishne.ecg
    # physionet file: ./sample-data/drive02
    miECG = ECGFactory().create_ECG("./matlab_ishne_code/ishne.ecg")
    miECG.printTestECG()