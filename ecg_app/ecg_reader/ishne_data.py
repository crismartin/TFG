#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 20:13:59 2018

@author: cristian
"""
from . import ecg as ecg
#import ecg as ecg
import numpy as np
import matplotlib.pyplot as plt
import os
from IPython.display import display



ISHNE_MAGIC_NUM     = "ISHNE1.0"
LONG_MAGICNUM_ISHNE = 8
LONG_CRC_ISHNE      = 1
LONG_FIJA_ISHNE     = 512
NUM_DERIVACIONES    = 12
EXT_FILE_DATA       = ".ecg"
EXT_FILE_ANN        = ".ann"




def is_Ishne_file(fileIshne):
    """
    Comprueba si el fichero tiene formato ISHNE

    Parameters
    ----------
    fileIshne : str
        Ruta del fichero.

    Returns
    -------
    bool
        True si el fichero es ISHNE, False en caso contrario.

    """
    print("[INFO][ISHNE_DATA] - is_Ishne_file() -> fileIshne: %s" %fileIshne)
    fileRoute = fileIshne.split(".")[0]
    print("[INFO][ISHNE_DATA] - is_Ishne_file() -> fileRoute sin ext: %s" %fileRoute)
    fileRoute = fileRoute + EXT_FILE_DATA
    print("[INFO][ISHNE_DATA] - is_Ishne_file() -> fileRoute con ext: %s" %fileRoute)
    fdFile = read_file(fileRoute)
    if fdFile  is not None:
        magicNum = fdFile.read(LONG_MAGICNUM_ISHNE).decode("utf8")
        print("[INFO] - is_Ishne_file() -> MAGIC NUM: %s"  %magicNum)
        fdFile.close()
        
        if(magicNum == ISHNE_MAGIC_NUM):
            return True
        
    return False



def is_ann_Ishne_file(fileAnnIshne):
    """
    Comprueba si las anotaciones tienen formato ISHNE

    Parameters
    ----------
    fileAnnIshne : str
        Ruta del fichero de anotaciones.

    Returns
    -------
    bool
        True si es un fichero de anotaciones válido, False en caso contrario.

    """
    print("[INFO][ISHNE_DATA] - is_ann_Ishne_file() -> fileAnnIshne: %s" %fileAnnIshne)
    fileRoute = fileAnnIshne.split(".")[0]
    print("[INFO][ISHNE_DATA] - is_ann_Ishne_file() -> fileRoute sin ext: %s" %fileAnnIshne)
    fileRoute = fileRoute + EXT_FILE_ANN
    print("[INFO][ISHNE_DATA] - is_ann_Ishne_file() -> fileRoute con ext: %s" %fileAnnIshne)
    fdFile = read_file(fileRoute)
    if fdFile  is not None:
        magicNum = fdFile.read(LONG_MAGICNUM_ISHNE).decode("utf8")
        print("[INFO] - is_ann_Ishne_file() -> MAGIC NUM ANN: '%s'"  %magicNum)
        fdFile.close()
        
        if (magicNum == "ANN  1.0"):
            return True
        
    return False




def get_fileName(urlFile):
    """
    Obtiene el nombre del fichero de la ruta

    Parameters
    ----------
    urlFile : str
        Ruta del fichero.

    Returns
    -------
    str
        Nombre del fichero.

    """
    return urlFile.split("/")[-1]
    

"""
Function that read whatever url file
return memory direction from read bytes
"""
def read_file(urlFile):
    """
    Devuelve el descriptor de un fichero para leer

    Parameters
    ----------
    urlFile : str
        Ruta del fichero.

    Returns
    -------
    int
        Descriptor del fichero para leer.

    """
    try:
        myFile = open(urlFile, 'rb')
        return myFile
    except IOError:
        print("[ERROR][ishne] - read_file() -> File with url '%s' doesn't exist or hasn't ISHNE format." 
              %urlFile)
        return None;
    
    
# Clase principal ECG_ISHNE
class ECGIshne(ecg.ECG):
    
    """
    Entidad para lectura de ficheros Physionet. Extiende de la clase abstracta ECG
        
    Attributes
    ----------
    _typeECG : str
        Formato del ECG, en este caso ISHNE
        
    fileRoute : str
        Ruta absoluta del fichero de electrocardiograma
        
    fileName : str
        Nombre del fichero de electrocardiograma sin extensión
        
    header : Object(Header.class)
        Datos de cabecera del electrocardiograma
        
    signal: array[int]
        Array de muestras del electrocardiograma
        
    annt: Object(Annotation.class)
        Objeto con los datos de las anotaciones sobre el electrocardiograma


    Methods
    -------
    read_signal(self, sampleFrom, sampleTo)
        Lee las muestras de la señal de electrocardiograma en un intervalo
    
    read_ishne_file(self, fileRoute)
        Funcion que lee los datos principales de la señal ECG
    
    read_annotations(self, sampFrom, sampTo)
        Obtiene los datos de las anotaciones del ECG
    
    printECG(self, sampleFrom, sampleTo)
        Muestra en una gráfica el electrocardiograma leído
        
    printSignalData(self)
        Imprime los datos más importantes de la señal ecg, 
        como array de muestras y la frecuencia de muestreo
        
    printInfoECG(self)
        Imprime el array de muestras de la señal ecg
        
    printTestECG(self)
        Imprime un resumen de los datos de cabecera, señal y anotaciones 
        del electrocardiograma    
    
    """
   
    _header = []      
    _signal = []
    _annt = None
    _fileRoute = ""
    _fileName = ""
    _typeECG = ISHNE_MAGIC_NUM
    
    @property
    def fileRoute(self):
        return self._fileRoute
        
    @fileRoute.setter
    def fileRoute(self, newvalue):
        self.fileRoute = newvalue
    
    
    @property
    def fileName(self):
        return self._fileName
      
    @fileName.setter
    def fileName(self, newvalue):
        self.fileRoute = newvalue
    
    
    @property
    def typeECG(self):
        return self._typeECG
        
    @typeECG.setter
    def typeECG(self, newvalue):
        self.typeECG = newvalue
    
    
    @property
    def header(self):
        return self._header
    
    @header.setter
    def header(self, newvalue):
        self.header = newvalue
    
    
    @property
    def signal(self):
        return self._signal
    
    @signal.setter
    def signal(self, newvalue):
        self.signal = newvalue
    
    
    @property
    def annt(self):
        return self._annt
        
    @annt.setter
    def annt(self, newvalue):
        self.annt = newvalue
    
    def __init__(self, fileRoute):
        self._fileRoute = fileRoute.split(".")[0]
        self._fileName = fileRoute.split("/")[-1]
        self.__allSignal = []
        
        self.read_ishne_file(fileRoute)
        
        """
        data = self._read_ishne_file(fileRoute)
        self.header = data['header'] if data != {} else []
        self.__allSignal = data['ecg'] if data != {} else []
        self.signal = self.__allSignal.ecg if self.__allSignal.ecg != [] else None
        self.lenEcg = self.__allSignal.lenEcg if self.__allSignal.ecg != [] else None
        print("data ann: " + str(data["ann"]))
        self.annt = data["ann"] if (data != {} and data["ann"] is not None) else None
        """
        #LECTURA DE LAS ANOTACIONES
        

    
    ""
    " Representa la señal ECG "
    ""
    def printECG(self, sampleFrom, sampleTo):
        """
        Representa la señal de ECG en una figura

        Parameters
        ----------
        sampleFrom : int
            Muestra inicial del ecg a mostrar.
        sampleTo : TYPE
            Muestra final del ecg a mostrar.

        """
        ecg = self._signal
        
        fs = self.getHeader().samplingRate
        offset = 30 + sampleFrom
        
        plt.figure(1)        
        numPlot = (self.getHeader().nLeads * 100) + 11
        
        print("printECG - numLeads: " + str(self.getHeader().nLeads))
        
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
    
    
    
    def printInfoECG(self):
        """
        Imprime en consola la informacion de los datos de la señal
        
        """
        display(self._signal)
    
    
    def printSignalData(self):
        """
        Imprime en consola los datos del array de muestras de ECG 
        """
        print("[INFO][ISHNE] Signal - len:  %s" %str(len(self.signal)))
        print("[INFO][ISHNE] Signal - data: %s" %str(self.signal))
    
    
    def printAnntECG(self):
        """
        Imprime en consola la información de los datos de las anotaciones

        Returns
        -------
        None.

        """
        display(self.annt.__dict__)
        
    
    class Header():
        """
        Entidad de apoyo para devolver los datos de la cabecera del fichero
        
        
        Attributes
        ----------
        
        nLeads : int
            Número total de derivaciones del fichero
            
        samplingRate : int
            Frecuencia de muestreo
            
        signal_len : int
            Número total de muestras de la señal de ECG
        
        comments : str
            Comentarios escritos en la cabecera del fichero
            
            
        Methods
        -------
        
        _parseDateISHNE(self, date)
            Devuelve la fecha en formato DD-MM-YYYY
                    
        _parseSexISHNE(self, sexo)
            Devuelve la equivalencia del sexo        
        
        _nombreCompleto(self, firstName, secondName)
            Devuelve el nombre completo del paciente de quien se tomó los datos
        
        readHeaderISHNE(self, fileFd)
            Lee el fichero para obtener los datos de la cabecera
        
        printInfo(self)
            Imprime en consola los datos más importantes de la cabecera
                
        """
        
        
        def __init__(self, fileFd):
            self.varLenBlockSize = ''
            self.signal_len = np.dtype(np.int32)
            self.offsetVarLengthBlock = ''
            self.offsetECGBlock = ''
            self.fileVersion = ''
            self.firstName = ''
            self.secondName = ''
            self.nombreCompleto = ''
            self.id = ''
            self.sex = ''
            self.race = []
            self.birthDate = []
            self.recordDate = []
            self.fileDate = []            
            self.startDate = []
            self.nLeads = 0
            self.leadSpec = []
            self.leadQual = []
            self.resolution = []
            self.paceMaker = ''
            self.recorder = ''
            self.samplingRate = ''
            self.propierty = ''
            self.copyright = ''
            self.reserverd = ''
            self.comments = []
            self.readHeaderISHNE(fileFd)            
            
        def _parseDateISHNE(self, date):
            fecha_nula = "-9"
            try:
                dia = str(date[0])
                mes = str(date[1])
                anio = str(date[2])
                
                if dia != fecha_nula and mes != fecha_nula and anio != fecha_nula:
                    dia = str(date[0]) if (int(date[0]) > 9) else ( "0" + str(date[0]) )
                    mes = str(date[1]) if (int(date[1]) > 9) else ( "0" + str(date[1]) )
                    anio = str(date[2])
                    
                    fecha = dia + "-" + mes + "-" + anio
                    return fecha
            except Exception:
                print("[INFO][ISHNE] _parseDateISHNE -> Ha ocurrido un error al intentar obtener la fecha")
            
            return None
        
        
        def _parseSexISHNE(self, sexo):
            try:
                if sexo == 0:
                    return "M"
                elif sexo == 1:
                    return "F"
                
            except Exception:
                print("[INFO][ISHNE] _parseSexISHNE -> Ha ocurrido un error al intentar parsear el sexo")
            
            return "unknown"
        
        def _nombreCompleto(self, firstName, secondName):
            nombre = ""
            if firstName is not None and firstName != "":
                nombre += firstName
            
            if secondName is not None and secondName != "":
                if nombre != "":
                    nombre += " " + secondName
                else:
                    nombre += secondName
                    
            return nombre
        
        
        def readHeaderISHNE(self, fileFd):
                                      
            self.varLenBlockSize = np.fromfile(fileFd, dtype=np.int32, count=1)[0]
            self.signal_len = np.fromfile(fileFd, dtype=np.int32, count=1)[0]
            self.offsetVarLengthBlock = np.fromfile(fileFd, dtype=np.int32, count=1)[0]
            self.offsetECGBlock = np.fromfile(fileFd, dtype=np.int32, count=1)[0]
            self.fileVersion = np.fromfile(fileFd, dtype=np.int16, count=1)[0]
            self.firstName = fileFd.read(40).decode("utf8")
            if self.firstName is not None: 
                self.firstName = self.firstName.rstrip('\x00')
                               
            self.secondName = fileFd.read(40).decode("utf8")
            if self.secondName is not None: 
                self.secondName = self.secondName.rstrip('\x00')
                
            self.nombreCompleto = self._nombreCompleto(self.firstName, self.secondName)
            self.id = fileFd.read(20).decode("utf8")
            self.sex = np.fromfile(fileFd, dtype=np.int16, count=1)[0] ##0 Male, 1 Female
            self.sex = self._parseSexISHNE(self.sex)
            self.race = np.fromfile(fileFd, dtype=np.int16, count=1)[0]
            self.birthDate = np.fromfile(fileFd, dtype=np.int16, count=3)
            print("[INFO][ISHNE] readHeaderISHNE -> birthdate: %s" %str(self.birthDate))
            self.birthDate = self._parseDateISHNE(self.birthDate)
            self.recordDate = np.fromfile(fileFd, dtype=np.int16, count=3)
            print("[INFO][ISHNE] readHeaderISHNE -> recordDate: %s" %str(self.recordDate))
            self.recordDate = self._parseDateISHNE(self.recordDate)
            self.fileDate = np.fromfile(fileFd, dtype=np.int16, count=3)    
            print("[INFO][ISHNE] readHeaderISHNE -> fileDate: %s" %str(self.fileDate))
            self.fileDate = self._parseDateISHNE(self.fileDate)                  
            self.startDate = np.fromfile(fileFd, dtype=np.int16, count=3)
            self.nLeads = np.fromfile(fileFd, dtype=np.int16, count=1)[0]
            self.leadSpec = np.fromfile(fileFd, dtype=np.int16, count=12)
            self.leadQual = np.fromfile(fileFd, dtype=np.int16, count=12)
            self.resolution = np.fromfile(fileFd, dtype=np.int16, count=12)
            #
            self.paceMaker = np.fromfile(fileFd, dtype=np.int16, count=1)[0]
            self.recorder = fileFd.read(40).decode("utf8")
            self.samplingRate = np.fromfile(fileFd, dtype=np.int16, count=1)[0]
            self.propierty = fileFd.read(80).decode("utf8")
            self.copyright = fileFd.read(80).decode("utf8")
            self.reserverd = fileFd.read(88).decode("utf8")
            
            if self.nombreCompleto != "":
                self.comments.append("name: " + self.nombreCompleto)
                
            self.comments.append("sex: " + self.sex)
            if self.birthDate is not None:    
                self.comments.append("birthdate: " + self.birthDate)
            
            return self
        
        
        def printInfo(self):
            print("[INFO][ISHNE] ******* HEADER ********")                             
            print("[INFO][ISHNE] length block variable: %s" %self.varLenBlockSize)
            
            print("[INFO][ISHNE] offsetVarLengthBlock: %s" %self.offsetVarLengthBlock)
            print("[INFO][ISHNE] offsetECGBlock: %s" %self.offsetECGBlock)
            print("[INFO][ISHNE] fileVersion: %s" %self.fileVersion)
            print("[INFO][ISHNE] First_Name: %s" %self.firstName)
            print("[INFO][ISHNE] secondName: %s" %self.secondName)
            print("[INFO][ISHNE] ID: %s" %self.id)
            print("[INFO][ISHNE] sex: %s" %self.sex)
                 
            print("[INFO][ISHNE] race: %s" %self.race)
            print("[INFO][ISHNE] birthDate: %s" %self.birthDate )
            print("[INFO][ISHNE] recordDate: %s" %self.recordDate)
            print("[INFO][ISHNE] fileDate: %s" %self.fileDate)
            print("[INFO][ISHNE] startDate: %s" %self.startDate)            
            print("[INFO][ISHNE] leadSpec: %s" %self.leadSpec)
            print("[INFO][ISHNE] leadQual: %s" %self.leadQual)
            print("[INFO][ISHNE] resolution: %s" %self.resolution)
            
            print("[INFO][ISHNE] paceMaker: %s" %self.paceMaker)
            print("[INFO][ISHNE] recorder: %s" %self.recorder)
            
            print("[INFO][ISHNE] propierty: %s" %self.propierty)
            print("[INFO][ISHNE] selfCopyright: %s" %self.copyright)
            print("[INFO][ISHNE] reserverd: %s" %self.reserverd)
            
            print("[INFO][ISHNE] Header - nLeads: %s" %self.nLeads)
            print("[INFO][ISHNE] Header - samplingRate: %s" %self.samplingRate)
            print("[INFO][ISHNE] Header - signal_len: %s" %self.signal_len)
            print("[INFO][ISHNE] Header - comments: %s" %self.comments)
    
        
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



    class ECGSignal():
        """
        Entidad de apoyo para devolver las muestras del ECG
        
        
        Attributes
        ----------
        
        ecg: array of int
            Array de muestras del ECG
        
        lenEcg : int
            Número total de muestras del ECG
            

        Methods
        -------
        read_ecg(self, fdFile, nLeads, sampFrom, sampTo)
            Devuelve las muestras de ECG de un intervalo y su longitud
        
        getECGArray(self)
            Devuelve las muestras de ECG
        
        printInfo(self)
            Imprime en consola los datos más importantes de la señal ECG
                
        """
        
        
        def __init__(self):
            self.crcChecksum = ""
            self.ecg = []
            self.lenEcg = 0
        
        def read_checksum(self, fdFile):
            crcChecksum = np.fromfile(fdFile, dtype=np.uint16, count=LONG_CRC_ISHNE)[0]
            #print("[INFO] CRC CHECKSUM: %s" %crcChecksum)
            return crcChecksum
        
        def read_ecg(self, fdFile, nLeads, sampFrom, sampTo):
            """
            Devuelve las muestras de ECG de un intervalo y su longitud

            Parameters
            ----------
            fdFile : int
                Descriptor del fichero a leer.
            nLeads : int
                Número de derivaciones del ECG.
            sampFrom : int
                Muestra inicial del intervalo de ECG a leer.
            sampTo : int
                Muestra final del intervalo de ECG a leer.

            Returns
            -------
            array of int
                Array de las muestras del ECG
            len_signal_total : int
                Longitud total de muestras leídas.

            """
            len_signal_total = 0
            ecgArrayBytes = np.fromfile(fdFile, dtype=np.int16, count=-1)
            ecgArrayBytes = np.asarray(ecgArrayBytes)            
            ecgArrayBytes = ecgArrayBytes.reshape(-1, nLeads)
            
            ecgChannels = np.hsplit(ecgArrayBytes, nLeads)
            for nChannel in range(nLeads):
                aux = ecgChannels[nChannel].reshape(-1)
                len_aux = len(aux)
                len_signal_total = len(aux)
                sampTo = len_aux if sampTo > len_aux else sampTo
                print("aux len de la señal ecg: " + str(len(aux)))
                self.ecg.append( aux[sampFrom:sampTo] )
            
            return self.ecg, len_signal_total
                
        def readVarBlock(self, fileFd, varLenBlockSize):
            varBlock = np.fromfile(fileFd, dtype=np.byte, count=varLenBlockSize)
            """print("[INFO] varBlockLen: %s" %varBlock);"""
            return varBlock
        
        def printInfo(self):
            """
            Imprime en consola los datos más importantes de la señal ECG

            """
            print("\n[INFO] ******* ECG_SIGNAL_Params ********") 
            print("[INFO] ecg: %s" %self.ecg)
            print("[INFO] ecg-len: %s" %len(self.ecg) )
        
        def getECGArray(self):
            """
            Devuelve las muestras de ECG

            Returns
            -------
            array of int
                Array de muestras.

            """
            return self.ecg
        
    
    class Annotations:
        """
        Clase de apoyo para obtener los datos de las anotaciones en el ECG
        
        Attributes
        ----------
        
        otherData: obj
            Datos completos obtenidos de las anotaciones
        
        ann_len : int
            Longitud total de las muestras de las anotaciones leídas
            
        sample : array of int
            Array de muestras donde estarán ubicadas las anotaciones en el ECG
            
        symbol : array of str
            Array de símbolos de las anotaciones
        
        
        Methods
        -------
        _read_annt(self, fileRoute, posBytesData, sampfrom, sampto)
            Obtiene los datos de las anotaciones de un intervalo del ECG
        
        printInfo(self)
            Imprime en consola los datos obtenidos de las anotaciones
        
        """
        
        def __init__(self, fileRoute, posBytesData, sampfrom, sampto):
            self.otherData = self._read_annt(fileRoute, posBytesData, sampfrom, sampto)

            self.ann_len = self.otherData["ann_len"] if self.otherData is not None else 0
            self.sample = self.otherData["sample"] if self.otherData is not None else None
            self.symbol = self.otherData["symbol"] if self.otherData is not None else None
            
            
        def _read_annt(self, fileRoute, posBytesData, sampfrom, sampto):
            """
            Obtiene los datos de las anotaciones de un intervalo del ECG

            Parameters
            ----------
            fileRoute : str
                Ruta del fichero.
            posBytesData : int
                Posición en bytes donde empieza a leer las anotaciones.
            sampfrom : int
                Muestra inicial del intervalo a leer.
            sampto : int
                Muestra final del intervalo a leer.

            Returns
            -------
            data_ant : array of int
                Array de anotaciones.

            """
            
            
            data_ant = None
            sample = []
            symbol = []
            
            try:
                fileRoute = fileRoute + EXT_FILE_ANN
                print("fileRoute es: " + str(fileRoute))
                
                if is_ann_Ishne_file(fileRoute):
                    print("[INFO][ISHNE][ANN] Leyendo anotaciones ISHNE\n")
                    fdIshneAnn = read_file(fileRoute)
                    fdIshneAnn.seek(posBytesData, 0)
                
                    firstLoc = np.fromfile(fdIshneAnn, dtype=np.int32, count=1)[0]
                    print("[INFO][ISHNE][ANN] firstLoc: " + str(firstLoc) )
        
                    # Obtenemos el numero de latidos
                    currentPosition = fdIshneAnn.tell()
                    fdIshneAnn.seek(0, os.SEEK_END)
                    endPosition = fdIshneAnn.tell()

                    numBeats = (endPosition - currentPosition)//4
                    print("[INFO][ISHNE][ANN] numBeats: " + str(numBeats) )
                    
                    # Preparamos el puntero para leer las anotaciones
                    fdIshneAnn.seek(currentPosition-endPosition, os.SEEK_END)
                    actualFd = fdIshneAnn.tell()
                    print("[INFO][ISHNE][ANN] actualFd: " + str(actualFd) )
                    
                    loc_sample = firstLoc
                    
                    # Leemos las anotaciones
                    for i in range(numBeats):
                        
                        ann = fdIshneAnn.read(1).decode("utf8")                     
                        #print("[INFO][ISHNE][ANN] ann: " + str(ann) )
                        
                        fdIshneAnn.read(1).decode("utf8")
                        #print("[INFO][ISHNE][ANN] internalUse: " + str(internalUse))
                        
                        sample_ecg = np.fromfile(fdIshneAnn, dtype=np.uint16, count=1)[0]
                        loc_sample = loc_sample + sample_ecg                       
                        
                        #print("[INFO][ISHNE][ANN] sample_ecg: " + str(sample_ecg) )
                        
                        if loc_sample < sampfrom:
                            continue
                        
                        if loc_sample > sampto:
                            break
                        
                        symbol.append(ann)
                        sample.append(loc_sample)
                    
                    fdIshneAnn.close()

                    data_ant = dict()
                    data_ant["sample"] = np.array(sample) if sample != [] else None
                    data_ant["ann_len"] = len(sample) if sample != [] else 0
                    data_ant["symbol"] = np.array(symbol) if symbol != [] else None
                    
                    #print("\nData_annt leidos es")
                    #print(data_ant)
                                        
            except IOError:
                print('[WARN] No existe fichero de anotaciones para %s' %fileRoute)
            finally:
                return data_ant
            

        def printInfo(self):
            """
            Imprime en consola los datos obtenidos de las anotaciones

            """
            display('[INFO] Mostrando resumen datos anotaciones ISHNE')
            display('[INFO][ISHNE] Annt - ann_len: %s' %self.ann_len)
            display('[INFO][ISHNE] Annt - samples: %s' %self.sample)
            #display('[INFO] symbols: %s' %self.symbol)
            

    """
    Function that reads ECG ISHNE format
    
    References:
    http://thew-project.org/papers/Badilini.ISHNE.Holter.Standard.pdf
    https://github.com/panrobot/ishneECGviewer/blob/master/ecgViewer.py
    https://bitbucket.org/atpage/ishneholterlib
    """           
    def read_ishne_file(self, fileName):
        """
        Funcion que lee los datos principales de la señal ECG

        Parameters
        ----------
        fileName : str
            Ruta del fichero.

        """
        fileRoute = fileName + EXT_FILE_DATA        
        ecg = self.ECGSignal()
        crc = self.Crc()
                
        fdIshne = read_file(fileRoute) #Open File 'r' mode
        if fdIshne is not None:
            
            fdIshne.read(LONG_MAGICNUM_ISHNE)
            
            ecg.crc = ecg.read_checksum(fdIshne)
            crc.crcCabecera = crc.crc_cabecera(fdIshne)
            
            header = self.Header(fdIshne)
            header.varBlock = ecg.readVarBlock(fdIshne, header.varLenBlockSize)
            crc.joinCrc(header.varBlock)

            fdIshne.close() #Close file
            
            self._header = header
                        
            
        
    def read_signal(self, sampleFrom, sampleTo):
        """
        Lee las muestras de la señal de electrocardiograma en un intervalo

        Parameters
        ----------
        sampleFrom : int
            Muestra inicial del intervalo a leer.
        sampleTo : int
            Muestra final del intervalo a leer.

        """
        fileRoute = self._fileRoute + EXT_FILE_DATA
        ecg = self.ECGSignal()
        
        if self._header == []:
            print('[ERROR][ISHNE] No se puede leer datos. Cabecera errónea para fichero "%s"' %self._fileRoute)
            return
                
        fdIshne = read_file(fileRoute) #Open File 'r' mode
        if fdIshne is None:
            print('[ERROR][ISHNE] No se puede leer datos de la señal. Error al abrir fichero')
            return
        
        byteStartSignal = self.header.offsetECGBlock
        sig_len = self._header.signal_len
        
        fdIshne.seek(byteStartSignal, 0)
        
        if(sampleTo >= 0 and sampleTo <= sig_len) and (sampleFrom < sampleTo):
            self._signal, len_signal_total = ecg.read_ecg(fdIshne, self.header.nLeads, sampleFrom, sampleTo)
            print('[INFO][ISHNE] - read_signal() -> len_signal_total: ' + str(len_signal_total))
            print('[INFO][ISHNE] - read_signal() -> sig_len: ' + str(sig_len))
            self._header.signal_len  = len_signal_total if len_signal_total != sig_len else sig_len            
            
            print('[INFO][ISHNE] - read_signal() -> self._header.signal_len: ' + str(self._header.signal_len))
        else:
            print('[INFO][ISHNE] No se puede leer datos de la señal. Intervalo de muestras erróneo')
        
        fdIshne.close() #Close file 
        
             
             
       
    def read_annotations(self, sampleFrom, sampleTo):
        """
        Obtiene los datos de las anotaciones del ECG

        Parameters
        ----------
        sampleFrom : int
            Muestra inicial del intervalo a leer.
        sampleTo : int
            Muestra final del intervalo a leer.

        """
        if self._header == []:
            print('[ERROR][ISHNE] No se puede leer anotaciones. Cabecera errónea (vacía) para fichero "%s"' %self.fileRoute)
            return
        
        posBytesData = self.header.offsetECGBlock
        sig_len = self._header.signal_len
    
        if(sampleTo >= 0 and sampleTo <= sig_len) and (sampleFrom < sampleTo):
            self._annt = self.Annotations(self.fileRoute, posBytesData, sampleFrom, sampleTo)
        else:
            print('[ERROR][ISHNE] No se puede leer anotaciones. Intervalo de muestras erróneo')
        


if __name__=="__main__":

    #ishneECG = ECGIshne("/Users/cristian/TFG/datos_prueba/matlab_ishne/1-300m")
    ishneECG = ECGIshne("/Users/cristian/TFG/datos_prueba/matlab_ishne/1-300m")
    ishneECG.read_signal(3000, 100000)
    ishneECG.read_annotations(3000, 100000)
    ishneECG.header.printInfo()
    

    #ishneECG.printAnntECG()
    #ishneECG.printECG(0, 150000)
    #display(ishneECG.signal[0])
  
    #ann_Ishne_file("/Users/cristian/TFG/datos_prueba/matlab_ishne/1-300m")
    #y = ishneECG.signal[0]
    #x = [{'value': 1, 'label': 'Derivacion 1'}, {'value': 2, 'label': 'Derivacion 2'}]
