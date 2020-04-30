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
    
    # Inserto un usuario
    def insert_new_user(nick, password):
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
        try:
            logger.info("[AuthUser] - 'get_usuario()' -> id_usuario: " + str(id_usuario) )
            usuario = db.get_usuario(id_usuario)
            return usuario
        except RuntimeError:
            app.logger.info("[AuthUser] - 'get_usuario()' -> Ha ocurrido un error al buscar el usuario")
        
        return None
    
    
    def get_usuario_nick(id_usuario):
        usuario = AuthUser.get_usuario(id_usuario)
        app.logger.info("[AuthUser] - 'get_usuario_nick()' -> usuario: " + str(usuario) )
        app.logger.info("[AuthUser] - 'get_usuario_nick()' -> nick: " + str(usuario.nick) )
        return usuario.nick if usuario is not None else None


    def get_usuario_by_nick(nick):
        try:
            logger.info("[AuthUser] - 'get_usuario_by_nick()' -> nick: " + str(nick) )
            usuario = db.get_usuario_by_nick(nick)
            return usuario
        except RuntimeError:
            app.logger.info("[AuthUser] - 'get_usuario_by_nick()' -> Ha ocurrido un error al buscar el usuario")
        
        return None
    

@login_manager.user_loader
def load_user(user_id):
    app.logger.info("[AuthUser] - 'load_user()' -> user_id: " + str(user_id) )
    return AuthUser.get_usuario(user_id)
