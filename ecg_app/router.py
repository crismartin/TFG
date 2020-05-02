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
import src.apps.user_module.perfil_page as perfil_page
from src.apps.error_module.error_page import SessionError


import src.apps.user_module.user_service as user_service

from flask_login import login_user, logout_user, current_user
from flask import request

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
    
    if pathname:
        logger.info("[ router ] - route_page() -> ENTRO AQUI con PATHNAME: " + pathname)
        
        if pathname == "/":
            """
            msg = Message(subject="Hello",
                          sender=server.config.get("MAIL_USERNAME"),
                          recipients=["emilytecnokent@gmail.com"], # replace with your email for testing
                          body="This is a test email I sent with Gmail and Python!")
            mail.send(msg)
            """
        if current_user.is_authenticated:
            if pathname == "/user/profile":
                app.logger.info("[ router ] - route_page() -> /user/profile")                 
                return [perfil_page.layout(), None]
            
            if pathname == "/logout":                
                return [logout_page.layout(), None]
                
            if pathname.startswith('/ecg/sesion/'):                
                token_session = "session_"+pathname.split('/')[-1]
                app.logger.info("'set_token_session()' -> token_session: "+ str(token_session))
    
                data = user_service.set_session(token_session)
                if data is not None:
                    return [ecg_page.layout(), data]
                else:
                    return [SessionError.layout(), data]
    
    return [None, data]



@app.callback(Output("nav-auth",   "children"),
              [Input("url",        "pathname")]
)
def auth_route(pathname):
    
    if pathname:
        if pathname == "/logout":
            if current_user.is_authenticated:
                logout_user()
                return auth_page.nologged_component()
        else:         
             if current_user.is_authenticated:
                 logger.info("[ router ] - route_page() -> current_user: " + str(current_user))
                 logged_navbar = auth_page.logged_component(current_user.nick)
                 return logged_navbar
    
    return auth_page.nologged_component()
    