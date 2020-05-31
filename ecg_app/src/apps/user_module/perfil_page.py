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
import src.commons.utils_ecg as utils

from app_context import app
logger = app.logger



def th_tbl_sesiones():
    result = []
    th_nombres = ["Id", "Token", "Nombre", "Fecha creación", "Última edición"]
    th_id = ["id", "token", "nombre", "f_creacion", "f_edicion"]
    
    for i in range( len(th_nombres) ):
        aux = {"id": th_id[i], "hidden": True if (th_id[i]=="id" or th_id[i]=="token") else False, "name":th_nombres[i]}
        result.append(aux)
            
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


mbtn_delete_files = dbc.Button(id="msesfiles-borrar", className="mr-1", color="danger",
                                children=[
                                    html.Span([html.I(className="fa fa-trash ml-2"), " Eliminar"])
                                 ], disabled=True                    
                        )

mbtn_cerrar_files = dbc.Button(id="msesfiles-cerrar", className="mr-1",
                              children=[
                                html.Span([html.I(className="fas fa-times ml-2"), " Cerrar"])
                             ])

histf_alert_error = html.Div(
     dbc.Alert(id="histf-al-error", children=["Ha ocurrido un error al eliminar los ficheros seleccionados"],
               color="danger", is_open=False, dismissable=True)
)

cnt_histf_alert_error = html.Div(id="cnt-histf-al-error", children=histf_alert_error)

