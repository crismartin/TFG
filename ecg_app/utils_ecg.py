#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 23:08:13 2019

@author: cristian
"""


import base64
import os, glob
import urllib2
import random
import constantes_ecg as cte
from ecg_reader import ecg_factory as ecgf


dir_files = os.getcwd() + cte.DIR_UPLOAD_FILES


# Para obtener token de session
def generateNewTokenSession():
    token_user = random.randint(cte.MIN_RANDOM_SESSION, cte.MAX_RANDOM_SESSION)
    return "user_"+str(token_user)    

# Obtener el valor de la session
def get_session_token(data_session):    
    return data_session["token_session"]
    

# Crea un nuevo directorio para usuario
def create_new_user_dir(token_user):
    ruta_dir = dir_files + token_user
    
    if not os.path.isdir(ruta_dir) :
        os.mkdir(ruta_dir)

def get_route_file(token_user, fname):
    ruta = cte.DIR_UPLOAD_FILES + token_user + "/" + fname
    return ruta
    

# Guarda el contenido en un fichero
def save_file_proces(token_user, nombre_file, contenido):
    ruta_fichero = dir_files + token_user + "/" + nombre_file
    content_type, content_string = contenido.split(',')
    decoded = base64.b64decode(content_string)
    
    create_new_user_dir(token_user)
   
    fh = open(ruta_fichero, "wb")
    fh.write(decoded)
    fh.close()
    
    return None


# Descarga un fichero desde una url
def download_file_url(token_user, url_file):
    name_file = url_file.split('/')[-1]
    save_file = dir_files + token_user + "/" + name_file
    
    try:
        response = urllib2.urlopen(url_file)
        datatowrite = response.read()
        
        create_new_user_dir(token_user)
        
        fh = open(save_file, "wb")
        fh.write(datatowrite)
        fh.close()    
        return name_file
    except:
        return None



# Borrar un fichero subido
def borrar_fichero(ruta_fichero):    
    filename, extension = os.path.splitext(ruta_fichero)
    ruta = dir_files + filename
    
    #print("** utils_ecg. borrar_fichero() -> ruta: " + ruta)
    for filename in glob.glob(ruta + "*"):
        if os.path.exists(filename):
            os.remove(filename)

    
# Comprueba si el nombre del fichero no es nulo o vacío
def name_file_valid(nombre_file):
    if nombre_file is not None and nombre_file != "":
        return True
        
    return False   


# Devuelve el nombre del fichero sin extesion
def get_name_file(file_url):
    filename_aux, extension = os.path.splitext(file_url)
    filename_aux = filename_aux.split("/")[-1]  
    return filename_aux


# Comprueba si el fichero es de los formatos soportados o no
def is_file_soported(file_route):

    ecgFactory = ecgf.ECGFactory()    
    
    try:
        ecg_data = ecgFactory.create_ECG(file_route)
        filename = ecg_data.fileName
        print( "** 'is_file_soported()' -> fileName: " + str(filename) )    
        return True, filename
    
    except ValueError:
        print( "** 'is_file_soported()' -> Ha ocurrido un error al comprobar el fichero" + str(file_route) )
        filename = get_name_file(file_route)
        return False, filename
    
    except IOError:
        print( "** 'is_file_soported()' -> Ha ocurrido un error de lectura al comprobar el fichero" + str(file_route) )    
        filename = get_name_file(file_route)
        return False, filename
    
    
    