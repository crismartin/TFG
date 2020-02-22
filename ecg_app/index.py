#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:43:27 2019

@author: cristian
"""

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app
from apps import ecg_page
import os
from flask import send_from_directory
import utils_ecg as utils
from database import db



navbar = dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Link", href="/")),
                dbc.DropdownMenu(
                    nav=True,
                    in_navbar=True,
                    label="Menu",
                    children=[
                        dbc.DropdownMenuItem("Entry 1"),
                        dbc.DropdownMenuItem("Entry 2"),
                        dbc.DropdownMenuItem(divider=True),
                        dbc.DropdownMenuItem("Entry 3"),
                    ],
                ),
            ],
            brand="ECG App",
            brand_href="/ecg",
            sticky="top",
        )

store_session = dcc.Store(id='session', storage_type='session')

app.layout=html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content'),
    store_session
])





@app.callback([Output("page-content", "children"),
               Output("session", "data")],
              [Input("url", "pathname")],
              [State("session", "data")]
)
def display_page(pathname, data):
    if pathname == '/ecg':
        data = db.set_token_session(data)
        #app.logger.info("'set_token_session()' -> data:"  + str(data["token_session"]) )
        
        # guardo el token del usuario
        #usuarios = ecgDB.db.Usuarios
        #usuarios.insert({"token" : str(data["token_session"]), "nick" : "cristian"})
        
        return [ecg_page.layout(), data]

    return [None, data]




@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


@app.server.route('/assets/<path:path>')
def assets_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


server = app.server

if __name__ == '__main__':
    app.server.run(host='0.0.0.0', port=8050, debug=True)