modal_files_sesion = html.Div([
    dbc.ModalHeader("Historial de ficheros"),
    dbc.ModalBody([
        tbl_ficheros
    ]),
    dbc.ModalFooter([
        cnt_histf_alert_error,
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
## Modal confirmacion borrar ficheros

mbtn_borrarfiles_borrar = dbc.Button(id="mborrarfiles-borrar", className="mr-1", color="danger",
                                children=[
                                    html.Span([html.I(className="fa fa-plus ml-2"), " Borrar"])
                                 ]
                          )

mbtn_borrarfiles_cancelar = dbc.Button(id="mborrarfiles-cancelar", className="mr-1",
                              children=[
                                html.Span([html.I(className="fas fa-times ml-2"), " Cancelar"])]
                             )

modal_borrar_ficheros = html.Div([    
    dbc.ModalBody([
        html.H4(children=["Eliminar ficheros"]),
        html.P("Se van a borrar los ficheros seleccionados."),
        html.P("Proceso IRREVERSIBLE. ¿Desea continuar?"),
        dbc.Row([
            dbc.Col([
                html.Div( id="cnt-mborrarfiles-cancelar",  children=[mbtn_borrarfiles_cancelar], className="text-left" )
            ]),
            dbc.Col([
                html.Div( id="cnt-mborrarfiles-borrar",    children=[mbtn_borrarfiles_borrar], className="text-right" )
            ])
        ])
    ], className="text-center"),
])

cnt_modal_borrar_files = dbc.Modal(
            children = modal_borrar_ficheros,
            id = "cnt-mborrarfiles",
            size = "lg",
            backdrop = "static"
)


##############################################################################
## Modal alta sesión

mbtn_nuevases_crear = dbc.Button(id="mnuevases-crear", className="mr-1", color="success",
                                children=[
                                    html.Span([html.I(className="fa fa-plus ml-2"), " Crear"])
                                 ], disabled=True                    
                        )

mbtn_nuevases_cancel = dbc.Button(id="mnuevases-cancelar", className="mr-1",
                              children=[
                                html.Span([html.I(className="fas fa-times ml-2"), " Cancelar"])
                             ])

form_nuevases_input = dbc.Input(type="text", id="fnuevases-nombre", placeholder="", value="", maxlength=40)

form_nuevases_body = html.Div([
    dbc.FormGroup([
        dbc.Label("Nombre sesión: ", html_for="fnuevases-nombre", width=3),
        dbc.Col(
            html.Div(id="cnt-fnuevases-nombre", children = form_nuevases_input), width=9,
        )
    ], row=True),
])


form_nuevases = dbc.Form(id="form-nueva-sesion", children=[
    form_nuevases_body
])

nuevases_alert_error = html.Div(
     dbc.Alert(id="nuevases-al-error", children=["No se ha podido crear la sesión. Vuelva a intentarlo"], 
               color="danger", is_open=False)
)

cnt_nuevases_alert_error = html.Div(id="cnt-nuevases-al-error", children=nuevases_alert_error)

modal_nueva_sesion = html.Div([
    dbc.ModalHeader("Nueva sesión"),
    dbc.ModalBody([
        form_nuevases,
        cnt_nuevases_alert_error
    ]),
    dbc.ModalFooter([
        html.Div( id="cnt-mnuevases-cancelar",  children=[mbtn_nuevases_cancel] ),
        html.Div( id="cnt-mnuevases-crear",     children=[mbtn_nuevases_crear] )        
    ]),
])


cnt_modal_nueva_sesion = dbc.Modal(
            children = modal_nueva_sesion,
            id = "mnueva-sesion",
            size = "lg",
            backdrop = "static"
        )

nuevases_alert_sucess = html.Div(
     dbc.Alert(id="nuevases-al-success", children=["Se ha creado la sesión correctamente"], 
               color="success", is_open=False, dismissable=True)
)

cnt_nuevases_alert = html.Div(children=nuevases_alert_sucess)


##############################################################################
## Modal confirmacion borrar sesion

borrarsesion_btn_borrar = dbc.Button(id="mdelsesion-borrar", className="mr-1", color="danger",
                                children=[
                                    html.Span([html.I(className="fa fa-plus ml-2"), " Borrar"])
                                 ]
                          )

borrarsesion_btn_cancel = dbc.Button(id="mdelsesion-cancelar", className="mr-1",
                              children=[
                                html.Span([html.I(className="fas fa-times ml-2"), " Cancelar"])]
                             )

modal_borrar_sesion = html.Div([
    dbc.ModalBody([
        html.H4(children=["Eliminar sesión"]),
        html.P("Se va a eliminar los datos de la SESIÓN seleccionada junto con los FICHEROS asociados a ella"),
        html.P("Proceso IRREVERSIBLE. ¿Desea continuar?"),
        dbc.Row([
            dbc.Col([
                html.Div( id="cnt-mdelsesion-cancelar",  children=[borrarsesion_btn_cancel], className="text-left" )
            ]),
            dbc.Col([
                html.Div( id="cnt-mdelsesion-borrar",    children=[borrarsesion_btn_borrar], className="text-right" )
            ])
        ])
    ], className="text-center"),
])

borrarsesion_al_error = html.Div(
     dbc.Alert(id="mdelsesion-al-error", children=["Ha ocurrido un error al eliminar la sesión"],
               color="danger", is_open=False, dismissable=True)
)

cnt_borrarsesion_al_error = html.Div(id="cnt-mdelsesion-al-error", children=borrarsesion_al_error)

cnt_modal_borrar_sesion = dbc.Modal(
            children = modal_borrar_sesion,
            id = "mdelsesion",
            size = "lg",
            backdrop = "static"
)

##############################################################################

cargar_sesiones = dbc.Input(id="load-sesiones", type="hidden", value="True")

nuevases_status = dbc.Input(id="nuevases-estado", type="hidden", value="")
cnt_nuevases_status = html.Div(id="cnt-nuevases-estado", children=nuevases_status)


body = dbc.Container([
    cnt_nuevases_alert,
    cnt_borrarsesion_al_error,
    html.Br(),
    cnt_nuevases_status,
    html.H1("Perfil de Usuario"),
    html.Hr(),
    cabecera,
    cargar_sesiones,
    cnt_modal_files_sesion,
    cnt_modal_nueva_sesion,
    cnt_modal_borrar_files,
    cnt_modal_borrar_sesion
])


###############################################################################
                       ########## CALLBACKS ##########
###############################################################################

def get_id_btn_clicked(ctx):
    button_id = ""
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate()
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        logger.info("[ perfil_page ] -  get_id_btn_clicked() -> button_id: "+ str(button_id))
    
    return button_id


def msesions_get_sesion(sesion_sel, tbl_sesiones):    
    sesion = None
    if sesion_sel is not None and tbl_sesiones != []:
        indice = sesion_sel[0]
        sesion = tbl_sesiones[indice]
    
    app.logger.info("[ perfil_page ] - msesions_get_sesion() -> sesion: " + str(sesion))
    return sesion
    


@app.callback(
    [Output("tbl-sesiones",         "data"),
     Output("prof-nick",            "children"),
     Output("prof-freg",            "children"),
     Output('cnt-nuevases-estado',  "children"),
     Output('mdelsesion-al-error',  "is_open")],
    [Input("load-sesiones",         "value"),
     Input("mdelsesion-borrar",     "n_clicks")],
    [State('tbl-sesiones',          "derived_virtual_selected_rows"),
     State('tbl-sesiones',          "derived_virtual_data")]
)
def load_sesiones_usuario(btn_new_sesion, btn_del_sesion, row_seleted, rows):
    """
    Carga las sesiones de usuario en la página de Perfil de Usuario
    
    """
    if current_user.is_authenticated:
        
        logger.info("\n@callback [ perfil_page ] - load_sesiones_usuario() -> ENTRA EN PERFIL PAGE") 
        ctx = dash.callback_context
        button_id = get_id_btn_clicked(ctx)
        
        if button_id == "mdelsesion-borrar" and btn_del_sesion is not None:
            sesion = msesions_get_sesion(row_seleted, rows)
            if sesion is not None:
                result_borrar = user_service.borrar_sesion(sesion)
                sesiones_usuario = user_service.get_sesiones_by_user(current_user.id)
                return [sesiones_usuario, current_user.nick, current_user.f_registro, nuevases_status, not result_borrar]
        else:
            sesiones_usuario = user_service.get_sesiones_by_user(current_user.id)
            logger.info("@callback [ perfil_page ] - load_sesiones_usuario() -> sesiones_usuario: " + str(sesiones_usuario))
            return [sesiones_usuario, current_user.nick, current_user.f_registro, nuevases_status, False]
        
    raise dash.exceptions.PreventUpdate()


@app.callback(
    [Output("btn-delete-sesion",    "disabled"),
     Output("btn-load-sesion",      "disabled"),
     Output("btn-ver-files",        "disabled")],
    [Input("tbl-sesiones",          "derived_virtual_selected_rows")]
)
def select_row_sesion(sesion_selected):
    """
    Activa/Desactiva los botones de acción para una sesión seleccionada

    """
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
    """
    Abre/Cierra la ventana modal de ficheros de una sesión

    """

    if btn_verfiles or btn_cancel_files:
        return not is_open
    return is_open



def msesfiles_get_sesion(sesion_sel, tbl_sesiones):    
    id_token_sesion = None
    if sesion_sel is not None and tbl_sesiones != []:
        indice = sesion_sel[0]
        id_token_sesion = tbl_sesiones[indice]["token"]
    
    app.logger.info("[ perfil_page ] - msesfiles_get_sesion() -> id_token_sesion: " + str(id_token_sesion))
    return id_token_sesion
    


def msesfiles_cargar_files(token_sesion):
    files_sesion = ecg_serv.get_list_files_user(token_sesion)
    app.logger.info("[ perfil_page ] - msesfiles_cargar_files() -> files_sesion: " + str(token_sesion))
    if files_sesion is not None and files_sesion != []:
        app.logger.info("[ perfil_page ] - msesfiles_cargar_files() -> MUESTRO LOS FICHEROS")
        return files_sesion
    
    return []

def msesfiles_borrar_files(token_sesion, list_files):

    if list_files is not None and list_files != []:
        app.logger.info("[ perfil_page ] - msesfiles_cargar_files() -> MUESTRO LOS FICHEROS")
        result = user_service.delete_files_selected(token_sesion, list_files)
        if result is True:
            files_sesion = msesfiles_cargar_files(token_sesion)
            return files_sesion, True
        else:
            return [], False
    
    return [], False

def get_data_selected(rows_sel, rows):
    result = []
    if rows_sel is not None and rows_sel != []:
        for row in rows_sel:
            data = rows[row]
            result.append(data)
    
    return result



@app.callback(
    [Output('tbl-files-sesion',     "data"),
     Output("tbl-files-sesion",     "selected_rows"),
     Output("histf-al-error",       "is_open")],
    [Input("btn-ver-files",         "n_clicks"),
     Input("mborrarfiles-borrar",   "n_clicks")],
    [State('tbl-sesiones',          "derived_virtual_selected_rows"),
     State('tbl-sesiones',          "derived_virtual_data"),
     State('tbl-files-sesion',      "derived_virtual_selected_rows"),
     State('tbl-files-sesion',      "derived_virtual_data"),]
)
def load_files_sesion(btn_ver_files, btn_borrar_files, row_selected_ses, rows_ses, rows_files_sel, rows_files):
    """
    Carga los ficheros de una sesión selecionada al clicar sobre el botón "Ver ficheros"

    """
    app.logger.info("@callback [ perfil_page ] INICIO 'load_files_sesion()'")    

    ctx = dash.callback_context
    button_id = get_id_btn_clicked(ctx)
    
    token_sesion = msesfiles_get_sesion(row_selected_ses, rows_ses)
    if utils.is_not_empty(token_sesion):
        if button_id == "btn-ver-files":
            app.logger.info("@callback [ perfil_page ] - 'load_files_sesion()' -> CARGAR ficheros")
            files_sesion = msesfiles_cargar_files(token_sesion)
            return files_sesion, [], False #Cargar ficheros de sesion
        
        elif button_id == "mborrarfiles-borrar":
            app.logger.info("@callback [ perfil_page ] - 'load_files_sesion()' -> BORRAR ficheros")
            # Borrar ficheros de sesion
            files_selected = get_data_selected(rows_files_sel, rows_files)
            files_sesion, result_operacion = msesfiles_borrar_files(token_sesion, files_selected) 
            if result_operacion is True:
                app.logger.info("@callback [ perfil_page ] - 'load_files_sesion()' -> Los ficheros se han borrado correctamente")
                return files_sesion, [], False
            else:
                app.logger.info("@callback [ perfil_page ] - 'load_files_sesion()' -> Los ficheros NO se han podido borrar")
                return rows_files, [], True
    
    raise dash.exceptions.PreventUpdate()



@app.callback(
     Output("msesfiles-borrar",    "disabled"),
    [Input("tbl-files-sesion",     "derived_virtual_selected_rows")]
)
def select_row_file_sesion(sesion_selected):
    """
    Activa/Desactiva el botón de "Borrar" en la selección de ficheros de una sesión

    """
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
    """
    Redirige a la página de análisis de ECG de una sesión

    """
    if showed_alert is None:
        raise dash.exceptions.PreventUpdate()
        
    if row_selected is not None and row_selected != []:
        indice = row_selected[0]
        token_sesion = rows[indice]["token"].split("_")[1]
        app.logger.info("@callback [ perfil_page ] - go_session_selected() -> token_sesion: " + str(token_sesion) )
        url = "/ecg/sesion/"+token_sesion
        return url



@app.callback(
    Output("cnt-mborrarfiles",      "is_open"),
    [Input("msesfiles-borrar",      "n_clicks"),
     Input("mborrarfiles-cancelar", "n_clicks"),
     Input("mborrarfiles-borrar",   "n_clicks")],
    [State("cnt-mborrarfiles",      "is_open")]
)
def mborrarfiles_toggle(btn, btn_cancel, btn_borrar, is_open):
    """
    Muestra o no la ventana de confirmación de borrado de los ficheros de una sesión

    """
    if btn or btn_cancel or btn_borrar:
        return not is_open
    return is_open
    

@app.callback(
    Output("cnt-histf-al-error",    "children"),
    [Input("msesfiles-borrar",      "n_clicks")],
)
def mborrarfiles_reset_alert(btn):
    """
    Reinicia el alert de borrar un fichero de la sesión

    """
    if btn:
        return histf_alert_error
    


###############################################################################
## Callbacks Nueva sesión
        
@app.callback(    
    Output("mnueva-sesion",      "is_open"),     
    [Input("prof-new-sesion",    "n_clicks"),
     Input("mnuevases-cancelar", "n_clicks")],
    [State('mnueva-sesion',      "is_open")]
)
def toggle_modal_new_session(btn_ns, btn_cancel, is_open):
    """
    Abre/Cierra la modal de creación de una sesión

    """

    if btn_ns or btn_cancel:
        return not is_open

    return is_open



@app.callback(
    [Output("mnuevases-crear",          "disabled"),
     Output("cnt-nuevases-al-error",    "children")],
    [Input("fnuevases-nombre",          "value")]
)
def mnuevases_crear_disabled(nombre_sesion):
    """
    Activa/Desactiva el botón de crear una nueva sesión

    """
    
    if utils.is_not_empty(nombre_sesion):        
        return False, nuevases_alert_error
    else:        
        return True, nuevases_alert_error



@app.callback(
    Output("fnuevases-nombre", "value"),
    [Input("prof-new-sesion", "n_clicks")]
)
def mnuevases_form_reset(btn):
    return ""
    

    
@app.callback(
    Output("nuevases-estado", "value"),
    [Input("mnuevases-crear", "n_clicks")],
    [State("fnuevases-nombre", "value")]
)
def mnuevases_crear_sesion(btn, nombre_sesion):
    """
    Crea una nueva sesión de usuario

    """
    if btn is None:
        raise dash.exceptions.PreventUpdate()
    
    if current_user.is_authenticated:    
        # Obtenemos el ID del usuario para asociar la nueva sesion 
        id_usuario = current_user.id  # "5ea8a6e7c725a0a9f3692e7a"
        # Guardamos la nueva sesion
        logger.info("@callback [ perfil_page ] - mnuevases_crear_sesion() -> Guardando nueva sesion...")
        result_operacion = user_service.create_sesion(id_usuario, nombre_sesion)
        logger.info("@callback [ perfil_page ] - mnuevases_crear_sesion() -> nueva_sesion: " + str(result_operacion))

    return result_operacion



@app.callback(
    [Output("nuevases-al-success",  "is_open"),
     Output("nuevases-al-error",    "is_open")],
    [Input("nuevases-estado",       "value")],    
)
def show_msg_crear_sesion(stat_created):
    """
    Muestra o no los mensajes de success o de error al crear una sesión

    """

    if stat_created == "0":
        return False, True

    elif stat_created == "1":
        return True, False
    
    else:
        raise dash.exceptions.PreventUpdate()
    
    
    
@app.callback(
    [Output("mnuevases-cancelar",   "n_clicks"),
     Output("load-sesiones",        "value")],
    [Input("nuevases-al-success",  "is_open"),
     Input("nuevases-al-error",    "is_open")],
    [State("mnuevases-cancelar",    "n_clicks")]
)
def click_cancel_btn(success, error, clicks_cancel):
    """
    Hace .click() en el botón de la modal de creación de sesiones cuando 
    se muestra un mensaje de creación o error al haber creado una nueva sesión

    """
    logger.info("@callback [ perfil_page ] - click_cancel_btn() -> success: " + str(success))
    if success is True:
        return clicks_cancel, ""
    else:
        raise dash.exceptions.PreventUpdate()



@app.callback(
    Output("mdelsesion",            "is_open"),
    [Input("btn-delete-sesion",     "n_clicks"),
     Input("mdelsesion-cancelar",   "n_clicks"),
     Input("mdelsesion-borrar",     "n_clicks")],
    [State("mdelsesion",            "is_open")]
)
def mborrarsesion_toggle(btn, btn_cancel, btn_borrar, is_open):
    """
    Abre/Cierra la modal de borrar una sesión

    """
    if btn or btn_cancel or btn_borrar:
        return not is_open
    return is_open





###############################################################################

sesion_load_url = dcc.Location(id='url_sesion_load',  refresh=True)

###############################################################################
                       ########## MAIN LAYOUT ##########
###############################################################################

def layout():
    return dbc.Container([body, sesion_load_url])