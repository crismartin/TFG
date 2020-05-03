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



###############################################################################
## SESIONES 
###############################################################################

def get_sesiones_by_user(id_usuario):
    try:
        sesiones = db.get_sesiones_by_user(id_usuario)
        return sesiones
    
    except RuntimeError:
            logger.info("[ user_service ] - 'get_sesiones_by_user()' -> Ha ocurrido un error al guardar")
        
    return None


def check_sesion(token_session):
    try:
        db.check_session(token_session)
        return token_session
    except RuntimeError:
        logger.info("[ user_service ] - 'check_sesion()' -> No se ha encontrado la sesión con token: " + str(token_session))
        
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
        logger.info("[ user_service ] - 'create_sesion()' -> No se ha creado la sesión con nombre: " + str(nombre_sesion))
    
    return result


#Actualiza la fecha de ultima edicion de la sesion
def update_sesion(token_sesion):
    try:
        f_edicion = utils.getCurrentStringDate(None)
        db.update_sesion(token_sesion, f_edicion)        
    except RuntimeError:
        app.logger.info("[ user_service ] - 'update_sesion()' -> Ha ocurrido un error al actualizar la fecha de la sesion")



def borrar_sesion(sesion):    
    id_sesion = sesion["id"]
    token_sesion = sesion["token"]
    
    # Borrar de BBDD los ficheros de la sesion
    app.logger.info("[ user_service ] - 'borrar_sesion()' -> Iniciando BORRADO de SESION")
    app.logger.info("[ user_service ] - 'borrar_sesion()' -> id_sesion: " + str(id_sesion))
    app.logger.info("[ user_service ] - 'borrar_sesion()' -> token_session: " + str(token_sesion))
    app.logger.info("[ user_service ] - 'borrar_sesion()' -> Borrando FICHEROS de SESION")
    
    result_del_files = db.delete_files_session(id_sesion)
    if result_del_files is False:        
        app.logger.info("[ user_service ] - 'borrar_sesion()' -> Ha ocurrido un ERROR al intentar borrar los FICHEROS de SESION")
        return False
    
    app.logger.info("[ user_service ] - 'borrar_sesion()' -> Borrado FICHEROS de SESION SUCESS!")
    
    # Borrar de BBDD la sesion
    app.logger.info("[ user_service ] - 'borrar_sesion()' -> Borrando SESION BBDD")
    result_del_ses = db.delete_sesion(id_sesion)
    if result_del_ses is False:
        app.logger.info("[ user_service ] - 'borrar_sesion()' -> Ha ocurrido un ERROR al intentar borrar la SESION de BBDD")
        return False
        
    app.logger.info("[ user_service ] - 'borrar_sesion()' -> Borrado de SESION BBDD SUCESS!")
    
    # Si todo ha ido bien, borrar la sesion del sys
    app.logger.info("[ user_service ] - 'borrar_sesion()' -> Borrando SESION SYS")    
    result_del_sys = utils.remove_dir(token_sesion)
    if result_del_sys is False:
        app.logger.info("[ user_service ] - 'borrar_sesion()' -> Ha ocurrido un ERROR al intentar borrar la SESION de SYS")
        return False
        
    app.logger.info("[ user_service ] - 'borrar_sesion()' -> Borrado de SESION SYS SUCESS!")
    return True
###############################################################################
## FICHEROS 
###############################################################################

# Elimina los ficheros del sistema
def delete_files_system(token_session, list_files):
    
    for file in list_files:
        ruta_fichero = token_session + "/" + file["nombre"]
        utils.borrar_fichero(ruta_fichero)


# Elimina de la BBDD los ficheros seleccionados
def delete_files_by_id(list_files):
    result = False
    try:
        result = db.delete_files_by_id(list_files)
    except RuntimeError:
        app.logger.info("[ user_service ] - 'delete_files_by_id()' -> Ha ocurrido un error al intentar eliminar los ficheros" )
    
    return result     


# Elimina los ficheros seleccionados
def delete_files_selected(token_session, list_files):
    list_id_files = []
    app.logger.info( "[ user_service ] - 'delete_files_selected()' -> Borrar ficheros: " + str(list_files))
    if list_files is not None and list_files != []:
        for file in list_files:
            list_id_files.append(file["id"])
        
        app.logger.info("[ user_service ] - 'delete_files_selected()' -> Pre borrado en BBDD..." )
        result = delete_files_by_id(list_id_files)

        if result is True:
            app.logger.info("[ user_service ] - 'delete_files_selected()' -> Pre borrado en SYS..." )
            delete_files_system(token_session, list_files)
            app.logger.info("[ user_service ] - 'delete_files_selected()' -> Borrado COMPLETED!" )
            return True
        
    return False      
