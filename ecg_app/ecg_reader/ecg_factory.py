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
        print("[INFO][ecgFactory] nombre del fichero a crear: " + fileName)
        if(ishne.is_Ishne_file(fileName)):
            print("[INFO][ecgFactory] Es un fichero ISHNE1.0")
            return ishne.ECGIshne(fileName)
        
        if(physionet.is_Physionet_file(fileName)):
            print("[INFO][ecgFactory] Es un fichero Pyshionet")
            return physionet.ECGPhysionet(fileName)
        
        msg = "Formato de fichero no valido y/o no especificado/implementado\n"
        print("\n[ERROR][ecgFactory] " + msg)
        msg = "Formatos disponibles: ['ISHNE', 'PHYSIONET']"
        raise ValueError(msg, 'fileName')
    
    
if __name__ == "__main__":
    print('Ejecutando como programa principal')
    # ishne file: ./matlab_ishne_code/ishne.ecg
    # physionet file: ./sample-data/drive02             #Con 5 leads
    #                  ./sample-data/100
    # physionet file: ../physionet/100
    #     ishne file: ../matlab_ishne/ishne.ecg
    miECG = ECGFactory().create_ECG("/Users/cristian/TFG/datos_prueba/physionet/100")
    sig_len = miECG.header.signal_len
    miECG.read_annotations(0, sig_len)
    miECG.printTestECG()