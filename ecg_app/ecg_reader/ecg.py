#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 21 18:29:54 2018

Clase abstracta que representará los datos leídos de un fichero de electrocardiograma,
cuyos datos más importantes constarán de cabecera (Header), señal de muestras (signal) y 
anotaciones (ann).
Los formatos ISHNE y Physionet, como cualquier nuevo formato que se agregue al módulo
extenderá/implementará los métodos y la estructura de esta clase, de este modo,
podremos declarar un objeto de ECG y dará igual si es de un formato u otro, 
por lo que obtenemos así una instanciación genérica e independiente de cualquier formato.

@author: obarquero
"""

#from IPython.display import display
from abc import abstractproperty, abstractmethod, ABCMeta

class ECG(object):
    """
    Clase que representa los datos de un fichero de electrocardiograma
        
    Attributes
    ----------
    typeECG : str
        Formato al que pertenece el electrocardiograma, puede ser ISHNE, Physionet, etc
        
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
        Lee las muestras de la señal de electrocardiograma en un intervalor
    
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
    
    __metaclass__ = ABCMeta
    
    """
    Function that implements an ECG object, which is goin to have basic ECG elements
    indepently of the original format
    """
    @abstractproperty
    def fileRoute(self):
        raise NotImplementedError
        
    @fileRoute.setter
    def fileRoute(self, newvalue):
        return
    
    
    @abstractproperty
    def fileName(self):
        raise NotImplementedError
      
    @fileName.setter
    def fileName(self):
        return
    
    
    @abstractproperty
    def typeECG(self):
        raise NotImplementedError
        
    @typeECG.setter
    def typeECG(self):
        return
    
    
    @abstractproperty
    def header(self):
        raise NotImplementedError
    
    @header.setter
    def header(self):
        return
    
    
    @abstractproperty
    def signal(self):
        raise NotImplementedError
    
    @signal.setter
    def signal(self):
        return
    
    
    @abstractproperty
    def annt(self):
        raise NotImplementedError
        
    @annt.setter
    def annt(self):
        return
        
    
    
    def __init__(self, fileRoute):        
        self.fileRoute = fileRoute
        self.fileName = fileRoute.split("/")[-1]
        
    
    @abstractmethod
    def read_signal(self, sampleFrom, sampleTo):
        """
        Lee las muestras de la señal de electrocardiograma en un intervalor

        Parameters
        ----------
        sampleFrom : int
            muestra donde inicia el intervalo a leer
        sampleTo : int
            muestra donde finaliza el intervalo a leer

        Returns
        -------
        array[int] -> Array de muestras de la señal electrocardiograma 
                        comprendido entre el intervalo [sampleFrom, sampleTo]

        """
        pass
    
    @abstractmethod
    def printECG(self, sampleFrom, sampleTo):
        """
        Muestra en una gráfica el electrocardiograma leído

        Parameters
        ----------
        sampleFrom : int
            Muestra que indice el inicio del intervalo de la señal a pintar
        sampleTo : int
            Muestra que indice el fin del intervalo de la señal a pintar

        Returns
        -------
        None.

        """
        pass
    
    
    @abstractmethod
    def printSignalData(self):
        """
        Imprime los datos más importantes de la señal ecg como son:
            - signal: Array con las muestras del electrocardiograma
            - fs: Frecuencia de muestreo

        Returns
        -------
        None.

        """        
        pass
    
    
    ""
    " Imprime la informacion de los datos de la señal "
    ""
    @abstractmethod
    def printInfoECG(self):
        """
        Imprime el array de muestras de la señal ecg
        
        
        Parameters
        ----------        
        self.signal: Array de muestras de la señal ecg        
        """
        pass
    
    
    # Metodo de testing para ver si el objeto se ha creado correctamente
    def printTestECG(self):
        """
        Metodo de testing para ver si el objeto se ha creado correctamente
        Además sirve para ver de una vista rápida los atributos más importantes
        del objeto ECG

        Returns
        -------
        None.

        """
    
        print("********************************************************\n")
        print("************ T E S T - E C G - B E G I N ***************\n")
        print("********************************************************\n")
        print("[TEST][ECG] - fileName: %s" %self.fileName)
        print("[TEST][ECG] - fileRoute: %s" %self.fileRoute)
        print("[TEST][ECG] - typeECG : %s\n" %self.typeECG)
        print("[TEST][ECG] - header - printInfo method START\n")
        self.header.printInfo()
        print("\n[TEST][ECG] - header - printInfo method END\n")
        
        if self.annt is not None:
            print("\n[TEST][ECG] - annotations - printInfo method START\n")
            self.annt.printInfo() 
            print("\n[TEST][ECG] - annotations - printInfo method END\n")
        else:
            print("\n[TEST][ECG] - annotations - annt: %s\n" %str(self.annt))
            
        if self.signal is not None:
            print("\n[TEST][ECG] - signal - printSignalData method START\n")        
            self.printSignalData()
            print("\n[TEST][ECG] - signal - printSignalData method END\n")
        else:
            print("\n[TEST][ECG] - signal - annt: %s\n" %str(self.signal))
        
        print("********************************************************\n")
        print("************** T E S T - E C G - E N D *****************\n")
        print("********************************************************\n")
         
