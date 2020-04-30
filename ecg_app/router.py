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
import src.apps.auth_module.auth_page as auth_page
import src.apps.auth_module.logout_page as logout_page

import src.apps.ecg_module.ecg_service as ecg_serv
from flask_login import login_user, logout_user, current_user

"""
from flask_mail import Message
from app_context import mail
from app_context import server
"""


app.layout = index_page.layout()
logger = app.logger


@app.callback([Output("page-content",   "children"),
               Output("session",        "data")],
              [Input("url",             "pathname")],
              [State("session",         "data")]
)
def route_page(pathname, data):
    logger.info("[router] - route_page() -> ENTRO AQUI")
    if pathname == "/":
        """
        msg = Message(subject="Hello",
                      sender=server.config.get("MAIL_USERNAME"),
                      recipients=["emilytecnokent@gmail.com"], # replace with your email for testing
                      body="This is a test email I sent with Gmail and Python!")
        mail.send(msg)
        """
    
    if pathname == "/logout":
        if current_user.is_authenticated:
            return [logout_page.layout(), None]
        
    if pathname == '/ecg':
        data = ecg_serv.set_token_session(data)
        #app.logger.info("'set_token_session()' -> data:"  + str(data["token_session"]) )
        
        # guardo el token del usuario
        #usuarios = ecgDB.db.Usuarios
        #usuarios.insert({"token" : str(data["token_session"]), "nick" : "cristian"})
    
        return [ecg_page.layout(), data]
    
        
    return [None, data]



@app.callback(Output("nav-auth",   "children"),
              [Input("url",        "pathname")]
)
def auth_route(pathname):
    logger.info("[router] - auth_route() -> ENTRO AQUI")
    if pathname == "/success" or pathname == "/" or pathname == "/perfil":
        if current_user.is_authenticated:
            logged_navbar = auth_page.logged_component(current_user.nick)
            return logged_navbar
    
    if pathname == "/logout":
        if current_user.is_authenticated:
            logout_user()
            return auth_page.nologged_component()
    
    return auth_page.nologged_component()
    