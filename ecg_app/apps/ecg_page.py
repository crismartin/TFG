#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:47:58 2019

@author: cristian
"""

import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

import utils_ecg as utils
import ecg_service as ecg_serv

from app import app


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
                    html.Span("Fichero seleccionado: "),
                    dbc.Badge(id="lbl_name_file", color="info", className="mr-1")
                ])

cnt_msg_upfile = html.Div([
                        html.Div(id="msg-upfile", children=msg_file)
                    ])

msg_file_ant = html.Div([
                        html.Span("Fichero seleccionado: "),
                        dbc.Badge(id="lbl_name_file_ant", color="info", className="mr-1")]               
                    )

cnt_msg_upfile_ant = html.Div([
                        html.Div(id="msg-upfile-ant", children=msg_file_ant)
                    ])                        

uploader = html.Div([
            dcc.Upload(id="upload-file",
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
                            "Error! El fichero no tiene un formato válido o está incompleto",
                            id="alert-format",
                            is_open=False,
                            color="danger"
                        )
                    ])
            ])
                        
                        
uploader_ant = html.Div([
                dcc.Upload(id="upload-ant",
                    children=html.Div([
                        'Arrastra y suelta o ',
                        html.A('selecciona un archivo')
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
                    multiple=False
                ),
                html.Div(id='container-upfile-ant',
                         children=[cnt_msg_upfile_ant]
                         )
            ])
  

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
        
    dbc.FormGroup(id="form-uploader", children = uploader),
])



formulario = dbc.Form([
    form_datos_ecg,    
    #dbc.FormGroup(id="form-optional", children= collapse )
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
])

cnt_state_fant =  html.Div([
        dbc.Input( id="st-up-ant",    type="hidden"),        
])

modal_component = html.Div([
    dbc.ModalHeader("Cargar Fichero"),
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

ecg_fig = dcc.Graph(id='ecg-fig', 
              figure=fig_default,
              style={'height': 600, 'width':900})


display_ecg = dbc.FormGroup([   
        
    html.Div([       
        dbc.Modal(
            children = modal_component,
            id = "modal",
            size = "lg"
        ),
    ]),
    
    html.Div(id="cnt-ecg-fig", children=ecg_fig)
])
    
        
menu_ecg = html.Div([
    dbc.Button("HRV", id="hrvGraph", outline=True, color="danger", className="mr-1"),
    dbc.Button("Otro",id="otroGraph", outline=True, color="secondary", className="mr-1"),
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

edit_point_input = dbc.FormGroup([
        
    dbc.Row([
        html.H6("Editar Punto"),    
    ]),
    
    dbc.FormGroup([
        dbc.Label("X:", html_for="point-x", width=2),
        dbc.Col(
            dbc.Input(
                type="number", id="point-x", disabled=True
            ),
            width=10,
        ),
    ], row=True),
                    
    dbc.FormGroup([
        dbc.Label("Y:", html_for="point-y", width=2),
        dbc.Col(
            dbc.Input(
                type="number", id="point-y", disabled=True
            ),
            width=10,
        ),
    ], row=True),
                    
    dbc.FormGroup([
        dbc.Col([
            dbc.Button(id="guardar-modif", color="success",
               children=[
                   html.Span([html.I(className="fas fa-floppy-o ml-2"), " Guardar"])
                  ]
            )
        ])
        
    ], className="float-right", row=True)
])

title_controls =  dbc.FormGroup([
                    html.H2("Controles", id="controles-title", style={'text-align': 'left'})
                  ], row=True)

form_controls = html.Div(id="form-controls", children=[title_controls, dropdown_leads, edit_point_input])

cnt_form_controls = dbc.Form(id="cnt-form-controls", children=form_controls)

title_format = html.H1("Formato", id="formato-title", style={'textAlign': 'center'})


body = dbc.Container([
    html.Div(id="cnt-title-format", children=title_format),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                cnt_form_controls
            ]),
        ], width=2),
        dbc.Col([
            dbc.Row(
                display_ecg,
                className="float-right"
            ),
            dbc.Row(
                menu_ecg, className="float-right"
            )
        ], width=10)  
    ])    
    
])


footer = html.Div([
            dbc.Input(type="hidden", id="fname_process")
        ])



###############################################################################
############################### CALLBACKS #####################################
###############################################################################


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
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
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
    Output("upload-ant", "disabled"),
    [Input("url-ant-file","value")]       
)
def disabled_uploader_ant(name_file):
    if utils.name_file_valid(name_file):
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
     Output("alert-format",     "is_open")],
    [Input("st-valid-data",     "value")],
)
def activar_btn_process(is_file_valid):
    app.logger.info("@callback: INICIO 'activar_btn_process()'")
    
    if is_file_valid is None:
        app.logger.info( "@callback: FIN 'activar_btn_process()'" )
        return True, False
    
    app.logger.info( "@callback: 'activar_btn_process()' -> is_file_valid: " + str(is_file_valid) )
    app.logger.info( "@callback: FIN 'activar_btn_process()'" )
    return not is_file_valid, not is_file_valid
    


@app.callback(
    [Output('container-upfile',     'children'),
     Output("input-component",      "children"),
     Output("input-component-hed",  "children"),
     Output("input-component-ant",  "children"),
     Output("form-uploader",        "children"),
     Output("cnt-st-fdata",         "children"),
     Output("cnt-ecg-fig",          "children"),
     Output("cnt-form-controls",    "children"),
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
    
    return [cnt_msg_upfile, input_component, input_component_hed, input_component_ant, 
            uploader, cnt_state_fdata, ecg_fig, cnt_form_controls, title_format]
    


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
    app.logger.info( "@callback: 'updload_file() -> token_user: " + str(utils.get_session_token(data_session)) )
    app.logger.info( "@callback: 'updload_file() -> list_nombres: " + str(list_nombres) )
    
    list_nombres = list_nombres or get_list_fname( url_head, url_ant, url_data )
    
    app.logger.info( "@callback: 'updload_file() -> list_nombres definitivo: " + str(list_nombres) )
    
    if utils.name_file_valid(url_data) or list_contents is not None:

        token_user = utils.get_session_token(data_session)                 
        msg_error, fichero_valido, nombre_file = ecg_serv.guardar_ficheros(list_contents, list_nombres, token_user)
        
        if fichero_valido:
            return [nombre_file, True, True, True, True, fichero_valido, msg_error]
        
        else:
            return [None, False, False, False, True, False, msg_error]
    
    else:    
        app.logger.info("@callback: FIN by None content 'updload_file()'")
        return [None, False, False, False, False, None, None]



@app.callback(
    Output("fname_process", "value"),
    [Input("proces-upfile", "n_clicks")],
    [State("session", "data"),
     State("lbl_name_file", "children")]
)
def process_file(click_button, data_session, name_file):
    app.logger.info("@callback: INICIO 'process_file()'")
    
    app.logger.info("@callback: 'process_file()' -> name_file: " + str(name_file) )
    
    if click_button <= 0:
        app.logger.info("@callback: FIN 'process_file()': 'click' Exception")
        raise dash.exceptions.PreventUpdate()

    token_user = utils.get_session_token(data_session)

    app.logger.info("@callback: FIN 'process_file()'")
    ruta_file = token_user + "/" + name_file
    
    return ruta_file



@app.callback(
    [Output("optLeads","disabled"),
     Output("optLeads","options"),
     Output("optLeads","value")],
    [Input("fname_process", "value")]
)
def select_first_lead(fname_uploaded):
    app.logger.info("@callback: INICIO 'select_first_lead()'")
    
    if fname_uploaded is not None:
        app.logger.info("@callback: 'select_first_lead()' -> Configurando parametros para pintar")
        ruta_file = utils.dir_files + fname_uploaded
        app.logger.info("@callback: 'select_first_lead()' -> ruta_file: " + str(ruta_file))
        app.logger.info("@callback: 'select_first_lead()' -> Obteniendo leads...")
        optLeads = ecg_serv.get_nleads_array(ruta_file)
        app.logger.info("@callback: 'select_first_lead()' -> optLeads: " + str(optLeads))
        app.logger.info("@callback: FIN 'select_first_lead()'")
        return False, optLeads, 1
    
    app.logger.info("@callback: FIN 'select_first_lead()'")

    return True, None, None



@app.callback(
    [Output("ecg-fig", "figure"),
     Output("formato-title", "children"),
     Output("point-y", "disabled")],
    [Input("optLeads", "value")],
    [State("fname_process", "value")]
)
def print_ecg_lead(selected_lead, fname_uploaded):
    app.logger.info("@callback: INICIO 'print_ecg()'")
    
    app.logger.info("@callback: 'print_ecg()' -> selected_lead: " + str(selected_lead))
    app.logger.info("@callback: 'print_ecg()' -> fname_uploaded: " + str(fname_uploaded))
    
    if fname_uploaded is None or selected_lead is None:
        app.logger.info("@callback: FIN 'print_ecg()' by Exception")
        raise dash.exceptions.PreventUpdate()
        
    app.logger.info("@callback: 'print_ecg()' -> Configurando parametros para pintar")
    ruta_file = utils.dir_files + fname_uploaded
    app.logger.info("@callback: 'print_ecg()' -> ruta_file: " + str(ruta_file))
    app.logger.info("@callback: 'print_ecg()' -> Pintando datos...")
    
    fig, title = ecg_serv.build_plot_by_lead(ruta_file, selected_lead)
    app.logger.info("@callback: FIN 'print_ecg()'")
    return fig, title, False
    

###############################################################################
############################## Main layout ####################################
###############################################################################
def layout():
    return html.Div([body, footer])

