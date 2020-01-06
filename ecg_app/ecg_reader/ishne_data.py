#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:13:59 2018

@author: cristian
"""
import ecg
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display


ISHNE_MAGIC_NUM     = "ISHNE1.0"
LONG_MAGICNUM_ISHNE = 8
LONG_CRC_ISHNE      = 1
LONG_FIJA_ISHNE     = 512
NUM_DERIVACIONES    = 12
EXT_FILE_DATA       = ".ecg"
EXT_FILE_ANN        = ".ann"



"""
Function that return 0 if it has a ISHNE format
"""    
def is_Ishne_file(fileIshne):
    print("[INFO][ISHNE_DATA] - is_Ishne_file() -> fileIshne: %s" %fileIshne)
    fileRoute = fileIshne.split(".")[0]
    print("[INFO][ISHNE_DATA] - is_Ishne_file() -> fileRoute sin ext: %s" %fileRoute)
    fileRoute = fileRoute + EXT_FILE_DATA
    print("[INFO][ISHNE_DATA] - is_Ishne_file() -> fileRoute con ext: %s" %fileRoute)
    fdFile = read_file(fileRoute)
    if(fdFile  > 0):
        magicNum = fdFile.read(LONG_MAGICNUM_ISHNE)
        print("[INFO] - is_Ishne_file() -> MAGIC NUM: %s"  %magicNum)
        fdFile.close()
        
        if(magicNum == ISHNE_MAGIC_NUM):
            return True
        
    return False

"""
Get name file
"""
def get_fileName(urlFile):
        return urlFile.split("/")[-1]
    

"""
Function that read whatever url file
return memory direction from read bytes
"""
def read_file(urlFile):
    try:
        myFile = open(urlFile, 'rb')
        return myFile
    except IOError:
        print("[ERROR][ishne_data] File with url '%s' doesn't exist or hasn't ISHNE format." 
              %urlFile)
        return -1;
    
    
# Clase principal ECG_ISHNE
class ECGIshne(ecg.ECG):
    
    typeECG = ISHNE_MAGIC_NUM
    
    def __init__(self, fileRoute):
        fileRoute = fileRoute.split(".")[0]
        self.fileRoute = fileRoute
        self.fileName = fileRoute.split("/")[-1]
        data = self._read_ishne_file(fileRoute)
        self.header = data['header'] if data != {} else []
        self.__allSignal = data['ecg'] if data != {} else []
        self.signal = self.__allSignal.ecg if self.__allSignal.ecg != [] else None
        self.lenEcg = self.__allSignal.lenEcg if self.__allSignal.ecg != [] else None
        self.annt = None
        #LECTURA DE LAS ANOTACIONES
        
    
    
    ""
    " Devuelve el formato de ECG "
    ""
    def getTypeECG(self):
        return self.typeECG
    
    ""
    " Devuelve ls datos de cabecera de la señal "
    ""
    def getHeader(self):
        return self.header
        
    ""
    " Devuelve los datos de la señal "
    ""
    def getSignal(self):
        return self.signal
    
    ""
    " Representa la señal ECG "
    ""
    def printECG(self, sampleFrom, sampleTo):
        ecg = self.signal
        
        fs = self.getHeader().samplingRate
        offset = 30 + sampleFrom
        
        plt.figure(1)        
        numPlot = 211
        for n in range(self.getHeader().nLeads):
            #lastSample = (fs * (NUM_DERIVACIONES + 1)) + offset
            #print("last sample es: " + str(lastSample))
            #print(str(len(ecg[n])))
            channel = ecg[n][offset:sampleTo]
            x = np.arange(0, len(channel), 1.0)/fs
            
            plt.subplot(numPlot)
            if(n == 0):
                plt.title("Representacion ECG Formato ISHNE")
            #ax = fig.gca()
            #ax.set_xticks(np.arange(0, len(channel), fs))
            
            plt.plot(x, channel)
            plt.xlabel("time/second")
            plt.ylabel("/mV")
            plt.grid(color='g', linestyle='--', linewidth=0.7)            
            numPlot += 1
            #print("size Channel: %d" %len(ecg[n]))
        plt.show()
    
    ""
    " Imprime la informacion de los datos de la señal "
    ""
    def printInfoECG(self):
        display(self.__allSignal.__dict__)
    
    
    
    class Header():
        def __init__(self):
            self.varLenBlockSize = ''
            self.sampleSizeECG = np.dtype(np.int32)
            self.offsetVarLengthBlock = ''
            self.offsetECGBlock = ''
            self.fileVersion = ''
            self.firstName = ''
            self.secondName = ''
            self.id = ''
            self.sex = ''
            self.race = []
            self.birthDate = []
            self.recordDate = []
            self.fileDate = []            
            self.startDate = []
            self.nLeads = ''
            self.leadSpec = []
            self.leadQual = []
            self.resolution = []
            self.paceMaker = ''
            self.recorder = ''
            self.samplingRate = ''
            self.propierty = ''
            self.copyright = ''
            self.reserverd = ''
            
        def _parseDateISHNE(self, date):
            dia = str(date[0]) if (int(date[0]) > 9) else ( "0" + str(date[0]) )
            mes = str(date[1]) if (int(date[1]) > 9) else ( "0" + str(date[1]) )
            anio = str(date[2])
            fecha = dia + "-" + mes + "-" + anio
            return fecha
        
        def readHeaderISHNE(self, fileFd):
                                      
            self.varLenBlockSize = np.fromfile(fileFd, dtype=np.int32, count=1)[0]
            self.sampleSizeECG = np.fromfile(fileFd, dtype=np.int32, count=1)[0]
            self.offsetVarLengthBlock = np.fromfile(fileFd, dtype=np.int32, count=1)[0]
            self.offsetECGBlock = np.fromfile(fileFd, dtype=np.int32, count=1)[0]
            self.fileVersion = np.fromfile(fileFd, dtype=np.int16, count=1)[0]
            self.firstName = fileFd.read(40).strip(' \x00')
            self.secondName = fileFd.read(40).strip(' \x00')
            self.id = fileFd.read(20).strip(' \x00')
            self.sex = np.fromfile(fileFd, dtype=np.int16, count=1)[0] ##0 Male, 1 Female
            self.race = np.fromfile(fileFd, dtype=np.int16, count=1)[0]
            self.birthDate = np.fromfile(fileFd, dtype=np.int16, count=3)
            self.birthDate = self._parseDateISHNE(self.birthDate)
            self.recordDate = np.fromfile(fileFd, dtype=np.int16, count=3)
            self.recordDate = self._parseDateISHNE(self.recordDate)
            self.fileDate = np.fromfile(fileFd, dtype=np.int16, count=3)    
            self.fileDate = self._parseDateISHNE(self.fileDate)                  
            self.startDate = np.fromfile(fileFd, dtype=np.int16, count=3)
            self.nLeads = np.fromfile(fileFd, dtype=np.int16, count=1)[0]
            self.leadSpec = np.fromfile(fileFd, dtype=np.int16, count=12)
            self.leadQual = np.fromfile(fileFd, dtype=np.int16, count=12)
            self.resolution = np.fromfile(fileFd, dtype=np.int16, count=12)
            #
            self.paceMaker = np.fromfile(fileFd, dtype=np.int16, count=1)[0]
            self.recorder = fileFd.read(40).strip(' \x00')
            self.samplingRate = np.fromfile(fileFd, dtype=np.int16, count=1)[0]
            self.propierty = fileFd.read(80).strip(' \x00')
            self.copyright = fileFd.read(80).strip(' \x00')
            self.reserverd = fileFd.read(88).strip(' \x00')
             
            return self
        
        
        def printInfo(self):
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
            print("[INFO] birthDate: %s" %self.birthDate )
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
            
     
    
        
    class Crc():
        def __init__(self):
            self.crcCabecera = []
        
        def crc_cabecera(self, fileFd):
            offsetCabecera = fileFd.tell();
            crcCabecera = np.fromfile(fileFd, dtype=np.uint8,
                                        count=LONG_FIJA_ISHNE)                          
            """print("[INFO] FixedBlock: %s" %crcCabecera)
            print("[INFO] Offset: " + str(offsetCabecera))
            print("[INFO] FixedBlock.size(): " + str(len(crcCabecera)) )"""
            
            fileFd.seek(offsetCabecera, 0); #Para volver al inicio de la cabecera
            return crcCabecera;
        
        def joinCrc(self, varBlock):      
            self.crcCabecera = np.append(self.crcCabecera, varBlock)
        
        def printCrc(self):
            print("[INFO] crcCabecera: %s" %self.crcCabecera)



    class ECG():    
        def __init__(self):
            self.crcChecksum = ""
            self.ecg = []
            self.lenEcg = 0
        
        def read_checksum(self, fdFile):
            crcChecksum = np.fromfile(fdFile, dtype=np.uint16, count=LONG_CRC_ISHNE)[0]
            #print("[INFO] CRC CHECKSUM: %s" %crcChecksum)
            return crcChecksum
        
        def read_ecg(self, fdFile, nLeads):
            ecgArrayBytes = np.fromfile(fdFile, dtype=np.int16, count=-1) 
            ecgArrayBytes = np.asarray(ecgArrayBytes)            
            ecgArrayBytes = ecgArrayBytes.reshape(-1, nLeads)
            
            ecgChannels = np.hsplit(ecgArrayBytes, nLeads)
            for nChannel in range(nLeads):
                aux = ecgChannels[nChannel].reshape(-1)
                self.ecg.append( aux[30:100000] ) #Esto hay que cambiar
            
            return self.ecg       
                
        def readVarBlock(self, fileFd, varLenBlockSize):
            varBlock = np.fromfile(fileFd, dtype=np.byte, count=varLenBlockSize)
            """print("[INFO] varBlockLen: %s" %varBlock);"""
            return varBlock
        
        def printInfo(self):
            print("\n[INFO] ******* ECG_SIGNAL_Params ********") 
            print("[INFO] ecg: %s" %self.ecg)
            print("[INFO] ecg-len: %s" %len(self.ecg) )
        
        def getECGArray(self):
            return self.ecg
        
        
                
    def _read_ishne_file(self, fileRoute):
        fileRoute = fileRoute + EXT_FILE_DATA
        header = self.Header()
        ecg = self.ECG()
        crc = self.Crc()
        
        """
        Function that reads ECG ISHNE format
        
        References:
        http://thew-project.org/papers/Badilini.ISHNE.Holter.Standard.pdf
        https://github.com/panrobot/ishneECGviewer/blob/master/ecgViewer.py
        https://bitbucket.org/atpage/ishneholterlib
        """
        "Read file."
       
        fdIshne = read_file(fileRoute) #Open File 'r' mode
        if(fdIshne > -1):
            fdIshne.read(LONG_MAGICNUM_ISHNE)
            
            ecg.crc = ecg.read_checksum(fdIshne)
            crc.crcCabecera = crc.crc_cabecera(fdIshne)
            header.readHeaderISHNE(fdIshne)
            header.varBlock = ecg.readVarBlock(fdIshne, header.varLenBlockSize)
            crc.joinCrc(header.varBlock)
            ecg.read_ecg(fdIshne, header.nLeads)
            
            fdIshne.close() #Close file 
            
            return {'header': header, 'ecg' : ecg}
        
        return {};
        

if __name__=="__main__":
    #print(is_Ishne_file("./sample-data/a103l.hea"))
    ishneECG = ECGIshne("/Users/cristian/TFG/datos_prueba/matlab_ishne/ishne")
    ishneECG.printInfoECG()
    ishneECG.printECG(0, 150000)
    display(ishneECG.signal[0])
    #y = ishneECG.signal[0]
    #x = [{'value': 1, 'label': 'Derivacion 1'}, {'value': 2, 'label': 'Derivacion 2'}]

    
    
