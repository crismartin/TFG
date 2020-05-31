#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 21:16:26 2018

@author: cristian
"""

#import numpy as np
from . import ecg as ecg
#import ecg as ecg
import wfdb
from IPython.display import display



PHYSIONET_TYPE = "PHYSIONET"


def is_Physionet_file(fileRoute):
    """
    Comprueba si el fichero tiene formato Physionet

    Parameters
    ----------
    fileRoute : str
        Ruta del fichero

    Returns
    -------
    bool
        True si el fichero es Physionet, False en caso contrario.

    """
    header = None  
    fileRoute = fileRoute.split(".")[0]
    print("[INFO][physionet] fichero a crear: " + fileRoute)
    
    try:
        header = wfdb.rdheader(fileRoute)
    except IOError:
        pass
    
    if (header is None):
        return False
    else:
        return True
    

# Clase Principal ECGPhysionet
class ECGPhysionet(ecg.ECG):
    """
    Entidad para lectura de ficheros Physionet. Extiende de la clase abstracta ECG
        
    Attributes
    ----------
    _typeECG : str
        Formato del ECG, en este caso Physionet
        
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
    
    read_physionet_file(self, fileRoute)
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
    _typeECG = PHYSIONET_TYPE    
    
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

        self.read_physionet_file(fileRoute)
        
    
    
    def printECG(self, sampleFrom, sampleTo):
        """
        Representa la señal ECG en una gráfica

        Parameters
        ----------
        sampleFrom : int
            Número de la muestra inicial de la señal a pintar
        sampleTo : int
            Número de la muestra final de señal a pintar.


        """
        wfdb.plot_wfdb(record=self.__allSignal, 
                       title='Record a103l from Physionet Challenge 2015',
                       time_units='seconds')
    
    
    def printInfoECG(self):
        """
        Imprime la informacion de los datos de la señal en consola
        
        """
        display(self.__allSignal.__dict__)
        
    
    def printSignalData(self):
        """
        Imprime en consola los datos del array 'signal'
        
        """
        print("[INFO][Physionet] Signal - len:  %s" %str(len(self.signal)))
        print("[INFO][Physionet] Signal - data: %s" %str(self.signal))
        
    
    class Header():
        """
        Entidad de apoyo para devolver los datos de la cabecera del fichero
        
        
        Attributes
        ----------
        
        otherData: obj
            Todos los datos leídos de la cabecera del fichero
        
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
        _read_header(self, fileRoute)
            Lee el fichero para obtener los datos de la cabecera
        
        printInfo(self)
            Imprime en consola los datos más importantes de la cabecera
        
        """        
        
        def __init__(self, fileRoute):           
            self.otherData = self._read_header(fileRoute) # Aqui tengo todos los datos de la cabecera
            self.nLeads = self.otherData.n_sig
            self.samplingRate = self.otherData.fs
            self.signal_len = self.otherData.sig_len
            self.comments = self.otherData.comments if self.otherData.comments != [] else None
            
        def _read_header(self, fileRoute):
            """
            Obtiene los datos de la cabecera

            Parameters
            ----------
            fileRoute : str
                Ruta del fichero.

            Returns
            -------
            obj
                Datos de la cabecera.

            """
            return wfdb.rdheader(fileRoute)
        
        def printInfo(self):
            """
            Imprime en consola los datos obtenidos de la cabecera
            
            """
            display('[INFO][Physionet] Header - otherData: \n%s' %self.otherData.__dict__)
            print("[INFO][Physionet] Header - Main Data:")
            print("[INFO][Physionet] Header - nLeads: %s" %str(self.nLeads))
            print("[INFO][Physionet] Header - samplingRate: %s" %str(self.samplingRate))
            print("[INFO][Physionet] Header - signal_len: %s" %str(self.signal_len))
            print("[INFO][Physionet] Header - comments: " + str(self.comments))
            
            
    class ECGSignal():
        """
        Clase de apoyo para obtener los datos de la señal ECG
        

        Methods
        -------
        _read_ecg_data(self, fileRoute, sampfrom, sampto)
            Devuelve las muestras de la señal ECG en un intervalo
            
        printInfo(self)
            Imprime en consola los datos obtenidos de las muestras de la señal ECG
        
        """
        
    
        def _read_ecg_data(self, fileRoute, sampfrom, sampto):
            """
            Devuelve las muestras de la señal ECG en un intervalo

            Parameters
            ----------
            fileRoute : str
                Ruta del fichero.
            sampfrom : int
                Muestra inicial de la señal ECG a leer.
            sampto : TYPE
                Muestra final de la señal ECG a leer.

            Returns
            -------
            list of int
                Array de muestras de la señal ECG.

            """
            return wfdb.rdrecord(fileRoute, sampfrom=sampfrom, sampto=sampto)
            
        def printInfo(self):
            """
            Imprime en consola los datos obtenidos de las muestras de la señal ECG

            """
            print('[INFO] Mostrando signal physionet')
            print(self.signal)
    
    
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
        _read_annt(self, fileRoute, sampfrom, sampto)
            Obtiene los datos de las anotaciones de un intervalo del ECG
        
        printInfo(self)
            Imprime en consola los datos obtenidos de las anotaciones    
        
        """
        
        
        def __init__(self, fileRoute, sampfrom, sampto):
            self.otherData = self._read_annt(fileRoute, sampfrom, sampto)
            
            self.ann_len = self.otherData.ann_len if self.otherData is not None else 0
            self.sample = self.otherData.sample if self.otherData is not None and self.otherData.sample != [] else None
            self.symbol = self.otherData.symbol if self.otherData is not None and self.otherData.symbol != [] else None
            
        def _read_annt(self, fileRoute, sampfrom, sampto):
            """
            Obtiene los datos de las anotaciones de un intervalo del ECG

            Parameters
            ----------
            fileRoute : str
                Ruta del fichero.
            sampfrom : int
                Muestra inicial de la señal ECG a obtener las anotaciones.
            sampto : TYPE
                Muestra final de la señal ECG a obtener las anotaciones.

            Returns
            -------
            data_ant : obj
                Datos de las anotaciones

            """
            data_ant = None
            try:
                data_ant = wfdb.rdann(fileRoute, 'atr', sampfrom=sampfrom, sampto=sampto)
            except IOError:
                print('[WARN] No existe fichero de anotaciones para %s' %fileRoute)
            finally:
                return data_ant

        def printInfo(self):
            """
            Imprime en consola los datos obtenidos de las anotaciones  

            """
            display('[INFO][Physionet] Mostrando resumen datos ANOTACIONES')
            display('[INFO][Physionet] Annt - ann_len: %s' %self.ann_len)
            display('[INFO][Physionet] Annt - samples: %s' %self.sample)
            #display('[INFO] symbols: %s' %self.symbol)
            #display('[INFO] Leyendo cabecera fichero physionet %s' %self.otherData.__dict__)


    def read_physionet_file(self, fileRoute):
        """
        Function that reads Physionet files format
        """        
        self._header = self.Header(fileRoute)
        
    
    def read_signal(self, sampFrom, sampTo):
        """
        Obtiene los datos de la señal ECG

        Parameters
        ----------
        sampFrom : int
            Muestra inicial de la señal ECG a leer.
        sampTo : TYPE
            Muestra final de la señal ECG a leer.

        """
        if self._header == []:
            print('[ERROR][Physionet] No se puede leer datos. Cabecera errónea para fichero "%s"' %self.fileRoute)
            return
        
        fileRoute = self._fileRoute
        sig_len = self._header.otherData.sig_len
        
        if (sampTo >= 0 and sampTo <= sig_len) and (sampFrom < sampTo):
            self.__allSignal = self.ECGSignal()._read_ecg_data(fileRoute, sampFrom, sampTo)
            self.lenEcg = self.__allSignal.sig_len
            self._signal = []
            auxSignal = self.__allSignal.p_signal
            nLeads = self.__allSignal.n_sig
            for n in range(0, nLeads):
                self._signal.append(auxSignal[:, n])
        else:
            print('[ERROR][Physionet] No se puede leer datos de la señal. Intervalo de muestras erróneo')
            
    
    
    def read_annotations(self, sampFrom, sampTo):
        """
        Obtiene los datos de las anotaciones del ECG

        Parameters
        ----------
        sampFrom : int
            Muestra inicial de la señal ECG para obtener anotaciones.
        sampTo : int
            Muestra final de la señal ECG para obtener anotaciones.

        """
        if self._header == []:
            print('[ERROR][Physionet] No se puede leer anotaciones. Cabecera errónea (vacía) para fichero "%s"' %self.fileRoute)
            return
        
        sig_len = self._header.signal_len
        if(sampTo >= 0 and sampTo <= sig_len) and (sampFrom < sampTo):
            self._annt = self.Annotations(self._fileRoute, sampFrom, sampTo)
        else:
            print('[ERROR][Physionet] No se puede leer anotaciones. Intervalo de muestras erróneo')    
    
        
    
    
if __name__=="__main__":
    
    physioECG = ECGPhysionet("/Users/cristian/TFG/datos_prueba/physionet/100")
    physioECG.read_signal(3000, 100000)
    physioECG.read_annotations(3000, 100000)    
    physioECG.printTestECG()
    aux = physioECG.signal[0]
    print("signal[0] size: " + str(len(aux)))
    print("signal[0]: " + str(aux))
