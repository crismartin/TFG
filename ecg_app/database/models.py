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
    
    def __init__(self, token, nick, password):
        self.id = token
        self.nick = nick
        self.password = password
        
    
    def toDBCollection(self):
        return {
            "_id" : self.token,
            "nick" : self.nick,
            "password": self.password
        }
    
    
class FicherosUsuario:
    
    def __init_(self, id_user, name_file):
        self.id_user = id_user
        self.name_file = name_file
        
    def toDBCollection(self):
        return {
            "id_user": self.id_user,
            "name_file": self.name_file
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
    