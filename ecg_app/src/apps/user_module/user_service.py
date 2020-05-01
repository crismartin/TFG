#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 01:43:25 2020

@author: cristian
"""

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