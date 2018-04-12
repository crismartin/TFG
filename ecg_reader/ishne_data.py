#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:13:59 2018

@author: cristian
"""
import numpy as np

ISHNE_MAGIC_NUM = "ISHNE1.0"
LONG_MAGICNUM_ISHNE = 8
LONG_CRC_ISHNE = 1
LONG_FIJA_ISHNE = 512

class Holter():    
    def __init__(self, name):
        self.name = name
        self.mg = ISHNE_MAGIC_NUM
        self.crc = []
        self.header = Header()
        self.ecg = []
    
    def read_checksum(self, fdFile):
        crcChecksum = np.fromfile(fdFile, dtype=np.uint16, count=LONG_CRC_ISHNE)
        print("[INFO] CRC CHECKSUM: %s" %crcChecksum)
        return crcChecksum
    
    def read_ecg(self, fileFd):
        ecg = np.fromfile(fileFd, dtype=np.int16, count=-1)
        print("[INFO] ecg: %s" %ecg)
        print("[INFO] ecg-len: %s" %len(ecg) )
        return ecg
    
class Header():
    def __init__(self):
        self.varLenBlockSize = []
        self.sampleSizeECG = np.dtype(np.int32)
        self.offsetVarLengthBlock = []
        self.offsetECGBlock = []
        self.fileVersion = []
        self.firstName = ""
        self.secondName = ""
        self.id = ""
        self.sex = []
        self.race = []
        self.birthDate = []
        self.recordDate = []
        self.fileDate = []            
        self.startDate = []
        self.nLeads = []
        self.leadSpec = []
        self.leadQual = []
        self.resolution = []
        self.paceMaker = []
        self.recorder = ""
        self.samplingRate = []
        self.propierty = ""
        self.copyright = ""
        self.reserverd = ""
    
    def printHeader(self):
        print("\n[INFO] ******* HEADER ********")                             
        print("[INFO] length block variable: %s" %self.varLenBlockSize)
        print("[INFO] sampleSizeECG: %s" %self.sampleSizeECG)
        print("[INFO] offsetVarLengthBlock: %s" %self.offsetVarLengthBlock)
        print("[INFO] offsetECGBlock: %s" %self.offsetECGBlock)
        print("[INFO] fileVersion: %s" %self.fileVersion)
        print("[INFO] First_Name: %s" %self.firstName)
        print("[INFO] secondName: %s" %self.secondName)
        print("[INFO] ID: %s" %self.id)
        print("[INFO] sex: %s" %self.sex)
             
        print("[INFO] race: %s" %self.race)
        print("[INFO] birthDate: %s" %self.birthDate)
        print("[INFO] recordDate: %s" %self.recordDate)
        print("[INFO] fileDate: %s" %self.fileDate)
        print("[INFO] startDate: %s" %self.startDate)
        print("[INFO] nLeads: %s" %self.nLeads)
        print("[INFO] leadSpec: %s" %self.leadSpec)
        print("[INFO] leadQual: %s" %self.leadQual)
        print("[INFO] resolution: %s" %self.resolution)
        
        print("[INFO] paceMaker: %s" %self.paceMaker)
        print("[INFO] recorder: %s" %self.recorder)
        print("[INFO] samplingRate: %s" %self.samplingRate)
        print("[INFO] propierty: %s" %self.propierty)
        print("[INFO] selfCopyright: %s" %self.copyright)
        print("[INFO] reserverd: %s" %self.reserverd)
    
    def readHeaderISHNE(self, fileFd):
        header = Header()
                                  
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
             
class Crc():
    def __init__(self):
        self.crcCabecera = []
    
    def crc_cabecera(self, fileFd):
        offsetCabecera = fileFd.tell();
        crcCabecera = np.fromfile(fileFd, dtype=np.uint8,
                                    count=LONG_FIJA_ISHNE)                          
        print("[INFO] FixedBlock: %s" %crcCabecera)
        print("[INFO] Offset: " + str(offsetCabecera))
        print("[INFO] FixedBlock.size(): " + str(len(crcCabecera)) )
        
        fileFd.seek(offsetCabecera, 0); #Para volver al inicio de la cabecera
        return crcCabecera;
    
    def joinCrc(self, varBlock):      
        self.crcCabecera = np.append(self.crcCabecera, varBlock)
    
    def printCrc(self):
        print("[INFO] crcCabecera: %s" %self.crcCabecera)


"""
Function that read whatever url file
return memory direction from read bytes
"""
def read_file(urlFile):
    try:
        myFile = open(urlFile, 'rb')
        return myFile
    except IOError:
        print("[ERROR] File with url '%s' doesn't exist." %urlFile)
        return -1;
    
"""
Function that return 0 if it has a ISHNE format
"""    
def is_Ishne_file(fileIshne):
    fdFile = read_file(fileIshne)
    if(fdFile  > 0):
        magicNum = fdFile.read(LONG_MAGICNUM_ISHNE)
        print("[INFO] MAGIC NUM: %s"  %magicNum)
        fdFile.close()
        
        if(magicNum == ISHNE_MAGIC_NUM):
            return True
        
    return False
                
"""
Get name file
"""
def get_fileName(urlFile):
    return urlFile.split("/")[-1]



def read_ishne_file(fileName):
    fname = get_fileName(fileName)
    
    """
    Function that reads ECG ISHNE format
    
    References:
    http://thew-project.org/papers/Badilini.ISHNE.Holter.Standard.pdf
    https://github.com/panrobot/ishneECGviewer/blob/master/ecgViewer.py
    https://bitbucket.org/atpage/ishneholterlib
    """
    "Read file."
    #return [holter, crcCabecera];
    fdIshne = read_file(fileName) #Open File 'r' mode
    if(fdIshne > -1):
        fdIshne.read(LONG_MAGICNUM_ISHNE)
        
        holter = Holter(fname)
        crc = Crc()
        
        holter.crc = holter.read_checksum(fdIshne)
        crc.crcCabecera = crc.crc_cabecera(fdIshne)
        holter.header = holter.header.readHeaderISHNE(fdIshne)
        holter.header.printHeader()
        holter.header.varBlock = holter.header.readVarBlock(fdIshne, holter.header.varLenBlockSize[0])
        crc.joinCrc(holter.header.varBlock)
        crc.printCrc()
        holter.ecg = holter.read_ecg(fdIshne)
        
        fdIshne.close() #Close file 
        
        return (holter, crc)
    
    return [];


if __name__=="__main__":
    #print(is_Ishne_file("./sample-data/a103l.hea"))
    data_ishne = read_ishne_file("./matlab_ishne_code/ishne.ecg")