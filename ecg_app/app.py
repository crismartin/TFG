#!/usr/bin/env python2
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

stylesheets = [dbc.themes.BOOTSTRAP, 
               "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
               "https://use.fontawesome.com/releases/v5.7.2/css/all.css"]

server = flask.Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=stylesheets)
logging.basicConfig(filename="ecgApp.log", level=logging.DEBUG, 
                    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
app.title = "ECGApp"


CACHE_CONFIG={
    'CACHE_TYPE':'simple',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL','localhost:6379')
}

cache=Cache()
cache.init_app(server,config=CACHE_CONFIG)


app.config.supress_callback_exceptions = True
app.css.config.serve_locally=True
app.scripts.config.serve_locally=True