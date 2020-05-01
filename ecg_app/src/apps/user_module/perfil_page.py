#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 20:41:32 2020

@author: cristian
"""

import dash
import dash_table
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
from flask_login import current_user

import src.apps.user_module.user_service as user_service
import src.apps.ecg_module.ecg_service as ecg_serv

from app_context import app
logger = app.logger

#{"id": i, "hidden": True if i=="id" else False } for i in ["id", "nombre", "f_creacion", "f_edicion"]
# 

def th_tbl_sesiones():
    result = []
    th_nombres = ["Id", "Token", "Nombre", "Fecha creación", "Última edición"]
    th_id = ["id", "token", "nombre", "f_creacion", "f_edicion"]
    
    for i in range( len(th_nombres) ):
        aux = {"id": th_id[i], "hidden": True if (th_id[i]=="id" or th_id[i]=="token") else False, "name":th_nombres[i]}
        result.append(aux)
        
    logger.info("[ perfil_page ]- th_tbl_sesiones() -> result: " + str(result))
    return result


tabla_sesiones = dash_table.DataTable(
    id="tbl-sesiones",
    columns = th_tbl_sesiones(),
    row_selectable="single",
    style_cell_conditional=[
            {'if': {'column_id': 'id'},
             'width': '5%',             
            },
            {'if': {'column_id': 'nombre'},
             'width': '50%'
            },
            {'if': {'column_id': 'f_creacion'},
             'width': '20%'
            },
            {'if': {'column_id': 'f_edicion'},
             'width': '25%'
            }
        ]
)


btns_sesiones = dbc.ButtonGroup(
    [ 
        html.Div([
            dbc.Button(id="btn-delete-sesion", children=[
                                 html.Span([html.I(className="fa fa-minus"), " Eliminar sesión"])
                             ], color="danger", disabled=True ,className="text-left mr-1"
                      ),  
        ], className="text-left"),
        
         html.Div([
             dbc.Button(id="btn-load-sesion", children=[
                             html.Span([html.I(className="fa fa-hourglass-start"), " Cargar sesión" ])
                         ], color="success", disabled=True
                       ),
         ], className="text-right mr-1"),
         html.Div([
             dbc.Button(id="btn-ver-files", children=[
                             html.Span([html.I(className="fa fa-database"), " Ver ficheros" ])
                         ], color="info", disabled=True
                       ),
         ], className="text-right")
         
     ]
)


profile_data_card = dbc.Card(
    [
        dbc.CardBody(
            [
                dbc.Row([
                    dbc.Col([
                        html.H5("Sesiones", className="card-title"),
                    ]),
                    dbc.Col([
                         dbc.Button(id="prof-new-sesion", children=[
                                 html.Span([html.I(className="fa fa-plus ml-2"), " Nueva sesión" ])
                              ], outline=True, color="dark"),
                    ], className="text-right")
                ]),
                html.Hr(className="my-4"),
                tabla_sesiones,
                html.Hr(className="my-4"),
                btns_sesiones
            ]
        ),
    ], color="light"    
)
            


cabecera = dbc.Jumbotron(
    [
        dbc.Row([
            dbc.Col([
                html.H5(children=["Usuario: ", html.Span(id="prof-nick", children=["undefined"])], className="display-5 text-left"),
            ], width=6),
            dbc.Col([
                html.H5(children=[
                                    "Fecha de registro: ",
                                    html.Span(id="prof-freg", children=["00/00/0000"])
                                  ], className="display-5 text-right"),
            ], width=6)
        ]),
        
        
        html.Hr(className="my-4"),
        dbc.Row([
            dbc.Col([
                profile_data_card
            ], width=12),
        ]),
    ]
)


##############################################################################
## Modal ficheros de sesion

def th_tbl_session_files():
    result = []
    th_nombres = ["Id", "Nombre", "Formato", "Fecha creación"]
    th_id = ["id", "nombre", "formato", "f_creacion"]
    
    for i in range( len(th_nombres) ):
        aux = {"id": th_id[i], "hidden": True if (th_id[i]=="id") else False, "name": th_nombres[i]}
        result.append(aux)    
    return result


tbl_ficheros = dash_table.DataTable(
    id="tbl-files-sesion",
    row_selectable="multiple",
    columns= th_tbl_session_files(),
    style_cell_conditional=[
            {'if': {'column_id': 'id'},
             'width': '5%',             
            },
            {'if': {'column_id': 'nombre'},
             'width': '50%'
            },
            {'if': {'column_id': 'formato'},
             'width': '20%'
            },
            {'if': {'column_id': 'f_creacion'},
             'width': '25%'
            }
    ]
)


mbtn_delete_files = dbc.Button(id="msesfiles-borrar", n_clicks=None, className="mr-1", color="danger",
                                children=[
                                    html.Span([html.I(className="fa fa-trash ml-2"), " Eliminar"])
                                 ], disabled=True                    
                        )

mbtn_cerrar_files = dbc.Button(id="msesfiles-cerrar", n_clicks=None, className="mr-1",
                              children=[
                                html.Span([html.I(className="fas fa-times ml-2"), " Cerrar"])
                             ])

modal_files_sesion = html.Div([
    dbc.ModalHeader("Historial de ficheros"),
    dbc.ModalBody([
        tbl_ficheros
    ]),
    dbc.ModalFooter([
        html.Div( id="cnt-msesfiles-cerrar",   children=[mbtn_cerrar_files] ),
        html.Div( id="cnt-msesfiles-borrar",   children=[mbtn_delete_files] )        
    ]),
])


cnt_modal_files_sesion = dbc.Modal(
            children = modal_files_sesion,
            id = "msesfiles-sesion",
            size = "lg",
            backdrop = "static"
        )
##############################################################################

cargar_sesiones = dbc.Input(id="load-sesiones", type="hidden", value="True")

body = dbc.Container([
    html.Br(),
    html.H1("Perfil de Usuario"),
    html.Hr(),
    cabecera,
    cargar_sesiones,
    cnt_modal_files_sesion
])


###############################################################################
                       ########## CALLBACKS ##########
###############################################################################

@app.callback(
    [Output("tbl-sesiones",   "data"),
     Output("prof-nick",      "children"),
     Output("prof-freg",      "children")],
    [Input("load-sesiones",   "value")]
)
def load_sesiones_usuario(btn_new_sesion):
    if current_user.is_authenticated:
        logger.info("@callback [ perfil_page ] - load_sesiones_usuario() -> ENTRA EN PERFIL PAGE")        
        sesiones_usuario = user_service.get_sesiones_by_user(current_user.id)
        logger.info("@callback [ perfil_page ] - load_sesiones_usuario() -> sesiones_usuario: " + str(sesiones_usuario))
        return [sesiones_usuario, current_user.nick, current_user.f_registro]



@app.callback(
    [Output("btn-delete-sesion",    "disabled"),
     Output("btn-load-sesion",      "disabled"),
     Output("btn-ver-files",        "disabled")],
    [Input("tbl-sesiones",          "derived_virtual_selected_rows")]
)
def select_row_sesion(sesion_selected):
    logger.info("@callback [ perfil_page ] - crear_sesion() -> sesion_selected: "+ str(sesion_selected))
    disable_btns = False
    if sesion_selected is not None and sesion_selected != []:
        return disable_btns, disable_btns, disable_btns
    
    return not disable_btns, not disable_btns, not disable_btns


@app.callback(
    Output("msesfiles-sesion",  "is_open"),
    [Input("btn-ver-files",     "n_clicks"),
     Input("msesfiles-cerrar",  "n_clicks")],
    [State("msesfiles-sesion",  "is_open")]
)
def toggle_msesfiles(btn_verfiles, btn_cancel_files, is_open):
    if btn_verfiles or btn_cancel_files:
        return not is_open
    return is_open


@app.callback(
    Output('tbl-files-sesion',  "data"),
    [Input("btn-ver-files",     "n_clicks")],
    [State('tbl-sesiones',      "derived_virtual_selected_rows"),
     State('tbl-sesiones',      "derived_virtual_data")]
)
def load_files_sesion(btn_ver_files, row_selected, rows):
    app.logger.info("@callback [ perfil_page ] INICIO 'load_files_sesion()'")    
    app.logger.info("@callback [ perfil_page ] - load_files_sesion() -> row_selected: " + str(row_selected))
        
    if row_selected is not None and row_selected != []:
        indice = row_selected[0]
        id_token_sesion = rows[indice]["token"]
        app.logger.info("@callback [ perfil_page ] - load_files_sesion() -> id_token_sesion: " + str(id_token_sesion))
        files_sesion = ecg_serv.get_list_files_user(id_token_sesion)
        app.logger.info("@callback [ perfil_page ] - load_files_sesion() -> files_sesion: " + str(files_sesion))
        return files_sesion
    
    return []




@app.callback(
     Output("msesfiles-borrar",    "disabled"),
    [Input("tbl-files-sesion",     "derived_virtual_selected_rows")]
)
def select_row_file_sesion(sesion_selected):
    #logger.info("@callback [ perfil_page ] - select_row_file_sesion() -> sesion_selected: "+ str(sesion_selected))
    disable_btns = False
    if sesion_selected is not None and sesion_selected != []:
        return disable_btns
    
    return not disable_btns




@app.callback(    
     Output("url_sesion_load",  "pathname"),
    [Input("btn-load-sesion",   "n_clicks")],
    [State('tbl-sesiones',      "derived_virtual_selected_rows"),
     State('tbl-sesiones',      "derived_virtual_data")]
)
def go_session_selected(showed_alert, row_selected, rows):
    if showed_alert is None:
        raise dash.exceptions.PreventUpdate()
        
    if row_selected is not None and row_selected != []:
        indice = row_selected[0]
        token_sesion = rows[indice]["token"].split("_")[1]
        app.logger.info("@callback [ perfil_page ] - go_session_selected() -> token_sesion: " + str(token_sesion) )
        url = "/ecg/sesion/"+token_sesion
        return url



sesion_load_url = dcc.Location(id='url_sesion_load',  refresh=True)


###############################################################################
                       ########## MAIN LAYOUT ##########
###############################################################################

def layout():
    return dbc.Container([body, sesion_load_url])