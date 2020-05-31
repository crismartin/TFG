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
import time

import src.commons.utils_ecg as utils
from database.authUser import AuthUser


from app_context import app
from app_context import bcrypt

#######################################
##### FORMULARIO MODAL REGISTRO
#######################################

email_input = dbc.FormGroup(
    [
        dbc.Label("Nick", html_for="mlogin-nick"),
        dbc.Input(type="text", id="mlogin-nick", placeholder="Enter nick", maxlength = "20", debounce=True),        
    ]
)

password_input = dbc.FormGroup(
    [
        dbc.Label("Password", html_for="mlogin-pass"),
        dbc.Input(
            type="password",
            id="mlogin-pass",
            placeholder="Enter password",
            debounce=True
        ),
    ]
)

btn_cerrar_mlogin = dbc.Button(id="mlogin-close", n_clicks=None, className="mr-1",
                              children=[
                                html.Span([html.I(className="fa fa-times ml-2"), " Cancelar"])
                             ])

btn_entrar_mlogin = dbc.Button(id="mlogin-enter", color="success", 
                          children=[
                                html.Span([html.I(className="fa fa-check"), " Entrar"])
                             ], disabled=True)

form_login = dbc.Form(id="form-login", children=[email_input, password_input])


alert_error_login = dbc.Alert(id="al-error-login", children=[
                                html.Span([html.I(className="fa fa-exclamation-triangle"), " Error: usuario o contraseña incorrectos"])
                             ], color="danger", is_open=False)

alert_success = dbc.Alert(id="al-success-login", children=[
                                html.Span([dbc.Spinner(color="success", size="sm"), "  Iniciando sesión..."])
                             ], color="success", is_open=False)

alerts_modal_login = html.Div(children=[alert_error_login, alert_success])

cnt_alert_error = html.Div(id="cnt-alerts-login", children=alerts_modal_login)


modal_signin = html.Div([
    dbc.ModalHeader(children=[html.Span([html.I(className="fa fa-power-off"), " Iniciar sesión"])]),
    dbc.ModalBody(id="mlogin-body", children=[
        form_login,
        cnt_alert_error
    ]),

    dbc.ModalFooter([
        html.Div( id="cnt-mlogin-cerrar",  children=btn_cerrar_mlogin ),
        html.Div( id="cnt-mlogin-entrar",  children=btn_entrar_mlogin )
    ]),
    
])

modales_logueo =  html.Div([dbc.Modal(id = "mlogin",
                             children = modal_signin,
                             size = "sm",
                             backdrop = "static")])

login_url = dcc.Location(id='url_login',   refresh=True)



###############################################################################
                       ########## CALLBACKS ##########
###############################################################################


@app.callback(
    Output("cnt-alerts-login",  "children"), 
    [Input("mlogin-nick",       "n_blur"),
     Input("mlogin-pass",       "n_blur")],
)
def set_error_alert_login(input1, input2):
    return alerts_modal_login



@app.callback(
    Output("mlogin",        "is_open"),     
    [Input("btn-login",     "n_clicks"),
     Input("mlogin-close",  "n_clicks")],
    [State("mlogin",        "is_open")],
)
def toggle_modal_login(open_click, close_click, is_open):
    """
    Abre/Cierra modal de login

    Returns
    -------
    bool
        Si se abre o no la ventana modal.

    """
    if (open_click or close_click):
        return not is_open    
    return is_open
        


@app.callback(
    [Output("mlogin-body",          "children"),
     Output("cnt-mlogin-entrar",    "children")],
    [Input("mlogin-close",          "n_clicks")]
)  
def reset_form_login(close_modal):
    """
    Reinicia el formulario de login

    """
    return [form_login, cnt_alert_error], btn_entrar_mlogin
    


@app.callback(
    [Output("al-error-login",   "is_open"),
     Output("al-success-login", "is_open")],
    [Input("mlogin-enter",      "n_clicks")],     
    [State("mlogin-nick",       "value"),
     State("mlogin-pass",       "value")],
)
def login_usuario(btn_login, nick, password):
    """
    Autentica a un usuario en la aplicación

    Parameters
    ----------    
    nick : str
        Nickname del usuario.
    password : str
        Contraseña del usuario.

    
    Returns
    -------
    show_alert_error : bool
        Muestra o no el mensaje de error al autenticar el usuario.
    bool
        Muestra o no el mensaje de success al autenticar el usuario.

    """
    show_alert_error = True
    
    app.logger.info("@callback[ login_page ]: 'toggle_modal_login()' -> entrando ando")
    if nick is None and password is None:
        raise dash.exceptions.PreventUpdate()
            
    # Compruebo los datos del usuario logado            
    usuario = AuthUser.get_usuario_by_nick(nick)
    if usuario:
        app.logger.info("@callback[ login_page ]: 'toggle_modal_login()' -> COMPROBANDO CONTRASEÑA DEL USUARIO")
        
        if  bcrypt.check_password_hash(usuario.password, password):
            # Devuelvo el token de usuario y lo seteo en el contexto
            login_user(usuario)
            app.logger.info("@callback[ login_page ]: 'toggle_modal_login()' -> LOGIN_USER SUCCESS")
            show_alert_error = False
            return show_alert_error, True

    return show_alert_error, False


@app.callback(
    Output("url_login",         "pathname"),
    [Input("al-success-login",  "is_open")]
)
def signin_success(showed_alert):
    """
    Redirecciona a la pantalla /success cuando se ha 
    logueado correctamente un usuario

    Parameters
    ----------
    showed_alert : bool
        Estado del mensaje que se muestra cuando la autenticación se ha realizado
        de manera correcta.

    Returns
    -------
    str
        Redirección de la página a success.

    """
    if showed_alert:
        time.sleep(1)
        return "/success"


@app.callback(
    Output("mlogin-enter",       "disabled"),
    [Input("mlogin-pass",        "value"),
     Input("mlogin-nick",        "value")]
)
def disabled_mlogin_enter(password, nick):
    """
    Activa/Desactiva el botón 'Enter' de la modal de login

    """
    
    app.logger.info("@callback[ signin_page ]: INICIO 'disabled_mlogin_enter()' -> password: " + str(utils.name_file_valid(password)) )
    app.logger.info("@callback[ signin_page ]: INICIO 'disabled_mlogin_enter()' -> nick: "     + str(utils.name_file_valid(nick)) )
    
    if utils.name_file_valid(password) and utils.name_file_valid(nick):
        app.logger.info("@callback[ signin_page ]: 'disabled_mlogin_enter()' -> NO valido")
        return False
    else:
        app.logger.info("@callback[ signin_page ]: 'disabled_mlogin_enter()' -> valido")
        return True


###############################################################################
                ########## LAYOUTS DE PAGINA ##########
###############################################################################


def layout():
    return html.Div([login_url, modales_logueo])