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
        self.name = name;
        self.mg = ISHNE_MAGIC_NUM;
        self.crc = [];
        self.header = Header();
        self.ecg = [];
    
    
class Header():
    def __init__(self):
        self.varLenBlockSize = [];
        self.sampleSizeECG = np.dtype(np.int32);
        self.offsetVarLengthBlock = [];
        self.offsetECGBlock = [];
        self.fileVersion = [];
        self.firstName = "";
        self.secondName = "";
        self.id = "";
        self.sex = [];
        self.race = [];
        self.birthDate = [];
        self.recordDate = [];
        self.fileDate = [];                        
        self.startDate = [];
        self.nLeads = [];
        self.leadSpec = [];
        self.leadQual = [];
        self.resolution = [];
        self.paceMaker = [];
        self.recorder = "";
        self.samplingRate = [];
        self.propierty = "";
        self.copyright = "";
        self.reserverd = "";
    
    def printHeader(self):
        print("\n[INFO] ******* HEADER ********");                             
        print("[INFO] length block variable: %s" %self.varLenBlockSize);
        print("[INFO] sampleSizeECG: %s" %self.sampleSizeECG);
        print("[INFO] offsetVarLengthBlock: %s" %self.offsetVarLengthBlock);
        print("[INFO] offsetECGBlock: %s" %self.offsetECGBlock);
        print("[INFO] fileVersion: %s" %self.fileVersion);
        print("[INFO] First_Name: %s" %self.firstName);
        print("[INFO] secondName: %s" %self.secondName);
        print("[INFO] ID: %s" %self.id);
        print("[INFO] sex: %s" %self.sex);
             
        print("[INFO] race: %s" %self.race);
        print("[INFO] birthDate: %s" %self.birthDate);
        print("[INFO] recordDate: %s" %self.recordDate);
        print("[INFO] fileDate: %s" %self.fileDate);
        print("[INFO] startDate: %s" %self.startDate);
        print("[INFO] nLeads: %s" %self.nLeads);
        print("[INFO] leadSpec: %s" %self.leadSpec);
        print("[INFO] leadQual: %s" %self.leadQual);
        print("[INFO] resolution: %s" %self.resolution);
        
        print("[INFO] paceMaker: %s" %self.paceMaker);
        print("[INFO] recorder: %s" %self.recorder);
        print("[INFO] samplingRate: %s" %self.samplingRate);
        print("[INFO] propierty: %s" %self.propierty);
        print("[INFO] selfCopyright: %s" %self.copyright);
        print("[INFO] reserverd: %s" %self.reserverd);
        
             
class Crc():
    def __init__(self):
        self.crcCabecera = []
    
    def joinCrc(self, varBlock):      
        self.crcCabecera = np.append(self.crcCabecera, varBlock)
    
    def printCrc(self):
        print("[INFO] crcCabecera: %s" %self.crcCabecera)