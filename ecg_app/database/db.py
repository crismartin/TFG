#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 18:26:55 2020

@author: cristian
"""

from datetime import datetime
from app_context import app, ecgDB
from bson.objectid import ObjectId
from database.models import Usuario, Sesion, Fichero

logger = app.logger


# Bases de datos de la APP
usuarios = ecgDB.db.Usuarios
sesiones_user = ecgDB.db.SesionesUsuario
ficheros = ecgDB.db.Ficheros
anotaciones_temp = ecgDB.db.Anotaciones_Temp




# Devuelve todos los ficheros asociados a una sesion de usuario
def get_list_files_user(token_session):
    """
    Devuelve una lista de ficheros asociados a una sesión

    Parameters
    ----------
    token_session : str
        Token de la sesión de usuario.

    Returns
    -------
    result : list of obj
        Lista de los ficheros de la sesión.

    """
    result = []
    
    usuario_sesion = check_session(token_session)   

    lista_ficheros = ficheros.find({"id_usession": usuario_sesion["_id"]})
    for file in lista_ficheros:        
        result_file = Fichero( str(file["_id"]), str(file["id_usession"]), file["nombre"], file["formato"], file["f_creacion"])
        result.append(result_file.toDBCollection())
    
    logger.info("[ db ] - 'get_list_files_user()' -> Se han encontrado "  + str(len(result)) + " FICHEROS")
    logger.info("[ db ] - 'get_list_files_user()' -> FICHEROS devueltos: "  + str(result) )

    return result



# Para una sesion de usuario, devuelve los datos de un fichero por su nombre
def get_file_user_by_name(filename, token_session):
    """
    Devuelve los datos de un fichero por su nombre, asociado a una sesión.

    Parameters
    ----------
    filename : str
        Nombre del fichero.
    token_session : str
        Token de la sesión.

    Returns
    -------
    fichero : obj
        Datos del fichero.

    """
    
    user_sesion = check_session(token_session)
    
    fichero = ficheros.find_one({"id_usession": user_sesion["_id"], "nombre": filename})
    logger.info("[ db ] - 'get_file_user_by_name()' -> fichero: "  + str(fichero) )
    
    return fichero
    


# Guarda los datos de un fichero asociados a una sesion de usuario
def insert_file_session(filename, formato, token_session, f_creacion):
    """
    Guarda los datos de un fichero asociado a una sesion de usuario

    Parameters
    ----------
    filename : str
        Nombre del fichero.
    formato : str
        Formato del fichero.
    token_session : str
        Token de la sesión.
    f_creacion : str
        Fecha de la creación.

    Returns
    -------
    id_file : str
        Id del fichero guardado.

    """
    id_file = None
    user_sesion = check_session(token_session)    
        
    id_file = ficheros.insert({"id_usession": user_sesion["_id"], "nombre": filename, "formato": formato, "f_creacion": f_creacion}) 
    logger.info("[ db ] - 'insert_file_session()' -> Insertado fichero con id "  + str(id_file) )
 
    return id_file



# Elimina los datos de un fichero asociados a una sesion de usuario
def delete_file_session(filename, token_session):
    """
    Elimina los datos de un fichero asociados a una sesion de usuario

    Parameters
    ----------
    filename : str
        Nombre del fichero.
    token_session : str
        Token de la sesión.

    Returns
    -------
    bool
        True si se ha borrado correctamente, False si ha ocurrido un fallo.

    """
    
    user_sesion = check_session(token_session)
    
    result_delete = ficheros.delete_one({"id_usession": user_sesion["_id"], "nombre": filename})
    
    return True if (result_delete.acknowledged == True and result_delete.deleted_count == 1) else False     


# Elimina los ficheros de una sesion
def delete_files_session(id_sesion):
    """
    Elimina los ficheros de una sesion

    Parameters
    ----------
    id_sesion : str
        Id de la sesión.

    Returns
    -------
    bool
        True si se ha podido borrar todos los ficheros de la sesión, False si ha ocurrido un error.

    """
    id_objSesion = ObjectId(id_sesion)
    
    # Obtengo los Ids de los ficheros para eliminar las anotaciones
    ids_ficheros = ficheros.find({"id_usession": id_objSesion}).distinct('_id')
        
    result_delete_ann = anotaciones_temp.delete_many( {'id_fichero': {'$in': ids_ficheros}} )
    if result_delete_ann.acknowledged == False:
        logger.info("[ db ] - delete_files_session() -> Error al BORRAR ANOTACIONES de los FICHEROS")
        return False
    
    logger.info("[ db ] - delete_files_session() -> ANOTACIONES de FICHEROS BORRADAS!")
    
    result_delete = ficheros.delete_many({"id_usession": id_objSesion})
    if (result_delete.acknowledged == True and result_delete.deleted_count == len(ids_ficheros)):
        logger.info("[ db ] - delete_files_session() -> Los ficheros se han BORRADO CORRECTAMENTE")        
        return True 
    
    logger.info("[ db ] - delete_files_session() -> Ha ocurrido un error al BORRAR los FICHEROS")
    return False

    
    
# Elimina una lista de ficheros
def delete_files_by_id(list_files):
    """
    Elimina una lista de ficheros

    Parameters
    ----------
    list_files : list of str
        Lista con los id's de cada uno de los ficheros.

    Returns
    -------
    bool
        True si la lista se ha borrado correctamente, False si ha ocurrido un error.

    """
    id_files = []
    
    for id_file in list_files:
        id_files.append(ObjectId(id_file))
    
    logger.info("[ db ] - delete_files_by_id() -> list_files: " + str(list_files) )
    result_delete_ann = anotaciones_temp.delete_many({'id_fichero': {'$in':id_files}})
    if result_delete_ann.acknowledged == True:
        result_delete = ficheros.delete_many({'_id':{'$in':id_files}})
        if (result_delete.acknowledged == True and result_delete.deleted_count == len(list_files)):
            logger.info("[ db ] - delete_files_by_id() -> Los ficheros se han BORRADO CORRECTAMENTE")            
            return True 
        else:
            logger.info("[ db ] - delete_files_by_id() -> Ha ocurrido un error al BORRAR los FICHEROS")
            return False
    
    logger.info("[ db ] - delete_files_by_id() -> Ha ocurrido un error al BORRAR las ANOTACIONES de los FICHEROS")
    return False


# Funciona auxiliar para mostrar mensaje de sesion no encontrada
def check_session(token_session):
    """
    Comprueba si existe una sesión

    Parameters
    ----------
    token_session : str
        Token de la sesión.

    Raises
    ------
    RuntimeError
        La sesión no ha sido encontrada.

    Returns
    -------
    user_sesion : obj
        Datos de la sesión.

    """
    user_sesion = sesiones_user.find_one({"token": token_session})
    if user_sesion is None:
        logger.info("[ db ] - 'check_session()' -> Sesion con token '"  + str(token_session)+ "' NO ENCONTRADA")
        raise RuntimeError
    
    logger.info("[ db ] - 'check_session()' -> Sesion con token '"  + str(token_session)+ "' ENCONTRADA")
    return user_sesion




###############################################################################
                            ####### ANOTACIONES ######
###############################################################################


# Guarda o actualiza una anotacion temporal
def save_ann_temp(pt_ini, pt_actual, filename, nLead, token_session):
    """
    Guarda o actualiza una anotación

    Parameters
    ----------
    pt_ini : obj
        Punto inicial de la anotación con formato (x, y).
    pt_actual : obj
        Punto actual de la anotación con formato (x, y).
    filename : str
        Nombre del fichero.
    nLead : int
        Numero de la derivación del ECG.
    token_session : str
        Token de la sesión.

    Raises
    ------
    RuntimeError
        Lanzada cuando el fichero no está registrado en la BBDD.

    Returns
    -------
    id_anotacion : str
        Id de la anotación si ha ido todo bien.

    """
    fichero = get_file_user_by_name(filename, token_session)
    
    if fichero is None:
        logger.info("[ db ] - 'get_file_user_by_name()' -> Fichero '"  + str(filename)+ "' NO REGISTRADO")
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
    
    logger.info("[ db ] - 'save_ann_temp()' -> Antes de query para buscar anotacion")
    logger.info("[ db ] - 'save_ann_temp()' -> query: " + str(query))
    
    anotacion_temp = anotaciones_temp.find_one(query)
    logger.info("[ db ] - 'save_ann_temp()' -> anotacion_temp: " + str(anotacion_temp))
    
    if anotacion_temp is None:  #Es edicion nueva, registrar punto
        logger.info("[ db ] - 'save_ann_temp()' -> Es ANOTACION NUEVA")
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
        
        logger.info("[ db ] - 'save_ann_temp()' -> Antes de crear registro")
        id_anotacion = anotaciones_temp.insert(ann_obj)
        logger.info("[ db ] - 'save_ann_temp()' -> CREATED registro con id_anotacion: " + str(id_anotacion))
    else:  #Es registro antiguo, hay que actualizarlo
        query_update = { "_id": anotacion_temp["_id"] }
        new_values =  { "$set": { "pt_actual" : pt_actual} }
            
        logger.info("[ db ] - 'save_ann_temp()' -> Antes de actualizar registro")
        id_anotacion = anotaciones_temp.update_one(query_update, new_values)
        logger.info("[ db ] - 'save_ann_temp()' -> UPDATED registro COMPLETED ")
            
    return id_anotacion
    
    
    


def get_ann_by_file(filename, nLead, token_session):
    """
    Devuelve las anotaciones modificadas de un fichero

    Parameters
    ----------
    filename : str
        Nombre del fichero.
    nLead : int
        Número de derivación del ECG.
    token_session : str
        Token de la sesión donde está asociado el fichero.

    Raises
    ------
    RuntimeError
        Lanzada cuando el fichero no está registrado en la sesión.

    Returns
    -------
    result : list of obj
        Lista de anotaciones modificadas del fichero.

    """
    result = []
    fichero = get_file_user_by_name(filename, token_session)
    
    if fichero is None:
        logger.info("[ db ] - 'get_ann_by_filen()' -> Fichero '"  + str(filename)+ "' NO REGISTRADO")
        raise RuntimeError
    
    list_ann_edit = anotaciones_temp.find({"id_fichero": fichero["_id"], "nLead": nLead})
    if list_ann_edit is not None:
        for ann in list_ann_edit:
            result_file = {"pt_inicial": ann["pt_inicial"], "pt_actual": ann["pt_actual"]}
            logger.info( "[ db ] - 'get_ann_by_filen()' -> result_file: "  + str(result_file) )
            result.append(result_file)
    
    logger.info("[ db ] - 'get_ann_by_filen()' -> result: "  + str(result))
    return result




###############################################################################
                            ####### USUARIOS ######
###############################################################################


# Guarda un nuevo usuario
def insert_user(nick, password):
    """
    Crea un usuario en la colección 'Usuarios'

    Parameters
    ----------
    nick : str
        Nickname del usuario.
    password : bytes
        Contraseña codificada del usuario

    Returns
    -------
    id_usuario : str
        Id del usuario en la colección 'Usuarios'

    """
    id_usuario = None
    date_registro = datetime.now()
    fecha_registro = date_registro.strftime("%d/%m/%Y")
    
    id_usuario = usuarios.insert({"nick": nick, "password": password, "f_registro": str(fecha_registro)}) 
    id_usuario = str(id_usuario) if id_usuario is not None else None
    logger.info("[ db ] - 'insert_user()' -> Creado nuevo usuario con id "  + id_usuario )
        
    return id_usuario


# Devuelve los datos de un usuario por id
def get_usuario(id_usuario):
    """
    Devuelve los datos de un usuario por id

    Parameters
    ----------
    id_usuario : str
        Id del usuario en la colección 'Usuarios'

    Raises
    ------
    RuntimeError
        Lanzada cuando no hay un usuario registrado con id_usuario

    Returns
    -------
    usuario : obj
        Datos del usuario.

    """
    obj_id = ObjectId(id_usuario)
    usuario = usuarios.find_one({"_id": obj_id})
    if usuario is None:
        logger.info("[ db ] - 'get_usuario()' -> Usuario con id '"  + str(id_usuario)+ "' NO ENCONTRADA")
        raise RuntimeError
    
    logger.info("[ db ] - 'get_usuario()' -> Usuario con id '"  + str(id_usuario)+ "' ENCONTRADA")
    
    # Devolvemos el objeto usuario
    usuario = Usuario(str(usuario["_id"]), usuario["nick"], usuario["f_registro"], usuario["password"])
    
    return usuario


def get_usuario_by_nick(nick):
    """
    Devuelve los datos de un usuario de la colección 'Usuarios' por su nick

    Parameters
    ----------
    nick : str
        Nickname del usuario.

    Raises
    ------
    RuntimeError
        Lanzada cuando no hay un usuario registrado con id_usuario.

    Returns
    -------
    usuario : obj
        Datos del usuario.

    """
    
    usuario = usuarios.find_one({"nick": nick})
    if usuario is None:
        logger.info("[ db ] - 'get_usuario()' -> Usuario con nick '"  + str(nick)+ "' NO ENCONTRADA")
        raise RuntimeError
    
    logger.info("[ db ] - 'get_usuario()' -> Usuario con nick '"  + str(nick)+ "' ENCONTRADA")
    
    # Devolvemos el objeto usuario
    usuario = Usuario(str(usuario["_id"]), usuario["nick"], usuario["f_registro"], usuario["password"])
    
    return usuario


###############################################################################
                            ####### SESIONES ######
###############################################################################

def get_sesiones_by_user(id_usuario):
    """
    Devuelve las sesiones asociadas a un usuario

    Parameters
    ----------
    id_usuario : str
        Id del usuario de la colección 'Usuarios'

    Returns
    -------
    sesiones_result : list of obj
        Lista de las sesiones de la colección 'SesionesUsuario' asociados al usuario

    """
    sesiones_result = []
    usuario = get_usuario(id_usuario)
    obj_id = ObjectId(usuario.id)
    sesiones = sesiones_user.find({"id_usuario": obj_id})
        
    if sesiones is not None:
        for sesion in sesiones:
            sesion_result = Sesion(str(sesion["_id"]), sesion["token"] ,sesion["nombre"], sesion["f_creacion"], sesion["f_edicion"])
            logger.info( "[ db ] - 'get_sesiones_by_user()' -> sesiones_result: "  + str(sesion_result.toDBCollection()) )
            sesiones_result.append(sesion_result.toDBCollection())
    else:
        logger.info("[ db ] - 'get_sesiones_by_user()' -> El usuario con nick '"  + str(usuario.nick)+ " NO tiene SESIONES")
        
    return sesiones_result



def create_sesion(id_usuario, token_sesion, nombre_sesion, f_creacion):
    """
    Crea una sesión en la colección 'SesionesUsuario'

    Parameters
    ----------
    id_usuario : str
        Id del usuario de la colección 'Usuarios'.
    token_sesion : str
        Token de la sesión a crear.
    nombre_sesion : str
        Nombre de la sesión a crear.
    f_creacion : str
        Fecha de creación de la sesión a crear.

    Returns
    -------
    id_sesion : str
        Id de la sesión de la colección 'SesionesUsuario'

    """
    usuario = get_usuario(id_usuario)
    usuario_obj_id = ObjectId(usuario.id)
    
    id_sesion = sesiones_user.insert({"id_usuario": usuario_obj_id, 
                                      "nombre": nombre_sesion, 
                                      "token": token_sesion, 
                                      "f_creacion": str(f_creacion),
                                      "f_edicion": None}) 
    id_sesion = str(id_usuario) if id_usuario is not None else None
    logger.info("[ db ] - 'create_sesion()' -> Creada nueva sesion con id "  + id_sesion )

    return id_sesion


def update_sesion(token_session, f_edicion):
    """
    Actualiza la fecha de edición de una sesión

    Parameters
    ----------
    token_session : str
        Token de la sesión.
    f_edicion : str
        Fecha de edición.

    Raises
    ------
    RuntimeError
        Lanzada cuando la sesión con token_session no existe en la colección 'SesionesUsuario'

    Returns
    -------
    None.

    """
    sesion = sesiones_user.find_one({"token" : token_session})
    if token_session is None:
        logger.info("[ db ] - 'update_sesion()' -> La sesion con token_session '" + str(token_session) + "' NO EXISTE")
        raise RuntimeError
    
    query_update = { "_id": sesion["_id"] }
    new_values =  { "$set": { "f_edicion" : f_edicion} }
        
    logger.info("[ db ] - 'save_ann_temp()' -> Antes de actualizar registro")
    id_sesion = sesiones_user.update_one(query_update, new_values)
    if id_sesion is None:
        logger.info("[db] - 'update_sesion()' -> La sesion con token_session '" + str(token_session) + "' NO EXISTE")
        raise RuntimeError
            


def delete_sesion(id_sesion):
    """
    Borra una sesión de la colección 'SesionesUsuario'

    Parameters
    ----------
    id_sesion : str
        Id de la sesión de la colección 'SesionesUsuario'

    Returns
    -------
    bool
        True si se ha borrado correctamente, False si ha ocurrido un error

    """
    id_objSesion = ObjectId(id_sesion)
    result_delete = sesiones_user.delete_one({"_id": id_objSesion})
    return True if (result_delete.acknowledged == True and result_delete.deleted_count == 1) else False     



def get_name_sesion_by_token(token_session):
    """
    Devuelve el nombre de una sesión

    Parameters
    ----------
    token_session : str
        Token de la sesión.

    Raises
    ------
    RuntimeError
        Lanzada en caso de que no exista una sesión con token_session en la coleccción 'SesionesUsuario'

    Returns
    -------
    str
        Nombre de la sesión.

    """
    
    sesion = sesiones_user.find_one({"token": token_session})
    if sesion is None:
        logger.info("[ db ] - 'get_name_sesion_by_token()' -> No se ha encontrado ninguna sesion con el token '"+ token_session+"'")
        raise RuntimeError
    
    logger.info("[ db ] - 'get_name_sesion_by_token()' -> Sesion encontrada para el token '"+ token_session+"'")
    return sesion["nombre"]
