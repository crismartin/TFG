#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 18:24:24 2018

Module with differente ECG read options

@author: obarquero
"""
import numpy as np
import ishne_data

        
class read_ECG(object):
    """
    Class that implements differente types or ECG formats.
    
    """
    
    def __init__(self):
        return;
    
    def read_ECG_physionet(self):
        """
        Function that allows to read ECG in physionet format
        Vamos a utilizar este modulo
        
        References
        https://pypi.python.org/pypi/wfdb
        www.physionet.org
        """
        print ("Ella se preparo, se puso linda");
        
    def read_ECG_ishne(self):
        myFileURL = "./matlab_ishne_code/ishne.ecg"
        fname = "ishne.ecg"
        
        """
        Function that reads ECG ISHNE format
        
        References:
        http://thew-project.org/papers/Badilini.ISHNE.Holter.Standard.pdf
        https://github.com/panrobot/ishneECGviewer/blob/master/ecgViewer.py
        https://bitbucket.org/atpage/ishneholterlib
        """
        "Read file."
        #return [holter, crcCabecera];
        fileIshne = self.read_file(myFileURL)
        if(fileIshne > -1):
            if(self.is_Ishne_format(fileIshne) != 0):
                print("[WARN] File with url '%s' haven't ISHNE format." %myFileURL)
                return;
            
            holter = ishne_data.Holter(fname)
            crc = ishne_data.Crc()
            
            holter.crc = self.crc_checksum(fileIshne)
            crc.crcCabecera = self.crc_cabecera(fileIshne)
            holter.header = self.readHeaderISHNE(fileIshne)
            holter.header.printHeader()
            holter.header.varBlock = self.readVarBlock(fileIshne, holter.header.varLenBlockSize[0])
            crc.joinCrc(holter.header.varBlock)
            crc.printCrc()
            holter.ecg = self.readEcg(fileIshne)
            
            fileIshne.close() #Close file 
                           
            return [holter, crc]
        
        return [];
                 
    
    """
    Function that read whatever url file
    return memory direction from read bytes
    """
    def read_file(self, urlFile):
        try:
            myFile = open(urlFile, 'rb')
            return myFile
        except IOError:
            print("[ERROR] File with url '%s' doesn't exist." %urlFile)
            return -1;
        
    """
    Function that return 0 if it has a ISHNE format
    """    
    def is_Ishne_format(self, fileIshne):
        magicNum = fileIshne.read(ishne_data.LONG_MAGICNUM_ISHNE)
        print("[INFO] MAGIC NUM: %s"  %magicNum)
        if(magicNum == ishne_data.ISHNE_MAGIC_NUM):
            return 0;
        else:
            return -1;
                
        
    def crc_checksum(self, fileFd):
        crcChecksum = np.fromfile(fileFd, dtype=np.uint16, count=ishne_data.LONG_CRC_ISHNE)
        print("[INFO] CRC CHECKSUM: %s" %crcChecksum)
        return crcChecksum
        
             
    def crc_cabecera(self, fileFd):
        offsetCabecera = fileFd.tell();
        crcCabecera = np.fromfile(fileFd, dtype=np.uint8,
                                    count=ishne_data.LONG_FIJA_ISHNE)                          
        print("[INFO] FixedBlock: %s" %crcCabecera)
        print("[INFO] Offset: " + str(offsetCabecera))
        print("[INFO] FixedBlock.size(): " + str(len(crcCabecera)) )
        
        fileFd.seek(offsetCabecera, 0); #Para volver al inicio de la cabecera
        return crcCabecera;
    
    
    def readHeaderISHNE(self, fileFd):
        header = ishne_data.Header()
                                  
        header.varLenBlockSize = np.fromfile(fileFd, dtype=np.int32, count=1)
        header.sampleSizeECG = np.fromfile(fileFd, dtype=np.int32, count=1)
        header.offsetVarLengthBlock = np.fromfile(fileFd, dtype=np.int32, count=1)
        header.offsetECGBlock = np.fromfile(fileFd, dtype=np.int32, count=1)
        header.fileVersion = np.fromfile(fileFd, dtype=np.int16, count=1)
        header.firstName = fileFd.read(40)
        header.secondName = fileFd.read(40)
        header.id = fileFd.read(20)
        header.sex = np.fromfile(fileFd, dtype=np.int16, count=1)
        header.race = np.fromfile(fileFd, dtype=np.int16, count=1)
        header.birthDate = np.fromfile(fileFd, dtype=np.int16, count=3)
        header.recordDate = np.fromfile(fileFd, dtype=np.int16, count=3)
        header.fileDate = np.fromfile(fileFd, dtype=np.int16, count=3)                  
        header.startDate = np.fromfile(fileFd, dtype=np.int16, count=3)
        header.nLeads = np.fromfile(fileFd, dtype=np.int16, count=1)
        header.leadSpec = np.fromfile(fileFd, dtype=np.int16, count=12)
        header.leadQual = np.fromfile(fileFd, dtype=np.int16, count=12)
        header.resolution = np.fromfile(fileFd, dtype=np.int16, count=12)
        #
        header.paceMaker = np.fromfile(fileFd, dtype=np.int16, count=1)
        header.recorder = fileFd.read(40)
        header.samplingRate = np.fromfile(fileFd, dtype=np.int16, count=1)
        header.propierty = fileFd.read(80)
        header.copyright = fileFd.read(80)
        header.reserverd = fileFd.read(88)
 
        return header
    
    def readVarBlock(self, fileFd, varLenBlockSize):
        varBlock = np.fromfile(fileFd, dtype=np.byte, count=varLenBlockSize)
        print("[INFO] varBlockLen: %s" %varBlock);
        return varBlock
    
    
    def readEcg(self, fileFd):
        ecg = np.fromfile(fileFd, dtype=np.int16, count=-1)
        print("[INFO] ecg: %s" %ecg)
        print("[INFO] ecg-len: %s" %len(ecg) )
        return ecg
        
        #TO_DO
        
        #implement this from the MATLAB file I give to you and the code.
        #There is a viewer that we can check how was built.
    

mivariable = read_ECG();
mivariable.read_ECG_ishne();                     
