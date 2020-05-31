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
    """
    Componente que se devolverá en el navbar cuando un usuario se haya logado

    Parameters
    ----------
    nombre_user : str
        Nickname del usuario.

    Returns
    -------
    logged_user : obj
        Componente con los datos del usuario logado.

    """
    
    logged_user = dbc.DropdownMenu(
                        nav=True,
                        in_navbar=True,
                        label="Welcome " + nombre_user,
                        children=[
                            dbc.DropdownMenuItem(children=[html.Span([html.I(className="fa fa-user"), " Ver perfil"])], href="/user/profile"),
                            dbc.DropdownMenuItem(children=[html.Span([html.I(className="fa fa-power-off"), " Cerrar sesión"])], href="/logout"),
                        ],
                    )
    return logged_user


def nologged_component():
    """
    Componente que se devolverá en el navbar cuando un usuario no se haya logado (por defecto)

    Returns
    -------
    nologed_user : TYPE
        Componente con los datos por defecto.

    """
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