#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 23:08:13 2019

@author: cristian
"""


import base64
import os
import urllib2
import random
import constantes_ecg as cte



# Para obtener token de session
def generateTokenSession():
    token_user = random.randint(cte.MIN_RANDOM_SESSION, cte.MAX_RANDOM_SESSION)
    return "user_"+str(token_user)    


# Guarda el contenido en un fichero
def save_file_proces(nombre_file, contenido):
    ruta_fichero = cte.DIR_UPLOAD_FILES + nombre_file
    content_type, content_string = contenido.split(',')
    decoded = base64.b64decode(content_string)
    
    fh = open(ruta_fichero, "wb")
    fh.write(decoded)
    fh.close()
    
    return None


# Descarga un fichero desde una url
def download_file_url(url_file):
    name_file = url_file.split('/')[-1]
    save_file = cte.DIR_UPLOAD_FILES + name_file
    
    try:
        response = urllib2.urlopen(url_file)
        datatowrite = response.read()
        fh = open(save_file, "wb")
        fh.write(datatowrite)
        fh.close()    
        return name_file
    except:
        return None
   

# Borrar un fichero subido
def borrar_fichero(nombre_fichero):    
    ruta = cte.DIR_UPLOAD_FILES + nombre_fichero
    
    if os.path.exists(ruta):
        os.remove(ruta)
    

# Comprueba si el nombre del fichero no es nulo o vacío
def name_file_valid(nombre_file):
    if nombre_file is not None and nombre_file != "":
        return True
        
    return False   

