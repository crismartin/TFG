#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 18:39:09 2020

@author: cristian
"""
from flask_login import UserMixin as UserMixin

class Punto:
    """
    Entidad de un punto con coordenadas rectangulares.
        
    Attributes
    ----------
    x : str
        Coordenada en x
        
    y : str
        Coordenada en y
        
    symbol : str
        Simbolo del punto
        
        
    Methods
    -------
    toDBCollection(self)
        Devuelve el objeto en formato JSON para guardar en BBDD
    """
    
    def __init__(self, x, y, symbol):
        self.x = x
        self.y= y
        self.symbol = symbol
        
    def toDBCollection(self):
        """
        Devuelve el objeto en formato JSON

        Returns
        -------
        Objeto en formato JSON

        """
        return{
            "x": self.x,
            "y": self.y,
            "symbol": self.symbol
        }
    

class Usuario(UserMixin):
    """
    Entidad de un usuario que extiende de la clase UserMixin para la autenticación
        
    Attributes
    ----------
    
    id: str
        Id del usuario
    
    nick : str
        Nickname del usuario
        
    f_registro : str
        Fecha de registro del usuario
        
    password : str
        Contraseña del usuario
        
        
    Methods
    -------
    toDBCollection(self)
        Devuelve el objeto en formato JSON para guardar en BBDD
    """
    
    def __init__(self, token, nick, f_registro, password):
        self.id = token
        self.nick = nick
        self.password = password
        self.f_registro = f_registro
    
    
    def toDBCollection(self):
        """
        Devuelve el objeto en formato JSON

        Returns
        -------
        Objeto en formato JSON

        """
        return {
            "_id" : self.token,
            "nick" : self.nick,
            "f_registro" : self.f_registro,
            "password": self.password
        }
    
    
class Fichero:
    """
    Entidad de un fichero asociado a una sesión
        
    Attributes
    ----------
    
    id: str
        Id del fichero
    
    id_sesion : str
        Id de la sesión asociado a la colección 'SesionesUsuario'
        
    nombre : str
        Nombre del fichero
        
    formato : str
        Formato del fichero
    
    f_creacion : str
        Fecha de creación del fichero
        
    Methods
    -------
    toDBCollection(self)
        Devuelve el objeto en formato JSON para guardar en BBDD    
    """
    
    def __init__(self, id_file, id_sesion, nombre, formato, f_creacion ):
        self.id = id_file
        self.id_sesion = id_sesion
        self.nombre = nombre
        self.formato = formato
        self.f_creacion = f_creacion
        
    def toDBCollection(self):
        """
        Devuelve el objeto en formato JSON

        Returns
        -------
        Objeto en formato JSON

        """
        return {
            "id": self.id,
            "id_sesion": self.id_sesion,
            "nombre": self.nombre,
            "formato": self.formato,
            "f_creacion": self.f_creacion            
        }
    
    
class Anotacion:
    """
    Entidad de una anotación asociada a una derivación de un fichero
        
    Attributes
    ----------
    
    id_fichero: str
        Id del fichero de la colección 'Ficheros'
    
    n_lead : int
        Número de la derivación
        
    pt_inicial : obj of Punto
        Punto inicial de la anotación (dato obtenido del fichero)
        
    pt_actual : obj of Punto
        Punto actual de la anotación
    
    
    Methods
    -------
    toDBCollection(self)
        Devuelve el objeto en formato JSON para guardar en BBDD
    
    """
    
    def __init__(self, id_fichero, n_lead, pt_default, pt_actual):
        self.id_fichero= id_fichero
        self.n_lead = n_lead
        self.pt_inicial = pt_default
        self.pt_actual = pt_actual
        
    def toDBCollection(self):
        """
        Devuelve el objeto en formato JSON

        Returns
        -------
        Objeto en formato JSON

        """
        return{
            "id_fichero" : self.id_fichero,
            "n_lead": self.n_lead,
            "pt_inicial": self.pt_inicial,
            "pt_actual": self.pt_actual            
        }


class Sesion:
    """
    Entidad de una sesión
        
    Attributes
    ----------
    
    id: str
        Id de la sesión en la colección 'SesionesUsuario'
    
    token : str
        Token de la sesión
        
    nombre : str
        Nombre de la sesión
        
    f_creacion : str
        Fecha de creación de la sesión
    
    f_edicion : str
        Fecha de edición de la sesión
    
    
    Methods
    -------
    toDBCollection(self)
        Devuelve el objeto en formato JSON para guardar en BBDD
    
    """
    
    def __init__(self, id_sesion, token, nombre, f_creacion, f_edicion):
        self.id = id_sesion
        self.token = token
        self.nombre = nombre
        self.f_creacion = f_creacion
        self.f_edicion = f_edicion
        
    def toDBCollection(self):
        """
        Devuelve el objeto en formato JSON

        Returns
        -------
        Objeto en formato JSON

        """
        return{
            "id" : self.id,
            "token": self.token,
            "nombre": self.nombre,
            "f_creacion": self.f_creacion,
            "f_edicion": self.f_edicion            
        }    