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
import src.commons.constantes_ecg as cte
from datetime import datetime
import shutil


dir_files = os.getcwd() + cte.DIR_UPLOAD_FILES


# Elimina un directorio con todo lo que hay dentro de él
def remove_dir(name_dir):
    """
    Elimina un directorio de manera recursiva

    Parameters
    ----------
    name_dir : str
        Nombre del directorio.

    Returns
    -------
    result : bool
        True si se ha borrado, False si ha ocurrido un error.

    """
    result = False
    path_folder = dir_files + "/" + name_dir
    try:
        print("[ utils_ecg ] - remove_dir() -> DIRECTORIO a BORRAR '%s'" %name_dir)
        shutil.rmtree(path_folder, ignore_errors=True)
        result = True
    except Exception:
        print("[ utils_ecg ] - remove_dir() -> Ha ocurrido un error al intentar borrar el directorio '%s'" %name_dir)
    
    return result


# Devuelve la fecha actual en un string
def getCurrentStringDate(formato):
    """
    Devuelve la fecha actual en formato DD/MM/YYYY o en el 'formato' del parámetro

    Parameters
    ----------
    formato : str
        Formato de la fecha a devolver.

    Returns
    -------
    string : str
        Fecha en formato DD/MM/YYYY o en 'formato'.

    """
    date_registro = datetime.now()
    formato = "%d/%m/%Y" if formato is None else formato
    string = date_registro.strftime(formato)
    return string


# Para obtener token de session
def generateNewTokenSession():
    """
    Genera un nuevo token de sesión

    Returns
    -------
    TYPE
        Nuevo token de sesión.

    """
    token_user = random.randint(cte.MIN_RANDOM_SESSION, cte.MAX_RANDOM_SESSION)
    return "session_"+str(token_user)    


# Obtener el valor de la session
def get_session_token(data_session):    
    """
    Obtiene el token de los datos de sesión

    Parameters
    ----------
    data_session : obj
        Datos de sesión.

    Returns
    -------
    str
        Token de la sesión.

    """
    return data_session["token_session"]
    

# Crea un nuevo directorio para usuario
def create_new_user_dir(token_user):
    """
    Crea un nuevo directorio para una sesión

    Parameters
    ----------
    token_user : str
        Token de la sesión.

    """
    ruta_dir = dir_files + token_user
    
    if not os.path.isdir(ruta_dir) :
        os.mkdir(ruta_dir)
        

def get_route_file(token_user, fname):
    """
    Genera la ruta de un fichero en una sesión

    Parameters
    ----------
    token_user : str
        Token de la sesión.
    fname : str
        Nombre del fichero.

    Returns
    -------
    ruta : str
        Ruta del fichero asociado a la sesión.

    """
    ruta = cte.DIR_UPLOAD_FILES + token_user + "/" + fname
    return ruta
    

# Guarda el contenido en un fichero
def save_file_proces(token_user, name_file, contenido):
    """
    Guarda un fichero por sus bytes

    Parameters
    ----------
    token_user : str
        Token de la sesión.
    name_file : str
        Nombre del fichero.
    contenido : bytes
        Contenido del fichero en bytes.

    Returns
    -------
    name_file : str
        Nombre del fichero.
    saved : bool
        True si se ha guardado, False en caso contrario.

    """
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
    """
    Descarga el contenido de un fichero desde su url

    Parameters
    ----------
    token_user : str
        Token de la sesión.
    url_file : str
        Ruta del fichero.

    Returns
    -------
    name_file : str
        Nombre del fichero.
    saved : TYPE
        True si el fichero se ha descargado, False en caso contrario.

    """
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
    """
    Convierte un strin en boolean

    Parameters
    ----------
    s : str
        String.

    Returns
    -------
    bool
        None en caso de que no sea 'True' ni 'False'.

    """
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         return None



# Borrar un fichero subido
def borrar_fichero(ruta_fichero):
    """
    Borra un fichero en el sistema

    Parameters
    ----------
    ruta_fichero : str
        Ruta del fichero a borrar.

    """
    filename, extension = os.path.splitext(ruta_fichero)
    ruta = dir_files + filename
    
    #print("** utils_ecg. borrar_fichero() -> ruta: " + ruta)
    for filename in glob.glob(ruta + "*"):
        if os.path.exists(filename):
            os.remove(filename)

    
# Comprueba si el nombre del fichero no es nulo o vacío
def name_file_valid(nombre_file):
    """
    Comprueba si el nombre del fichero no es nulo o vacío

    Parameters
    ----------
    nombre_file : str
        Nombre del fichero.

    Returns
    -------
    bool
        True si es valido, False en caso contrario.

    """
    if nombre_file is not None and nombre_file != "":
        return True
        
    return False   


def is_not_empty(string):
    """
    Comprueba si un string es vacío o nulo

    Parameters
    ----------
    string : str
        String a comprobar.

    Returns
    -------
    bool
        True si es válido, False en caso contrario.

    """
    if string is not None and string != "":
        return True
        
    return False   


def get_name_file(file_url, with_ext):
    """
    Devuelve el nombre del fichero sin extesion

    Parameters
    ----------
    file_url : str
        Ruta de un fichero.
    with_ext : bool
        True si se quiere obtener el nombre con extensión, False sin extensión.

    Returns
    -------
    filename_aux : str
        Nombre del fichero con o sin extensión.

    """
    filename_aux, extension = os.path.splitext(file_url)
    filename_aux = filename_aux.split("/")[-1]
    filename_aux = filename_aux + extension if with_ext else filename_aux
                
    return filename_aux



def get_ext_file(name_file):
    """
    Devuelve la extensión de un fichero

    Parameters
    ----------
    name_file : str
        Nombre de un fichero.

    Returns
    -------
    extension : str
        Extensión del fichero.

    """
    filename, extension = os.path.splitext(name_file)
    return extension



def convert_seg_to_hhmm(num_sec):
    """
    Devuelve las horas y minutos de acuerdo a un número de segundos

    Parameters
    ----------
    num_sec : int
        Segundos.

    Returns
    -------
    result : str
        Equivalencia en formato Horas minutos segundos.

    """
    result = ""
    hor=(int(num_sec/3600))
    minu=int((num_sec-(hor*3600))/60)
    sec = int(num_sec) / 60
    if hor != 0:
        result += str(hor)+" horas "
        
    if minu != 0:
        result += str(minu)+" min "
        
    if sec <= 1:
        result += str(num_sec) + " seg"
    
    return result


def sec_to_min(num_sec):
    """
    Transforma segundos a minutos

    Parameters
    ----------
    num_sec : int
        Segundos.

    Returns
    -------
    int
        Equivalencia en minutos.

    """
    if(num_sec > 0):
        return (num_sec // 60)
    elif num_sec == 0:
        return 0
    
    return None


# Transforma minutos a segundos
def min_to_sec(num_min):
    """
    Transforma minutos a segundos

    Parameters
    ----------
    num_min : int
        Minutos.

    Returns
    -------
    int
        Equivalencia en segundos.

    """
    if num_min > 0:
        return num_min * 60
    elif num_min == 0:
        return 0
    
    return None

    