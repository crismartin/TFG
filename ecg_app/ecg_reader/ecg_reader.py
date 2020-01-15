#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 18:24:24 2018

Module with differente ECG read options

@author: obarquero
"""


import ecg_reader.ecg_factory as ecgf


    
if __name__ == "__main__":
    print('[ecg_reader] Ejecutando como programa principal')
    # ishne file: ./matlab_ishne_code/ishne.ecg
    # physionet file: ./sample-data/drive02
    ecgFactory = ecgf.ECGFactory()
    ecg = ecgFactory.create_ECG("./sample-data/drive02")
    ecg.printTestECG() 
    