#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 23:08:13 2019

@author: cristian
"""


import base64
import os, glob
from urllib.request import urlopen
import random
import constantes_ecg as cte



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
def save_file_proces(token_user, name_file, contenido):
    saved = False
    ruta_fichero = dir_files + token_user + "/" + name_file
    
    print("[utils_ecg] - save_file_proces() -> name_file: %s" %name_file)
    
    try:
        content_type, content_string = contenido.split(',')
        decoded = base64.b64decode(content_string)
        
        create_new_user_dir(token_user)
       
        fh = open(ruta_fichero, "wb")
        fh.write(decoded)
        fh.close()
        saved = True
        print("[utils_ecg] - save_file_proces() -> saved SUCCESS fichero: "+ str(name_file))
    except:
        print("[utils_ecg] - save_file_proces() -> ERROR al guardar el contenido del fichero: "+ str(name_file))
        
    finally:
        return name_file, saved


# Descarga un fichero desde una url
def download_file_url(token_user, url_file):
    saved = False
    name_file = url_file.split('/')[-1]
    save_file = dir_files + token_user + "/" + name_file
    
    print("[utils_ecg] - download_file_url() -> name_file: %s" %name_file)
    print("[utils_ecg] - download_file_url() -> save_file: %s" %save_file)
    
    try:
        response = urlopen(url_file)
        datatowrite = response.read()
        
        create_new_user_dir(token_user)
        
        fh = open(save_file, "wb")
        fh.write(datatowrite)
        fh.close()    
        saved = True
        print("[utils_ecg] - download_file_url() -> saved SUCCESS fichero: "+ str(name_file))
    except:
        print("[utils_ecg] - download_file_url() -> ERROR al descargar el fichero: " + str(name_file))
        
    finally:
        return name_file, saved


def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
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
def get_name_file(file_url, with_ext):
    filename_aux, extension = os.path.splitext(file_url)
    filename_aux = filename_aux.split("/")[-1]
    filename_aux = filename_aux + extension if with_ext else filename_aux
                
    return filename_aux


# Devuelve la extensión del fichero
def get_ext_file(name_file):
    filename, extension = os.path.splitext(name_file)
    return extension

