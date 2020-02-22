#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 18:39:09 2020

@author: cristian
"""


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
    

class Usuarios:
    
    def __init__(self, token, nick):
        self.token = token
        self.nick = nick
        
    def toDBCollection(self):
        return {
            "token" : self.token,
            "nick" : self.nick
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
    