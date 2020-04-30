#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 20:55:03 2020

@author: cristian
"""
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc


from app_context import app

jumbotron = dbc.Jumbotron(
    [
        html.H1("Hasta la próxima!", className="display-3"),
        html.Hr(className="my-2"),
        html.H5(
            "Se ha cerrado la sesión"
        ),
        html.P(dbc.Button(id="btn_gohome", children=html.Span([html.I(className="fa fa-home ml-2"), " Volver al inicio"]), 
                          color="primary"), className="lead text-right"),
    ], className="text-center"
)


login_url = dcc.Location(id='url_logout',   refresh=True)


@app.callback(
    Output("url_logout",  "pathname"),
    [Input("btn_gohome",  "n_clicks")]
)
def go_home(click_btn):
    if click_btn:
        return "/"


def layout():
    return html.Div([jumbotron,login_url ])