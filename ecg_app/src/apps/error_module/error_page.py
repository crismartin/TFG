#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 20:57:00 2020

@author: cristian
"""
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc


from app_context import app
import dash_html_components as html
import dash_bootstrap_components as dbc



# Página de sesion errónea
session_error_layout = dbc.Jumbotron(
        [
            html.H1(children=html.Span([html.I(className="fa fa-exclamation-triangle"), " Sesión No Encontrada"]), className="display-3"),
            html.Hr(className="my-2"),
            html.H5(
                "La sesión a la que ha querido acceder no existe en su perfil."
            ),
            html.H5(
                "Vuelva a su perfil e inténtelo de nuevo."
            ),
            html.P(dbc.Button(id="se-btn-perfil", children=html.Span([html.I(className="fa fa-user"), " Volver al perfil"]), 
                              color="primary"), className="lead text-right"),
        ], className="text-center"
)

url_sesion_error= dcc.Location(id='url_sesion_error',   refresh=True)



class SessionError:
    """
    Clase que contiene los métodos para los componentes de la página de SesionError
    
    """
    
    @app.callback(
        Output("url_sesion_error", "pathname"),
        [Input("se-btn-perfil", "n_clicks")]
    )
    def redirect_profile(btn):
        """
        Redirige la pantalla de perfil de usuario cuando se clica en el botón "Volver al perfil"

        """
        if btn:
            return "/user/profile"
    
    
    @staticmethod
    def layout():
        return html.Div([session_error_layout, url_sesion_error])

