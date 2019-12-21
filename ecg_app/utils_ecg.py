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
def generateNewTokenSession():
    token_user = random.randint(cte.MIN_RANDOM_SESSION, cte.MAX_RANDOM_SESSION)
    return "user_"+str(token_user)    

# Obtener el valor de la session
def get_session_token(data_session):    
    return data_session["token_session"]
    

# Crea un nuevo directorio para usuario
def create_new_user_dir(token_user):
    ruta_dir = cte.DIR_UPLOAD_FILES + token_user
    
    if not os.path.isdir(ruta_dir) :
        os.mkdir(ruta_dir)

def get_route_file(token_user, fname):
    ruta = cte.DIR_UPLOAD_FILES + token_user + "/" + fname
    return ruta
    

# Guarda el contenido en un fichero
def save_file_proces(token_user, nombre_file, contenido):
    ruta_fichero = cte.DIR_UPLOAD_FILES + token_user + "/" + nombre_file
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
    save_file = cte.DIR_UPLOAD_FILES + token_user + "/" + name_file
    
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
    ruta = cte.DIR_UPLOAD_FILES + ruta_fichero
    
    if os.path.exists(ruta):
        os.remove(ruta)
    

# Comprueba si el nombre del fichero no es nulo o vacío
def name_file_valid(nombre_file):
    if nombre_file is not None and nombre_file != "":
        return True
        
    return False   

