#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 22:07:47 2020

@author: cristian
"""

from database import db
from app_context import app
from app_context import bcrypt


logger = app.logger
usuarios = db.usuarios
login_manager = app.server.login_manager


class AuthUser:
    """
    Clase repositorio con métodos para un usuario autenticado


    Methods
    -------
    insert_new_user(nick, password)
        Inserta un nuevo usuario en la base de datos
    
    get_usuario(id_usuario)
        Obtiene los datos de un usuario
        
    get_usuario_nick(id_usuario)
        Obtiene los datos de un usuario autenticado
        
    get_usuario_by_nick(nick)
        Obtiene los datos de un usuario autenticado por su nickname

    """
    
    # Inserto un usuario
    def insert_new_user(nick, password):
        """
        Da de alta un nuevo usuario desde la ventana de registro

        Parameters
        ----------
        nick : str
            Nickname del usuario a registrarse.
        password : str
            Contraseña del usuario a registrarse.

        Returns
        -------
        obj
            Objeto con los datos del usuario registrado o None si ha ocurrido un error.

        """
        try:
            logger.info("[AuthUser] - 'insert_new_user()' -> nick: " + str(nick) )
            hash_password = bcrypt.generate_password_hash(password)
            logger.info("[AuthUser] - 'insert_new_user()' -> password: " + str(hash_password) )
            id_usuario = db.insert_user(nick, hash_password)
            if id_usuario:
                return db.get_usuario(id_usuario)
        except RuntimeError:
            logger.info("[AuthUser] - 'insert_new_user()' -> Ha ocurrido un error al guardar")
        
        return None
    
    
    # Obtiene los datos de un usuario
    def get_usuario(id_usuario):
        """
        Devuelve los datos de un usuario por su id

        Parameters
        ----------
        id_usuario : str
            Id del usuario.

        Returns
        -------
        usuario : obj
            Datos del usuario.

        """
        try:
            logger.info("[AuthUser] - 'get_usuario()' -> id_usuario: " + str(id_usuario) )
            usuario = db.get_usuario(id_usuario)
            return usuario
        except RuntimeError:
            app.logger.info("[AuthUser] - 'get_usuario()' -> Ha ocurrido un error al buscar el usuario")
        
        return None
    
    
    def get_usuario_nick(id_usuario):
        """
        Devuelve el nick de un usuario

        Parameters
        ----------
        id_usuario : str
            Id del usuario.

        Returns
        -------
        str
            Nickname del usuario.

        """
        usuario = AuthUser.get_usuario(id_usuario)
        app.logger.info("[AuthUser] - 'get_usuario_nick()' -> usuario: " + str(usuario) )
        app.logger.info("[AuthUser] - 'get_usuario_nick()' -> nick: " + str(usuario.nick) )
        return usuario.nick if usuario is not None else None


    def get_usuario_by_nick(nick):
        """
        Devuelve los datos de un usuario por su nick

        Parameters
        ----------
        nick : str
            Nickname del usuario.

        Returns
        -------
        usuario : obj
            Datos del usuario.

        """
        try:
            logger.info("[AuthUser] - 'get_usuario_by_nick()' -> nick: " + str(nick) )
            usuario = db.get_usuario_by_nick(nick)
            return usuario
        except RuntimeError:
            app.logger.info("[AuthUser] - 'get_usuario_by_nick()' -> Ha ocurrido un error al buscar el usuario")
        
        return None
    

@login_manager.user_loader
def load_user(user_id):
    """
    This callback is used to reload the user object from the user ID stored 
    in the session. It should take the unicode ID of a user, and return the 
    corresponding user object (Arreglo para Flask-login)

    Parameters
    ----------
    user_id : str
        Id del usuario logado.

    Returns
    -------
    obj
        Datos del usuario en sesión.

    """
    app.logger.info("[AuthUser] - 'load_user()' -> user_id: " + str(user_id) )
    return AuthUser.get_usuario(user_id)
