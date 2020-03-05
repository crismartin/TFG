#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:39:33 2019

@author: cristian
"""
import flask
import dash
import dash_bootstrap_components as dbc
import os
import logging
from flask_caching import Cache
from flask_pymongo import PyMongo
from flask_mail import Mail

stylesheets = [dbc.themes.BOOTSTRAP, 
               "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
               "https://use.fontawesome.com/releases/v5.7.2/css/all.css"]


# Declaracion del servidor
server = flask.Flask(__name__,static_folder="src/static")


# Declaracion del fichero de log
logging.basicConfig(filename="logs/ecgApp.log", level=logging.DEBUG, 
                    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")


# Configuracion de la BBDD en el server
server.config['MONGO_HOST'] = 'localhost'
server.config['MONGO_PORT'] = '27017'
server.config['MONGO_DBNAME'] = 'EcgDB'
server.config['MONGO_USERNAME'] = 'hexxa'
server.config['MONGO_PASSWORD'] = '1708bilens'
server.config['MONGO_AUTH_SOURCE'] = 'admin'
server.config["MONGO_URI"] = "mongodb://localhost:27017/EcgDB"
                            
ecgDB = PyMongo(server)

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "vnitlasmeo@gmail.com",
    "MAIL_PASSWORD": "o1@txa7@k0mor"
}

server.config.update(mail_settings)
mail = Mail(server)


# Configuracion de la Cache del server
CACHE_CONFIG={
    'CACHE_TYPE':'simple',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL','localhost:6379')
}

cache=Cache()
cache.init_app(server,config=CACHE_CONFIG)

# Propiedades de la APP

app = dash.Dash(server=server, external_stylesheets=stylesheets)
app.title = "ECGApp"
app.config.supress_callback_exceptions = True
app.css.config.serve_locally=True
app.scripts.config.serve_locally=True


