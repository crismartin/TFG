#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 18:26:55 2020

@author: cristian
"""

from app_context import ecgDB
from app_context import app

logger = app.logger


# Bases de datos de la APP
sesiones_user = ecgDB.db.SesionesUsuario
ficheros = ecgDB.db.Ficheros
anotaciones_temp = ecgDB.db.Anotaciones_Temp

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




# Guarda o actualiza una anotacion temporal
def save_ann_temp(pt_ini, pt_actual, filename, nLead, token_session):
    fichero = get_file_user_by_name(filename, token_session)
    
    if fichero is None:
        logger.info("[db] - 'get_file_user_by_name()' -> Fichero '"  + str(filename)+ "' NO REGISTRADO")
        raise RuntimeError
            
    # compruebo si ya se ha cambiado dicho punto, buscando pt_inicial en la BBDD
    query = {
        "id_fichero": fichero["_id"],
        "nLead": nLead,
        "$or":[
            {
                "pt_inicial": {
                    "x":pt_ini["x"],
                    "y":pt_ini["y"]
                }
            },
            {
                "pt_actual": {
                    "x":pt_ini["x"],
                    "y":pt_ini["y"]
                }
            }
        ]
    }
    
    logger.info("[db] - 'save_ann_temp()' -> Antes de query para buscar anotacion")
    logger.info("[db] - 'save_ann_temp()' -> query: " + str(query))
    
    anotacion_temp = anotaciones_temp.find_one(query)
    logger.info("[db] - 'save_ann_temp()' -> anotacion_temp: " + str(anotacion_temp))
    
    if anotacion_temp is None:  #Es edicion nueva, registrar punto
        logger.info("[db] - 'save_ann_temp()' -> Es ANOTACION NUEVA")
        ann_obj = {
            "id_fichero": fichero["_id"],
            "nLead": nLead,
            "symbol":pt_ini["symbol"],
            "pt_inicial":{
                "x":pt_ini["x"],
                "y":pt_ini["y"]
            },
            "pt_actual": pt_actual
        }
        
        logger.info("[db] - 'save_ann_temp()' -> Antes de crear registro")
        id_anotacion = anotaciones_temp.insert(ann_obj)
        logger.info("[db] - 'save_ann_temp()' -> CREATED registro con id_anotacion: " + str(id_anotacion))
    else:  #Es registro antiguo, hay que actualizarlo
        query_update = { "_id": anotacion_temp["_id"] }
        new_values =  { "$set": { "pt_actual" : pt_actual} }
            
        logger.info("[db] - 'save_ann_temp()' -> Antes de actualizar registro")
        id_anotacion = anotaciones_temp.update_one(query_update, new_values)
        logger.info("[db] - 'save_ann_temp()' -> UPDATED registro COMPLETED ")
            
    return id_anotacion
    
    
    


def get_ann_by_file(filename, nLead, token_session):
    result = []
    fichero = get_file_user_by_name(filename, token_session)
    
    if fichero is None:
        logger.info("[db] - 'get_ann_by_filen()' -> Fichero '"  + str(filename)+ "' NO REGISTRADO")
        raise RuntimeError
    
    list_ann_edit = anotaciones_temp.find({"id_fichero": fichero["_id"], "nLead": nLead})
    if list_ann_edit is not None:
        for ann in list_ann_edit:
            result_file = {"pt_inicial": ann["pt_inicial"], "pt_actual": ann["pt_actual"]}
            logger.info( "[db] - 'get_ann_by_filen()' -> result_file: "  + str(result_file) )
            result.append(result_file)
    
    logger.info("[db] - 'get_ann_by_filen()' -> result: "  + str(result))
    return result


