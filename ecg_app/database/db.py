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