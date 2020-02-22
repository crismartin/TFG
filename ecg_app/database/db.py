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
usuarios = ecgDB.db.Usuarios
ficheros = ecgDB.db.Ficheros


def set_token_session(data_session):
    logger.info("'db.set_token_session()' -> data_session: " + str(data_session ) )
    
    #usuarios = ecgDB.db.Usuarios
    #usuarios.insert({"token" : str(data["token_session"]), "nick" : "cristian"})
    
    if data_session is None:
        logger.info("'db.set_token_session()' -> cargando sesion de DB" )
        token_session = usuarios.find_one({"nick" : "willem"})["token"]
        logger.info("'db.set_token_session()' -> token: " + str(token_session) )
        data_session = {"token_session": token_session}
    else:
        logger.info("'set_token_session()' -> return value in storage" )
   
    return data_session


def get_list_files_user(token_session):
    usuario_sesion = usuarios.find_one({"token": token_session})
    logger.info("[db] - 'get_list_files_user()' -> usuario_sesion: "  + str(usuario_sesion) )
    lista_ficheros = ficheros.find({"id_usuario": usuario_sesion["_id"]})
    
    result = []
    for file in lista_ficheros:        
        result_file = {"Id": str(file["_id"]), "Nombre": file["nombre"], "Formato": file["formato"]}
        logger.info("[db] - 'get_list_files_user()' -> result_file: "  + str(result_file) )
        result.append(result_file)
    
    return result


def insert_file_session(token_session):
    usuario_sesion = usuarios.find_one({"token": token_session})
    id_file = ficheros.insert({"id_usuario": usuario_sesion["_id"], "nombre": "100", "formato": "Physionet"})
    
    return id_file
    