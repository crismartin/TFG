#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 18:39:09 2020

@author: cristian
"""
from flask_login import UserMixin as UserMixin

class Punto:
    
    def __init__(self, x, y, symbol):
        self.x = x
        self.y= y
        self.symbol = symbol
        
    def toDBCollection(self):
        return{
            "x": self.x,
            "y": self.y,
            "symbol": self.symbol
        }
    

class Usuario(UserMixin):
    
    def __init__(self, token, nick, f_registro, password):
        self.id = token
        self.nick = nick
        self.password = password
        self.f_registro = f_registro
    
    
    def toDBCollection(self):
        return {
            "_id" : self.token,
            "nick" : self.nick,
            "f_registro" : self.f_registro,
            "password": self.password
        }
    
    
class Fichero:
    
    def __init__(self, id_file, id_sesion, nombre, formato, f_creacion ):
        self.id = id_file
        self.id_sesion = id_sesion
        self.nombre = nombre
        self.formato = formato
        self.f_creacion = f_creacion
        
    def toDBCollection(self):
        return {
            "id": self.id,
            "id_sesion": self.id_sesion,
            "nombre": self.nombre,
            "formato": self.formato,
            "f_creacion": self.f_creacion            
        }
    
    
class Anotacion:
    
    def __init__(self, id_user_file, n_lead, pt_default, pt_actual):
        self.id_user_file= id_user_file
        self.n_lead = n_lead
        self.pt_default = pt_default
        self.pt_actual = pt_actual
        
    def toDBCollection(self):
        return{
            "id_user_file" : self.id_user_file,
            "n_lead": self.n_lead,
            "pt_default": self.pt_default,
            "pt_actual": self.pt_actual            
        }


class Sesion:
    
    def __init__(self, id_sesion, token, nombre, f_creacion, f_edicion):
        self.id = id_sesion
        self.token = token
        self.nombre = nombre
        self.f_creacion = f_creacion
        self.f_edicion = f_edicion
        
    def toDBCollection(self):
        return{
            "id" : self.id,
            "token": self.token,
            "nombre": self.nombre,
            "f_creacion": self.f_creacion,
            "f_edicion": self.f_edicion            
        }    