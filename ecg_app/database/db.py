#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 18:26:55 2020

@author: cristian
"""

from app import ecgDB
from app import app

logger = app.logger


# Bases de datos de la APP
sesiones_user = ecgDB.db.SesionesUsuario
ficheros = ecgDB.db.Ficheros


def set_token_session(data_session):
    logger.info("'db.set_token_session()' -> data_session: " + str(data_session ) )
    
    #usuarios = ecgDB.db.Usuarios
    #usuarios.insert({"token" : str(data["token_session"]), "nick" : "cristian"})
    
    if data_session is None:
        logger.info("'db.set_token_session()' -> cargando sesion de DB" )
        token_session = sesiones_user.find_one({"nick" : "willem"})["token"]
        logger.info("'db.set_token_session()' -> token: " + str(token_session) )
        data_session = {"token_session": token_session}
    else:
        logger.info("'set_token_session()' -> return value in storage" )
   
    return data_session



# Devuelve todos los ficheros asociados a una sesion de usuario
def get_list_files_user(token_session):
    result = []
    
    usuario_sesion = check_session(token_session)
    
    lista_ficheros = ficheros.find({"id_usession": usuario_sesion["_id"]})    
    
    for file in lista_ficheros:        
        result_file = {"Id": str(file["_id"]), "Nombre": file["nombre"], "Formato": file["formato"]}
        logger.info("[db] - 'get_list_files_user()' -> result_file: "  + str(result_file) )
        result.append(result_file)
    
    return result



# Para una sesion de usuario, devuelve los datos de un fichero por su nombre
def get_file_user_by_name(filename, token_session):
    
    user_sesion = check_session(token_session)
    
    fichero = ficheros.find_one({"id_usession": user_sesion["_id"], "nombre": filename})
    logger.info("[db] - 'get_file_user_by_name()' -> fichero: "  + str(fichero) )
    
    return fichero
    


# Guarda los datos de un fichero asociados a una sesion de usuario
def insert_file_session(filename, formato, token_session):
    id_file = None
    user_sesion = check_session(token_session)    
        
    id_file = ficheros.insert({"id_usession": user_sesion["_id"], "nombre": filename, "formato": formato}) 
    logger.info("[db] - 'insert_file_session()' -> Insertado fichero con id "  + str(id_file) )
 
    return id_file



# Elimina los datos de un fichero asociados a una sesion de usuario
def delete_file_session(filename, token_session):
    
    user_sesion = check_session(token_session)
    
    result_delete = ficheros.delete_one({"id_usession": user_sesion["_id"], "nombre": filename})
    
    return True if (result_delete.acknowledged == True and result_delete.deleted_count == 1) else False        
    
    


# Funciona auxiliar para mostrar mensaje de sesion no encontrada
def check_session(token_session):
    user_sesion = sesiones_user.find_one({"token": token_session})
    if user_sesion is None:
        logger.info("[db] - 'check_session()' -> Sesion con token '"  + str(token_session)+ "' NO ENCONTRADA")
        raise RuntimeError
    
    logger.info("[db] - 'check_session()' -> Sesion con token '"  + str(token_session)+ "' ENCONTRADA")
    return user_sesion
    


    