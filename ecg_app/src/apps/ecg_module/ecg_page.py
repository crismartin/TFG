#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:47:58 2019

@author: cristian
"""

import json
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go


import src.commons.utils_ecg as utils
import src.apps.ecg_module.ecg_service as ecg_serv


from app_context import app




###############################################################################


tipos_soportados = [{"label": "ISHNE",      "value": 1}, 
                    {"label": "Physionet",  "value": 2},
                    ]

fig_default = go.Figure(layout=go.Layout(hovermode = 'closest', uirevision=True, autosize=True, 
                    xaxis=dict(gridcolor="LightPink", range=[0, 12]), 
                    yaxis=dict(gridcolor="LightPink"),plot_bgcolor='rgb(248,248,248)') )


spiner_loading = html.Div([
    dbc.Button(
        [dbc.Spinner(size="sm"), " Loading..."],
        color="primary",
        disabled=True,
    )
])


msg_file = html.Div([
                    html.Span("  Fichero seleccionado: "),
                    dbc.Badge(id="lbl_name_file", color="info", className="mr-1"),                    
                ])


cnt_msg_upfile = html.Div([
                        html.Div(id="msg-upfile", children=msg_file)                        
                    ])
                       

cnt_uploader = html.Div([dcc.Upload(id="upload-file",
                children=html.Div([
                    'Arrastra y suelta o ',
                    html.A('selecciona el/los archivo/s')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center'
                },
                multiple=True
            ),
            html.Div(id='container-upfile',
                     children=[cnt_msg_upfile]
                     ),
            html.Div(id="cnt-alert-format", 
                     children=[
                        dbc.Alert(
                            id="alert-format",
                            color="light",
                            is_open=False
                        )
                    ]),
            html.Div([html.Span("* Formatos soportados: Ishne, Physionet")])
            ])

uploader = html.Div(id="cnt-uploader", children=cnt_uploader)
                        
  

input_component_hed  = dbc.Input(type="url", id="url-hed-file", placeholder="http://", value="")
input_component_ant  = dbc.Input(type="url", id="url-ant-file", placeholder="http://", value="")
input_component      = dbc.Input(type="url", id="url-dat-file", placeholder="http://", value="", debounce=True)


form_datos_ecg = html.Div([
    
    html.H5("Datos Header"),
    dbc.FormGroup([
        dbc.Label("Desde url remota: ", html_for="url-hed-file"),
        html.Div(id="input-component-hed", children = input_component_hed)
    ]),

    html.H5("Anotaciones"),
    dbc.FormGroup([
        dbc.Label("Desde url remota: ", html_for="url-ant-file"),
        html.Div(id="input-component-ant", children = input_component_ant)
    ]),

    html.H5("Datos ECG"),
    dbc.FormGroup([
        dbc.Label("Desde url remota: ", html_for="url-dat-file"),
        html.Div(id="input-component", children = input_component)
    ]),
    
    html.P([
        html.Label("ó")
    ], style={'text-align': 'center'} ),
        
    dbc.FormGroup(children = uploader)
])


formulario = dbc.Form(id="form-uploader", children=[
    form_datos_ecg
])


btn_procesar = dbc.Button(id="proces-upfile", color="success", 
                          children=[
                                html.Span([html.I(className="fas fa-cogs ml-2"), " Procesar"])
                             ], disabled=True)

btn_eliminar = dbc.Button(id="eliminar-file",
                          className="mr-1", color="danger", disabled=True,
                          children=[
                             html.Span([html.I(className="fas fa-trash ml-2"), " Borrar fichero/s"])
                          ])

btn_cerrar_modal = dbc.Button(id="close-upfile", n_clicks=None, className="mr-1",
                              children=[
                                html.Span([html.I(className="fas fa-times ml-2"), " Cerrar"])
                             ])

cnt_state_fdata = html.Div([
        dbc.Input( id="st-up-data",   type="hidden"),        
        dbc.Input( id="st-valid-data",  type="hidden"),
        dbc.Input( id="st-valid-ant",  type="hidden"),
])

cnt_state_fant =  html.Div([
        dbc.Input( id="st-up-ant",    type="hidden"),
])


modal_component = html.Div([
    dbc.ModalHeader("Cargar Fichero*"),
    dbc.ModalBody([
        formulario        
    ]),
    dbc.ModalFooter([
        html.Div( id="cnt-eliminar-file",   children=[btn_eliminar] ),
        html.Div( id="cnt-cerrar-modal",    children=[btn_cerrar_modal] ),
        html.Div( id="cnt-proces-modal",    children=[btn_procesar] ),
        html.Div( id="cnt-st-fdata",        children=[cnt_state_fdata] ),
        html.Div( id="cnt-st-fant",         children=[cnt_state_fant] ),
    ]),
])


##############################################################################
## Modal historico de ficheros

def th_tbl_hist_files():
    result = []
    th_nombres = ["Id", "Nombre", "Formato", "Fecha creación"]
    th_id = ["id", "nombre", "formato", "f_creacion"]
    
    for i in range( len(th_nombres) ):
        aux = {"id": th_id[i], "hidden": True if (th_id[i]=="id") else False, "name": th_nombres[i]}
        result.append(aux)    
    return result

table = dash_table.DataTable(
    id="tblHistFiles",
    columns=th_tbl_hist_files(),    
    row_selectable="single",
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


btn_cargar_modal_hist = dbc.Button(id="load-file-hist", n_clicks=None, className="mr-1", color="success",
                                children=[
                                    html.Span(["Cargar ",html.I(className="fas fa-play ml-2")])
                                 ], disabled=True                    
                        )

btn_cerrar_modal_hist = dbc.Button(id="close-hist", n_clicks=None, className="mr-1",
                              children=[
                                html.Span([html.I(className="fas fa-times ml-2"), " Cerrar"])
                             ])

modal_historial = html.Div([
    dbc.ModalHeader("Historial de ficheros"),
    dbc.ModalBody([
        table
    ]),
    dbc.ModalFooter([
        html.Div( id="cnt-cerrar-hist",    children=[btn_cerrar_modal_hist] ),
        html.Div( id="cnt-load-hist",    children=[btn_cargar_modal_hist] )        
    ]),
])
##############################################################################

ecg_fig = dcc.Graph(id='ecg-fig', 
                    figure=fig_default,              
                    style={'height': 600, 'width':900}
          )


display_ecg = dbc.FormGroup([   
        
    html.Div([       
        dbc.Modal(
            children = modal_component,
            id = "modal",
            size = "lg",
            backdrop = "static"
        ),
        dbc.Modal(
            children = modal_historial,
            id = "modal-historico",
            size = "lg",
            backdrop = "static"
        )
    ]),
    
    html.Div(id="cnt-ecg-fig", children=ecg_fig)
])
    
        
menu_ecg = html.Div([
    dbc.Button(id="hrvGraph", outline=True, color="info", className="mr-1",
               children=[
                       html.Span([html.I(className="fas fa-info-circle ml-2"), " Datos ECG"])
                       ]
               ),
    dbc.Button(id="otroGraph", outline=True, color="secondary", className="mr-1",
               children=[
                       html.Span([html.I(className="fas fa-folder ml-2"), " Historial de ficheros"])
                       ]
               ),
    dbc.Button(id="open-upfile",
               color="primary", 
               children=[
                       html.Span([html.I(className="fas fa-upload ml-2"), " Subir fichero"])
                       ]
               )
])


dropdown_leads = dbc.FormGroup([
    dbc.Row([
        html.H6("Elije una derivación"),    
    ]),
        
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id = 'optLeads',
                clearable=False,
                disabled=True             
            ), width=12
        )
    ])
])

point_info_input = dbc.FormGroup([
    dbc.Col(
        html.Span( [html.P(id="pto-inf-xi", children="Xi: "), html.P(id="pto-inf-yi", children="Yi: ")] ),  
    ),
    dbc.Col(
        html.Span( [html.P(id="pto-inf-xf", children="Xf: "), html.P(id="pto-inf-yf", children="Yf: ")] ),  
    )
    
], row=True)


edit_pt = html.Div([html.Div([
                dbc.Alert(                
                    id="alert-ann-success",                
                    color="success",
                    is_open=False,
                    dismissable=True
                ),    
            ]),
            html.Div([
                 dbc.Alert(id="alert-ann", children="Seleccione la anotación a cambiar", color="info"),
            ]),
            html.Div([
                point_info_input
            ]),
        ])

edit_point_input = dbc.Row( 
    dbc.Col(
        dbc.FormGroup([
        
            html.H6("Editar Anotación"),
            
            html.Div(id="cnt-pt-edit", children=edit_pt),
                
            dbc.FormGroup([            
                dbc.Input(
                    type="hidden", id="point-ini", disabled=True, step="any", value=""
                ),
                dbc.Input(
                    type="hidden", id="point-fin", disabled=True, step="any", value=""
                ),
                dbc.Input(
                    type="hidden", id="estado-edit", disabled=True, step="any", value=""
                ),
                dbc.Col([
                    dbc.Button(id="guardar-modif", color="success", disabled=True,
                       children=[
                           html.Span([html.I(className="fas fa-floppy-o ml-2"), " Finalizar Edición"])
                          ], className="float-right"
                    )
                ])
            ], row=True),       
        ]), width=12
    )
    
)



load_intervals_inputs = dbc.Row(
    dbc.FormGroup([
        dbc.Row([
            html.H6("Intervalos señal"),  
        ]),
        
        dbc.FormGroup([
            html.Div(
                children=[
                     html.P(id="msg-duracion", children=["Duración total aprox: "])
                ]
            )
        ], row=True),
        
        dbc.Row([
            html.H6("Ver señal:"),  
        ]),
        dbc.FormGroup([
            dbc.Label("desde ", html_for="interv_ini", width=3),
            dbc.Col(
                dbc.InputGroup([
                    dbc.InputGroupAddon("min", addon_type="prepend"),
                    dbc.Input(
                        type="number", id="interv_ini", 
                        disabled=True, debounce=True,
                        min=0,
                        pattern="^[0-9]\d*$"
                    ),                  
                ]),
                width=8,
            ),    
        ], row=True),
        
        dbc.FormGroup([
            dbc.Label("hasta ", html_for="interv_fin", width=3),
            dbc.Col(
                dbc.InputGroup([
                    dbc.InputGroupAddon("min", addon_type="prepend"),
                    dbc.Input(
                        type="number", id="interv_fin", 
                        disabled=True, debounce=True,
                        min=0,
                        pattern="^[0-9]\d*$"
                    ),
                    
                ]),
                width=8,
            ),
        ], row=True),
        
        dbc.FormGroup([
            dbc.Col([
                dbc.Alert(
                    "Intervalo incorrecto",
                    id="alert-interval",
                    color="danger",
                    is_open=False,
                    
                )            
            ],width=6),
            dbc.Col([
                dbc.Button(id="ver-intervalo", color="success", disabled=True,
                   children=[
                       html.Span([html.I(className="fas fa-play ml-2"), " Cargar"])                   
                      ]
                ),
                dbc.Input(type="hidden", id="diff_interv")
            ]),
        ], row=True),
        
        dbc.FormGroup([
            dbc.Input(
                type="hidden", id="duracion-total", disabled=True
            )
        ])
    ])
)

btn_next_interval = dbc.Button(id="btn-next-interval", outline=True, color="dark",
                       children=[
                           html.Span([html.I(className="fas fa-step-forward mr-1"), " Next"])
                          ],
                       n_clicks_timestamp='0',
                       disabled=True
                    )

btn_prev_interval = dbc.Button(id="btn-prev-interval", outline=True, color="dark",
                       children=[
                           html.Span([html.I(className="fas fa-step-backward mr-1"), " Prev"])
                          ],
                       n_clicks_timestamp='0',
                       disabled=True
                    )


move_controls = [dbc.Col(btn_prev_interval, width={"size": 2, "order": 1, "offset": 4}),
                    dbc.Col(btn_next_interval, width={"size": 2, "order": "last"}) ]

cnt_move_controls = dbc.Row(id="cnt-move-controls", 
                         children=move_controls,
                         style={"visibility":"hidden"}                         
                    )



title_controls =  dbc.FormGroup([
                    html.H2("Controles", id="controles-title", style={'text-align': 'left'})
                  ], row=True)


collapse_edicion = dbc.Row(
    dbc.FormGroup([
        dbc.Button(
            id="btn-collapse-edicion",
            className="mb-3",
            color="primary",
            disabled=True,
            children=[
                html.Span([html.I(className="fas fa-pencil-square-o mr-1"), " Editar Anotaciones"])
            ],
        ),    
        dbc.Collapse(            
            id="collapse-edicion",
            children=edit_point_input
        ),
    ]),    
)


form_controls = html.Div(id="form-controls", children=[ dropdown_leads, load_intervals_inputs, collapse_edicion])

cnt_form_controls = dbc.Form(id="cnt-form-controls", children=form_controls)

title_format = html.H1("Formato", id="formato-title", style={'textAlign': 'center'})


body = dbc.Container([
    html.Div(id="cnt-title-format", children=title_format),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                cnt_form_controls
            ]),
        ], width=3),
        dbc.Col([
            dbc.Row(
                display_ecg
            ),            
            cnt_move_controls
        ], width={"size": 9}, className="float-right")  
    ]),
    dbc.Row(
        menu_ecg, className="float-right"
    ),    
])

input_up_fecha_edicion_aux = dbc.Input(id="up-fecha-edicion-aux", type="hidden", value="")
input_up_fecha_edicion = dbc.Input(id="up-fecha-edicion", type="hidden", value="")

footer = html.Div([
            dbc.Input(type="hidden", id="fname_process"),
            input_up_fecha_edicion,
            input_up_fecha_edicion_aux
        ])


###############################################################################
############################### CALLBACKS #####################################
###############################################################################
    


# Validaciones de campos

@app.callback(
    [Output("alert-interval", "is_open"),
     Output("ver-intervalo", "disabled"),
     Output("cnt-move-controls", "style")],
    [Input("diff_interv", "value")]
)
def validar_intervalo(diff_interv):
    app.logger.info("@callback: INICIO 'validar_intervalo()'")
    if diff_interv == "" :
        style = {"visibility":"hidden"}
        return True, True, style
    
    style = {"visibility":"visible"}
    return False, False, style



@app.callback(
    Output("modal", "is_open"),
    [Input("open-upfile", "n_clicks"), 
     Input("close-upfile", "n_clicks"), 
     Input("proces-upfile", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, n3, is_open):    
    
    if (n1 or n2 or n3):
        return not is_open    
    return is_open



@app.callback(
    [Output("modal-historico",  "is_open"),
    Output('tblHistFiles',      "selected_rows"),
    Output('tblHistFiles',      "data")],
    [Input("otroGraph",         "n_clicks"),
     Input("close-hist",        "n_clicks"),
     Input("load-file-hist",    "n_clicks")],
    [State("modal-historico",   "is_open"),
     State("session",           "data")],
)
def toggle_modal_hist(open_click, close_click, load_click, is_open, session):
    historial_files = []
    if (open_click or close_click or load_click):
        app.logger.info("@callback: INICIO 'toggle_modal_hist()' -> aqui")
        if(open_click):            
            token_session = session["token_session"]
            app.logger.info("@callback: INICIO 'toggle_modal_hist()' -> token_session: " + str(token_session))
            historial_files = ecg_serv.get_list_files_user(token_session)
                    
        return not is_open, [], historial_files
    
    app.logger.info("@callback: INICIO 'toggle_modal_hist()' -> aca")
    return is_open, [], historial_files



@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("collapse-edicion", "is_open"),
    [Input("btn-collapse-edicion", "n_clicks")],
    [State("collapse-edicion", "is_open")],
)
def toggle_collapse_edicion(n, is_open):
    if n:
        return not is_open
    return is_open



@app.callback(
    Output("upload-file", "disabled"),
    [Input("url-hed-file","value"),
     Input("url-dat-file","value")]
)
def disabled_uploader(head_file, data_file):
    
    if utils.name_file_valid(head_file) or utils.name_file_valid(data_file):
        return True
    else:
        return False




@app.callback(
     Output("eliminar-file",  "disabled"),
    [Input("st-up-data", "value")]
)
def activar_btn_delete(st_upfile_data):
    app.logger.info("@callback: INICIO 'activar_btn_delete()'")
    
    app.logger.info( "@callback: 'activar_btn_delete()' -> st_upfile_data: " + str(st_upfile_data) )
    
    
    disabled_btn = True
    
    if st_upfile_data is None:
        app.logger.info("@callback: FIN by Exception 'activar_btn_delete()'")
        raise dash.exceptions.PreventUpdate()
        
    if st_upfile_data is True:
        disabled_btn = False
        
    app.logger.info( "@callback: 'activar_btn_delete()' -> disabled_btn: "  + str(disabled_btn) )
    
    app.logger.info("@callback: FIN 'activar_btn_delete()'")
    
    return disabled_btn



@app.callback(
    [Output("proces-upfile",    "disabled"),
     Output("alert-format",     "is_open"),
     Output("alert-format",     "color")],
    [Input("st-valid-data",     "value")],
)
def activar_btn_process(result_upfile):
    app.logger.info("@callback: INICIO 'activar_btn_process()'")
    
    if result_upfile is None:
        app.logger.info( "@callback: FIN by None result 'activar_btn_process()'" )
        return True, False, "light"
    
    is_file_valid, has_annt = result_upfile.split(",")
    is_file_valid = utils.str_to_bool(is_file_valid)
    has_annt = utils.str_to_bool(has_annt)
    
    app.logger.info( "@callback: 'activar_btn_process()' -> is_file_valid: " + str(is_file_valid) )
    app.logger.info( "@callback: 'activar_btn_process()' -> has_annt: " + str(has_annt) )
    if is_file_valid and (has_annt is not None and not has_annt):
        return False, True, "warning"
    
    
    app.logger.info( "@callback: FIN 'activar_btn_process()'" )
    return not is_file_valid, not is_file_valid, "danger"
    


@app.callback(
    [Output("form-uploader",        "children"),
     Output("cnt-st-fdata",         "children"),
     Output("cnt-ecg-fig",          "children"),
     Output("cnt-form-controls",    "children"),
     Output("cnt-move-controls",    "children"),     
     Output("cnt-title-format",     "children")],
    [Input("eliminar-file",         "n_clicks")],
    [State("lbl_name_file",         "children"),
     State("session",               "data")]
)
def delete_file(eliminar_file, name_file, data_session):
    
    app.logger.info("@callback: INICIO 'delete_file()'")
    app.logger.info( "@callback: delete_file() -> eliminar_file: " + str(eliminar_file) )
    app.logger.info( "@callback: delete_file() -> name_file: " + str(name_file) )    
    
    if utils.name_file_valid(name_file):
#        app.logger.info("@callback: FIN by exception 'delete_file()'")
        
        token_user = utils.get_session_token(data_session)
        app.logger.info( "@callback: delete_file() -> token_user: " + str(token_user) )
    
        app.logger.info( "@callback: 'delete_file(): Borrando fichero datos: '" + str(name_file) )
        ecg_serv.delete_file_system(token_user, name_file)
        
    app.logger.info( "@callback: FIN 'delete_file()'" )
    
    return [form_datos_ecg, cnt_state_fdata, ecg_fig, cnt_form_controls, move_controls, title_format]
    


def get_list_fname( url_head, url_ant, url_data ):
    list_nombres = []
    
    if utils.name_file_valid(url_head):
        list_nombres.append(url_head)
    
    if utils.name_file_valid(url_ant):
        list_nombres.append(url_ant)
        
    if utils.name_file_valid(url_data):
        list_nombres.append(url_data)
        
    return list_nombres
        
    


@app.callback(
    [Output('lbl_name_file',  'children'),
     Output("url-dat-file",   "disabled"),
     Output("url-hed-file",   "disabled"),
     Output("url-ant-file",   "disabled"),
     Output("st-up-data",     "value"),     
     Output('st-valid-data',  'value'),     
     Output("alert-format",   "children")],
    [Input('upload-file',     'contents'),
     Input('url-dat-file',    'value')],
    [State('upload-file',     'filename'),
     State("url-hed-file",    "value"),
     State("url-ant-file",    "value"),
     State("session",         "data")]
)
def updload_file(list_contents, url_data, list_nombres, url_head, url_ant, data_session):
    
    app.logger.info( "@callback: INICIO 'updload_file()'" )
    app.logger.info( "@callback: 'updload_file() -> url_data: " + str(url_data) )  
    app.logger.info( "@callback: 'updload_file() -> url_head: " + str(url_head) )
    app.logger.info( "@callback: 'updload_file() -> url_ant: "  + str(url_ant) )
    #app.logger.info( "@callback: 'updload_file() -> token_user: " + str(utils.get_session_token(data_session)) )
    app.logger.info( "@callback: 'updload_file() -> list_nombres: " + str(list_nombres) )
    
    list_nombres = list_nombres or get_list_fname( url_head, url_ant, url_data )
    
    app.logger.info( "@callback: 'updload_file() -> list_nombres definitivo: " + str(list_nombres) )
    
    if utils.name_file_valid(url_data) or list_contents is not None:

        token_user = utils.get_session_token(data_session)
        msg_error, fichero_valido, nombre_file = ecg_serv.guardar_ficheros(list_contents, list_nombres, token_user)
        
        app.logger.info( "@callback: 'updload_file() -> msg_error: " + str(msg_error) )
        app.logger.info( "@callback: 'updload_file() -> fichero_valido: " + str(fichero_valido) )
        app.logger.info( "@callback: 'updload_file() -> nombre_file: " + str(nombre_file) )
        
        if fichero_valido:
            hay_annt = msg_error is None
            app.logger.info( "@callback: 'updload_file() -> hay_annt: " + str(hay_annt) )
            st_val_data = str(fichero_valido) + "," + str(hay_annt)
            return [nombre_file, True, True, True, True, st_val_data, msg_error]
        
        else:
            st_val_data = str(fichero_valido) + "," + str(None)
            return [nombre_file, False, False, False, True, st_val_data, msg_error]
    
    else:
        app.logger.info("@callback: FIN by None content 'updload_file()'")
        return [None, False, False, False, False, None, None]



@app.callback(
    Output("fname_process",     "value"),
    [Input("proces-upfile",     "n_clicks"),
     Input("load-file-hist",    "n_clicks")],
    [State("session",           "data"),
     State("lbl_name_file",     "children"),
     State("tblHistFiles",      "derived_virtual_data"),
     State("tblHistFiles",      "derived_virtual_selected_rows")]
)
def process_file(click_process, click_load, data_session, name_file, rows, row_select):
    app.logger.info("@callback: INICIO 'process_file()'")
    
    app.logger.info("@callback: 'process_file()' -> name_file: " + str(name_file) )
    app.logger.info("@callback: 'process_file()' -> row_select: " + str(row_select) )
    
    if (click_process is None or click_process <= 0) and (click_load is None or click_load <= 0):
        app.logger.info("@callback: FIN 'process_file()': 'click' Exception")
        raise dash.exceptions.PreventUpdate()
    
    token_user = utils.get_session_token(data_session)
    ruta_file = token_user + "/"
    
    if row_select is not None and row_select != []:
        index_element = row_select[0]
        name_file = rows[index_element]["nombre"]    
    
    ruta_file += name_file
    
    app.logger.info("@callback: 'process_file()' -> ruta_file: " + str(ruta_file))
    app.logger.info("@callback: FIN 'process_file()'")
    
    return ruta_file



@app.callback(
    [ Output("duracion-total", "value"),
     Output("optLeads","disabled"),
     Output("optLeads","options"),
     Output("optLeads","value"),
     Output("msg-duracion", "children"),    
     Output("interv_ini", "max"),
     Output("interv_fin", "max")
     ],
    [Input("fname_process", "value")]
)
def select_first_lead(fname_uploaded):
    app.logger.info("@callback: INICIO 'select_first_lead()'")
    
    if fname_uploaded is not None:
        app.logger.info("@callback: 'select_first_lead()' -> Configurando parametros para pintar")
        ruta_file = utils.dir_files + fname_uploaded
        app.logger.info("@callback: 'select_first_lead()' -> ruta_file: " + str(ruta_file))
        app.logger.info("@callback: 'select_first_lead()' -> Obteniendo leads...")
        optLeads, msg_duration, duration_min = ecg_serv.get_nleads_and_duration(ruta_file)
        
        app.logger.info("@callback: 'select_first_lead()' -> optLeads: " + str(optLeads))
        app.logger.info("@callback: FIN 'select_first_lead()'")
        text_duracion = "Duración total aprox: " + msg_duration
        return duration_min, False, optLeads, 1, text_duracion,  duration_min, duration_min
    
    app.logger.info("@callback: FIN 'select_first_lead()'")

    return "", True, None, None, None, "", ""


@app.callback(
    [Output("ecg-fig",          "figure"),
     Output("formato-title",    "children"),     
     Output("point-y",          "disabled"),
     Output("point-x",          "disabled"),
     Output("interv_ini",       "disabled"),
     Output("interv_fin",       "disabled"),
     Output("btn-collapse-edicion", "disabled")],
    [Input("optLeads",          "value"),
     Input("ver-intervalo",     "n_clicks"),
     Input("estado-edit",       "value")],
    [State("fname_process",     "value"),
     State("interv_ini",        "value"),
     State("interv_fin",        "value"),
     State("duracion-total",    "value"),
     State("session",           "data")]
)
def print_ecg_lead(selected_lead, ver_intervalo, estado_edit, fname_uploaded, interv_ini, interv_fin, duracion_total, data_session):
    app.logger.info("\n@callback: INICIO 'print_ecg()'")
    
    app.logger.info("@callback: 'print_ecg()' -> selected_lead: " + str(selected_lead))
    app.logger.info("@callback: 'print_ecg()' -> fname_uploaded: " + str(fname_uploaded))
    
    if fname_uploaded is None or selected_lead is None:
        app.logger.info("@callback: FIN 'print_ecg()' by Exception")
        raise dash.exceptions.PreventUpdate()
    
    token_user = utils.get_session_token(data_session)
    app.logger.info("@callback: 'print_ecg()' -> Configurando parametros para pintar")
    ruta_file = utils.dir_files + fname_uploaded
    app.logger.info("@callback: 'print_ecg()' -> ruta_file: " + str(ruta_file))
    app.logger.info("@callback: 'print_ecg()' -> Pintando datos...")
    
    fig, title, hay_annt = ecg_serv.build_plot_by_lead(ruta_file, selected_lead, interv_ini, interv_fin, token_user)
    
    # Desactivamos los inputs de intervalos porque la duracion de la señal es menor de 1 minuto
    desactivar_interval = True if int(duracion_total) < 1 else False 
    app.logger.info("@callback: FIN 'print_ecg()'")
    return fig, title, False, False, desactivar_interval, desactivar_interval, not hay_annt


@app.callback(
    Output('diff_interv', 'value'),
    [Input("interv_ini", "value"),
     Input("interv_fin", "value")]
)
def change_diff_interv(ini_value, fin_value):
    app.logger.info("@callback: INICIO 'change_diff_interv()'")
    
    if ini_value is None or fin_value is None:
        app.logger.info("@callback: FIN 'change_diff_interv()' by Exception: None value")
        raise dash.exceptions.PreventUpdate()
    
    if fin_value > ini_value:
        diff = fin_value - ini_value
    else:        
        diff = ""
    
    app.logger.info("@callback: 'change_diff_interv()': diff: " + str(diff))
    app.logger.info("@callback: FIN 'change_diff_interv()'")
    
    return diff



@app.callback(    
     Output("btn-next-interval", "disabled"),
    [Input("ver-intervalo", "n_clicks"),
     Input("interv_fin", "value")],
    [State("duracion-total", "value")]
)
def enable_btn_next(btn_cargar, interv_fin, duracion):
    app.logger.info("@callback: INICIO 'enable_btn_next()'")
    if btn_cargar and (int(interv_fin) < int(duracion)):
        app.logger.info("@callback: INICIO 'enable_btn_next()' -> return True")
        return False

    app.logger.info("@callback: INICIO 'enable_btn_next()' -> return False")
    return True


@app.callback(    
     Output("btn-prev-interval", "disabled"),
    [Input("ver-intervalo", "n_clicks"),
     Input("interv_ini", "value")],
)
def enable_btn_prev(btn_cargar, interv_ini):
    app.logger.info("@callback: INICIO 'enable_btn_prev()'")
        
    if btn_cargar and (int(interv_ini) > 0):
        app.logger.info("@callback: INICIO 'enable_btn_prev()' -> return True")
        return False

    app.logger.info("@callback: INICIO 'enable_btn_prev()' -> return False")
    return True



@app.callback(
    [Output("interv_fin", "value"),
     Output("interv_ini", "value"),
     Output("ver-intervalo", "n_clicks")],
    [Input("btn-next-interval", "n_clicks_timestamp"),
     Input("btn-prev-interval", "n_clicks_timestamp")],
    [State("diff_interv", "value"),
     State("interv_ini", "value"),
     State("interv_fin", "value"),
     State("ver-intervalo", "n_clicks"),
     State("duracion-total", "value")]
    
)
def next_interval_signal(next_btn, prev_btn, diff_interv, interv_ini, interv_fin, click_ver_interv, duracion):
    app.logger.info("@callback: INICIO 'next_interval_signal()'")
    if interv_ini is None and interv_fin is None:
        app.logger.info("@callback: FIN 'next_interval_signal()' by Exception: None values")
        raise dash.exceptions.PreventUpdate()
    
    next_btn = int(next_btn)
    prev_btn = int(prev_btn)
    
    if prev_btn > next_btn:
        diff_interv = (-1)*diff_interv
    
    new_interv_ini = interv_ini + diff_interv
    new_interv_fin = interv_fin + diff_interv
    duracion = int(duracion)
    
    if new_interv_ini < 0:
        new_interv_ini = 0
    
    if new_interv_fin > duracion:
        new_interv_fin = duracion
        
    app.logger.info("@callback: INICIO 'next_interval_signal()'")
    
    return [new_interv_fin, new_interv_ini, click_ver_interv+1]
    


###############################################################################
#### CALLBACK DE TABLAS    
###############################################################################

@app.callback(
    Output('load-file-hist',    "disabled"),
    [Input('tblHistFiles',      "derived_virtual_data"),
     Input('tblHistFiles',      "derived_virtual_selected_rows")])
def tbl_hist_row_selected(rows, derived_virtual_selected_rows):
    app.logger.info("@callback: INICIO 'tbl_hist_row_selected()'")
    
    app.logger.info("@callback: INICIO 'tbl_hist_row_selected()' -> rows: " + str(rows))
    app.logger.info("@callback: INICIO 'tbl_hist_row_selected()' -> derived_virtual_selected_rows: " + str(derived_virtual_selected_rows))
    
    if derived_virtual_selected_rows is None or derived_virtual_selected_rows == []:
        return True
    
    return False

    

###############################################################################
#### Edicion de Anotaciones    
###############################################################################


@app.callback(
    [Output("pto-inf-xi",   "children"),
     Output("pto-inf-yi",   "children"),
     Output("pto-inf-xf",   "children"),
     Output("pto-inf-yf",   "children"),
     Output("point-ini",    "value"),
     Output("point-fin",    "value"),
     Output("estado-edit",  "value")],
    [Input("ecg-fig",       "clickData")],
    [State("estado-edit",   "value"),
     State("point-ini",     "value"),
     State("fname_process", "value"),
     State("optLeads",      "value"),
     State("session",       "data")]
)
def display_click_data(clickData, last_estado, pt_ini, rutafile, nLead, data_session):
    info_xi = "Xi: "
    info_yi = "Yi: "
    info_xf = "Xf: "
    info_yf = "Yf: "
    
    app.logger.info("@callback: INICIO 'display_click_data()'")
    if clickData is None:
        raise dash.exceptions.PreventUpdate()
        
    data_json = json.dumps(clickData, indent=2)
    data_json = json.loads(data_json)
    
    app.logger.info("@callback: 'display_click_data() -> data_json: " + str(data_json))
    app.logger.info("@callback: 'display_click_data() -> last_estado: '" + str(last_estado)+ "'")

    pto_select = data_json["points"][0]
        
    if last_estado == "" or last_estado=="1": #Es primera seleccion
        #Comprobamos que es una anotacion
        if "text" in pto_select: #Es una posible anotacion
            simbolo =  str(pto_select["text"])
            app.logger.info("@callback: 'display_click_data() -> simbolo: " + str(simbolo))
            if "#" not in simbolo: #Es una anotacion                
                app.logger.info("@callback: 'display_click_data() -> Anotacion seleccionada")
                # seteo el valor del punto en los input hidden
                pt_ini = {}
                pt_ini["x"] = str("{:.8}".format(pto_select["x"]) )
                pt_ini["y"] = str(pto_select["y"])
                pt_ini["symbol"] = simbolo
                info_xi += pt_ini["x"]
                info_yi += pt_ini["y"]

                return info_xi, info_yi, info_xf, info_yf, pt_ini, "", "0"
        
    elif last_estado == "0": #Es la segunda seleccion
        #Comprobamos que no es una anotacion        
        app.logger.info("@callback: 'display_click_data() -> Entro aqui")
        if not "text" in pto_select: #Es un punto         
            app.logger.info("@callback: 'display_click_data() -> y tambien aqui")
            pt_fin = {}
            pt_fin["x"] = str("{:.8}".format(pto_select["x"]) )
            pt_fin["y"] = str(pto_select["y"])
            
            # GUARDAR AQUI EL PUNTO EN LA TABLA ANOTACIONES_TEMP            
            token_user = utils.get_session_token(data_session)
            ecg_serv.save_ann_temp(pt_ini, pt_fin, rutafile, nLead, token_user)
            
            return info_xi, info_yi, info_xf, info_yf, pt_ini, pt_fin, "1"
    
    app.logger.info("@callback: FIN 'display_click_data()'")
    return info_xi, info_yi, info_xf, info_yf, "", "", ""



@app.callback(
    [Output("alert-ann",            "children"),
     Output("alert-ann",            "color"),
     Output("alert-ann-success",    "children"),
     Output("alert-ann-success",    "is_open")],
    [Input("estado-edit",           "value")],
    [State("point-fin",             "value")]
)
def change_msg_alert_ann(estatus_edit, pt_fin):
    app.logger.info("@callback: INICIO 'change_msg_alert_ann()' -> estatus_edit: " + str(estatus_edit))
    app.logger.info("@callback: INICIO 'change_msg_alert_ann()' -> pt_fin: " + str(pt_fin))
    
    if estatus_edit == "0":
        msg = "Seleccione el punto nuevo"
        return msg, "secondary", "", False
    elif estatus_edit == "1":
        msg = html.Div(children=[            
                html.P(
                "Nueva anotación en "            
                ),
                html.P(                
                "X: " + str(pt_fin["x"]) + "   Y: " + str(pt_fin["x"])
                )
            ]                  
        )        
        return "Seleccione la anotación a cambiar", "primary", msg, True
    
    return "Seleccione la anotación a cambiar", "primary", "", False



@app.callback(
    Output("up-fecha-edicion",      "value"),
    [Input("up-fecha-edicion-aux",  "value")],
    [State("url",                   "pathname")]
)
def up_fecha_edicion_sesion(val, url_sesion):
    app.logger.info("@callback: INICIO 'change_msg_alert_ann()' -> ENTRO PARA ACTUALIZAR LA SESION")
    id_token = url_sesion.split('/')[-1]
    
    if utils.is_not_empty(id_token):
        token_session = "session_" + id_token
        ecg_serv.update_sesion(token_session)
        
    raise dash.exceptions.PreventUpdate()

###############################################################################
############################## Main layout ####################################
###############################################################################
def layout():
    return html.Div([body, footer])

