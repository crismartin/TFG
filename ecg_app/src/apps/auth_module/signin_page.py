#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:47:58 2019

@author: cristian
"""
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask_login import login_user, logout_user, current_user

import src.commons.utils_ecg as utils
from database.authUser import AuthUser

import time
from app_context import app


#######################################
##### FORMULARIO MODAL REGISTRO
#######################################

email_input = dbc.FormGroup(
    [
        dbc.Label("Nick", html_for="msignin-nick"),
        dbc.Input(type="text", id="msignin-nick", placeholder="Enter nick", maxlength = "20", debounce=True),        
    ]
)

password_input = dbc.FormGroup(
    [
        dbc.Label("Password", html_for="msignin-password"),
        dbc.Input(
            type="password",
            id="msignin-pass",
            placeholder="Enter password",
            debounce=True
        ),
    ]
)

btn_cerrar_msignin = dbc.Button(id="msignin-close", n_clicks=None, className="mr-1",
                              children=[
                                html.Span([html.I(className="fa fa-times ml-2"), " Cancelar"])
                             ])

btn_entrar_msignin = dbc.Button(id="msignin-enter", color="success", 
                          children=[
                                html.Span([html.I(className="fa fa-check"), " Registrarte"])
                             ], disabled=True)

form_signin = dbc.Form(id="form-signin", children=[email_input, password_input])


alert_error_signin = dbc.Alert(id="al-error-signin", children=[
                                html.Span([html.I(className="fa fa-exclamation-triangle"), " Error: el nick introducido no está disponible"])
                             ], color="danger", is_open=False)



alert_success = dbc.Alert(id="al-success-signin", children=[html.P("Registrado correctamente!"),
                                html.Span([dbc.Spinner(color="success", size="sm"), "  Iniciando sesión..."])
                             ], color="success", is_open=False)

alerts_modal_signin = html.Div(children=[alert_error_signin, alert_success])

cnt_alert_error = html.Div(id="cnt-alerts-signin", children=alerts_modal_signin)


modal_signin = html.Div([
    dbc.ModalHeader(children=[html.Span([html.I(className="fa fa-pencil-square-o"), " Registrarse"])]),
    dbc.ModalBody(id="msignin-body", children=[
        form_signin,
        cnt_alert_error
    ]),

    dbc.ModalFooter([
        html.Div( id="cnt-msignin-cerrar",  children=btn_cerrar_msignin ),
        html.Div( id="cnt-msignin-entrar",  children=btn_entrar_msignin )
    ]),
    
])

modales_logueo =  html.Div([dbc.Modal(id = "msignin",
                             children = modal_signin,
                             size = "sm",
                             backdrop = "static")])

signin_url = dcc.Location(id='url_signin',  refresh=True)




###############################################################################
                       ########## CALLBACKS ##########
###############################################################################

@app.callback(
    Output("cnt-alerts-signin", "children"),
    [Input("msignin-nick",      "n_blur"),
     Input("msignin-pass",      "n_blur")],
)
def set_error_alert_signin(input1, input2):    
    return alerts_modal_signin


@app.callback(
    Output("msignin",        "is_open"),     
    [Input("btn-signin",     "n_clicks"),
     Input("msignin-close",  "n_clicks")],
    [State("msignin",        "is_open")],
)
def toggle_modal_signin(open_click, close_click, is_open):
    
    if (open_click or close_click):
        return not is_open    
    return is_open



@app.callback(
    [Output("al-error-signin",   "is_open"),
     Output("al-success-signin", "is_open")],
    [Input("msignin-enter",      "n_clicks")],     
    [State("msignin-nick",       "value"),
     State("msignin-pass",       "value")],
)
def signin_usuario(btn_signin, nick, password):
    show_alert_error = True
    
    if nick is None and password is None:
        raise dash.exceptions.PreventUpdate()
    
    # Compruebo si el nick de usuario ya esta registrado
    app.logger.info("@callback[ signin_page ]: 'signin_usuario()' -> Buscando usuario con NICK: " + str(nick))
    usuario_registered = AuthUser.get_usuario_by_nick(nick)
    if usuario_registered is None:
        app.logger.info("@callback[ signin_page ]: 'signin_usuario()' -> Es usuario NUEVO")
        # Hago el insert en la BBDD para obtener el token de usuario
        app.logger.info("@callback[ signin_page ]: 'signin_usuario()' -> REGISTRANDO usuario")
        usuario = AuthUser.insert_new_user(nick, password)
        if usuario:
            app.logger.info("@callback[ signin_page ]: 'signin_usuario()' -> REGISTRO SUCCESS")
            # Devuelvo el token de usuario y lo seteo en el contexto
            app.logger.info("@callback[ signin_page ]: 'signin_usuario()' -> HACIENDO LOGIN usuario")
            login_user(usuario)
            app.logger.info("@callback[ signin_page ]: 'signin_usuario()' -> LOGIN_USER SUCCESS")
            show_alert_error = False
            return show_alert_error, True
    
    # Quiere decir que ese nick no está disponible, por tanto, habrá que devolver un error en pantalla
    return show_alert_error, False
      


@app.callback(
    Output("url_signin",        "pathname"),
    [Input("al-success-signin",  "is_open")]
)
def signin_success(showed_alert):
    if showed_alert:
        time.sleep(1)
        return "/success"

@app.callback(
    [Output("msignin-body",         "children"),     
     Output("cnt-msignin-entrar",   "children")],
    [Input("msignin-close",   "n_clicks")]
)  
def reset_form_login(close_modal):
    return [form_signin, cnt_alert_error], btn_entrar_msignin



@app.callback(
    Output("msignin-enter",       "disabled"),
    [Input("msignin-pass",        "value"),
     Input("msignin-nick",        "value")]
)
def disabled_msignin_enter(password, nick):
    
    app.logger.info("@callback[ signin_page ]: INICIO 'disabled_msignin_enter()' -> password: " + str(utils.name_file_valid(password)) )
    app.logger.info("@callback[ signin_page ]: INICIO 'disabled_msignin_enter()' -> nick: "     + str(utils.name_file_valid(nick)) )
    
    if utils.name_file_valid(password) and utils.name_file_valid(nick):
        app.logger.info("@callback[ signin_page ]: 'disabled_msignin_enter()' -> NO valido")
        return False
    else:
        app.logger.info("@callback[ signin_page ]: 'disabled_msignin_enter()' -> valido")
        return True



###############################################################################
                ########## LAYOUTS DE PAGINA ##########
###############################################################################

def layout():
    return html.Div([signin_url, modales_logueo])