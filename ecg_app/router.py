#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:43:27 2019

@author: cristian
"""

from dash.dependencies import Input, Output, State
from app_context import app

import src.apps.ecg_module.ecg_page as ecg_page
import src.apps.index as index_page

import src.apps.ecg_module.ecg_service as ecg_serv

from flask_mail import Message
from app_context import mail
from app_context import server



app.layout = index_page.layout()



@app.callback([Output("page-content",   "children"),
               Output("session",        "data")],
              [Input("url",             "pathname")],
              [State("session",         "data")]
)
def route_page(pathname, data):
    
    if pathname == "/":
        """
        msg = Message(subject="Hello",
                      sender=server.config.get("MAIL_USERNAME"),
                      recipients=["emilytecnokent@gmail.com"], # replace with your email for testing
                      body="This is a test email I sent with Gmail and Python!")
        mail.send(msg)
        """
        
    if pathname == '/ecg':
        data = ecg_serv.set_token_session(data)
        #app.logger.info("'set_token_session()' -> data:"  + str(data["token_session"]) )
        
        # guardo el token del usuario
        #usuarios = ecgDB.db.Usuarios
        #usuarios.insert({"token" : str(data["token_session"]), "nick" : "cristian"})
        
        return [ecg_page.layout(), data]
    
    return [None, data]

