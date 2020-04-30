#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:47:58 2019

@author: cristian
"""

import dash_html_components as html
import dash_bootstrap_components as dbc
import src.apps.auth_module.login_page as login_page
import src.apps.auth_module.signin_page as signin_page



###############################################################################
                      ########## COMPONENTES ##########
###############################################################################

def logged_component(nombre_user):
    
    logged_user = dbc.DropdownMenu(
                        nav=True,
                        in_navbar=True,
                        label="Bienvenido " + nombre_user,
                        children=[
                            dbc.DropdownMenuItem(children=[html.Span([html.I(className="fa fa-user"), " Ver perfil"])], href="/perfil"),
                            dbc.DropdownMenuItem(children=[html.Span([html.I(className="fa fa-power-off"), " Cerrar sesión"])], href="/logout"),
                        ],
                    )
    return logged_user


def nologged_component():
    nologed_user = [dbc.NavItem(children=dbc.Button(id="btn-login", 
                                                    children=[html.Span([html.I(className="fa fa-power-off"), " Iniciar sesión"])],  
                                                    color="link") 
                                ),
                    dbc.NavItem(children=dbc.Button(id="btn-signin", 
                                                    children=[html.Span([html.I(className="fa fa-pencil-square-o"), " Registrarse"])], 
                                                    color="link") 
                                )
                    ]
    return nologed_user



def layout():
    return html.Div([
                login_page.layout(),
                signin_page.layout()
            ])