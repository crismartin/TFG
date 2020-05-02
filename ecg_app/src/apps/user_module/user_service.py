#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 01:43:25 2020

@author: cristian
"""

import src.commons.utils_ecg as utils
from database import db
from app_context import app

logger = app.logger


def get_sesiones_by_user(id_usuario):
    try:
        sesiones = db.get_sesiones_by_user(id_usuario)
        return sesiones
    
    except RuntimeError:
            logger.info("[user_service] - 'get_sesiones_by_user()' -> Ha ocurrido un error al guardar")
        
    return None


def check_sesion(token_session):
    try:
        db.check_session(token_session)
        return token_session
    except RuntimeError:
        logger.info("[user_service] - 'check_sesion()' -> No se ha encontrado la sesión con token: " + str(token_session))
        
    return None


def set_session(token_session):
    data_session = None
    token_session = check_sesion(token_session)

    if token_session is not None:
        data_session = {"token_session": token_session}
    
    return data_session


#Crea una nueva sesion para un usuario
def create_sesion(id_usuario, nombre_sesion):
    result = "0"
    try:
        token_sesion = utils.generateNewTokenSession()
        f_creacion = utils.getCurrentStringDate(None)
        id_sesion = db.create_sesion(id_usuario, token_sesion, nombre_sesion, f_creacion)
        if id_sesion is not None:
            # creo el directorio para que el usuario guarde los ficheros
            utils.create_new_user_dir(token_sesion)
        result = "1" if id_sesion is not None else result
    except RuntimeError:
        logger.info("[user_service] - 'create_sesion()' -> No se ha creado la sesión con nombre: " + str(nombre_sesion))
    
    return result


#Actualiza la fecha de ultima edicion de la sesion
def update_sesion(token_sesion):
    try:
        f_edicion = utils.getCurrentStringDate(None)
        db.update_sesion(token_sesion, f_edicion)        
    except RuntimeError:
        app.logger.info("[ecg_service] - 'update_sesion()' -> Ha ocurrido un error al actualizar la fecha de la sesion")
    