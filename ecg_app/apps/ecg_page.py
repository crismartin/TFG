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
import constantes_ecg as cte

import numpy as np

from ecg_reader import ecg_factory as ecgf
from app import app

fig = go.Figure()


spiner_loading = html.Div([
    dbc.Button(
        [dbc.Spinner(size="sm"), " Loading..."],
        color="primary",
        disabled=True,
    )
])


cnt_msg_upfile = html.Div([
                        html.Div(id="msg-upfile"),
                        html.Div(id="div_file_aux",
                                 children= html.Div(id='name_file_aux', style={'display': 'none'})
                       )
                    ])
                        

uploader = html.Div([
        dcc.Upload(
            id="upload-file",
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
        html.Div(id='container-upfile',
                 children=[cnt_msg_upfile]
                 ),
        ])

input_component = dbc.Input(type="url", id="url-rem-file", placeholder="http://")


formulario = dbc.Form([
        
    dbc.FormGroup([
        dbc.Label("Desde url remota: ", html_for="url-rem-file"),
        html.Div(id="input-component", children = input_component)
    ]),
        
    html.P([
        html.Label("ó")
    ], style={'text-align': 'center'} ),
        
    dbc.FormGroup(id="form-uploader",children = uploader),
             
])


btn_procesar = dbc.Button(id="proces-upfile", color="success", 
                          children=[
                                html.Span([html.I(className="fas fa-cogs ml-2"), " Procesar"])
                             ], disabled=True)

btn_eliminar = dbc.Button(id="eliminar-file", n_clicks=None,
                          className="mr-1", color="danger", disabled=True,
                          children=[
                             html.Span([html.I(className="fas fa-trash ml-2"), " Borrar fichero/s"])
                          ])

btn_cerrar_modal = dbc.Button(id="close-upfile", n_clicks=None, className="mr-1",
                              children=[
                                html.Span([html.I(className="fas fa-times ml-2"), " Cancelar"])
                             ])

modal_component = html.Div([
    dbc.ModalHeader("Cargar Fichero"),
    dbc.ModalBody([
        formulario
    ]),
    dbc.ModalFooter([
        html.Div( id="btn-eliminar-file", children=[btn_eliminar] ),
        btn_cerrar_modal,
        html.Div( id="btn-proces", children=[btn_procesar] ),
    ]),
])



display_ecg = dbc.FormGroup([   
        
    html.Div([       
        dbc.Modal(
            children = modal_component,
            id = "modal",
            size = "lg"
        ),
    ]),
    
    #Agregamos la figura
    dcc.Graph(id='plot', 
              figure=fig,
              style={'height': 600, 'width':900}),
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


controls_ecg = dbc.FormGroup([
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
                type="number", id="point-y"
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


form_controls = dbc.Form(id="form-controls", 
                         children=[controls_ecg, edit_point_input]
)


body = dbc.Container([
    dbc.Row([
        html.H1(id="formato-title", children='Formato')
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Row(),
            dbc.Row(),
            dbc.Row(form_controls),
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
########################## FUNCIONES AUXILIARES ###############################
###############################################################################


def getTokenUser():
    token_user = utils.generateTokenSession()
    return dbc.Input(id="token-user", type="hidden", value=token_user)


def build_select_leads(nleads):
    return [ {'value': i+1, 'label': 'Derivacion '+ str(i+1)} for i in range(nleads)]
    
    

def get_nleads_array(file_name):
    # Factoria de ECG
    ecgFactory = ecgf.ECGFactory()
    
    ecg = ecgFactory.create_ECG(file_name)
    nLeads = ecg.header.nLeads    
    
    return build_select_leads(nLeads)    
    


def build_plot_by_lead(file_name, lead):
    ecgFactory = ecgf.ECGFactory()    
    ecg = ecgFactory.create_ECG(file_name)
    
    signals = ecg.signal
    nLeads = ecg.header.nLeads
    fs = ecg.header.samplingRate
    
    if lead > nLeads:
        return None    
    
    #Datos de la señal (Y(x))
    ejeY = signals[lead-1]
    ejeX = np.arange(0, len(ejeY), 1.0)/fs
    
    optsLeads = build_select_leads(nLeads)
    
    layout = go.Layout(title = "Representacion de la Derivación " + str(optsLeads[lead-1]['value']),
                    hovermode = 'closest', uirevision=True, autosize=True, 
                    xaxis=dict(gridcolor="LightPink", range=[0, 12]), 
                    yaxis=dict(gridcolor="LightPink")  
                    )
    
    #Objeto grafica
    ecg_trace = go.Scatter(x = ejeX, y = ejeY,
                    name = 'SF', mode='lines')
    
    fig = go.Figure(data = [ecg_trace], layout = layout)
    
    return fig

    
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
    if n1 or n2 or n3:
        return not is_open
    return is_open



@app.callback(
    Output("upload-file", "disabled"),
    [Input("url-rem-file","value")]       
)
def disabled_uploader(name_file):
    
    if utils.name_file_valid(name_file):
        return True
    else:
        return False



@app.callback(
    [Output('container-upfile', 'children'),
     Output("btn-proces", "children"),
     Output("btn-eliminar-file", "children"),
     Output("url-rem-file", "value"),
     Output("form-uploader", "children")],
    [Input("eliminar-file", "n_clicks"),
     Input("name_file_aux", "children")],
    [State("session", "data")]
)
def delete_file(eliminar_file, name_file, data_session):
    
    app.logger.info("@callback: INICIO 'delete_file()'")
    app.logger.info( "@callback: delete_file() -> eliminar_file: " + str(eliminar_file) )
    token_user = utils.get_session_token(data_session)
    app.logger.info( "@callback: delete_file() -> token_user: " + str(token_user) )

    if eliminar_file <= 0 or name_file is None:
        app.logger.info("@callback: FIN by exception 'delete_file()'")
        raise dash.exceptions.PreventUpdate()
    
    if name_file is not None:   
        app.logger.info( "@callback: 'delete_file(): Borrando fichero: '" + str(name_file) )        
        ruta_fichero = token_user + "/" + name_file
        utils.borrar_fichero(ruta_fichero)
                
        btn_eliminar = dbc.Button("Eliminar fichero/s", id="eliminar-file", n_clicks=None,
                                className="mr-1", color="danger", disabled=True)

        app.logger.info( "@callback: FIN 'delete_file()'" )
        
        return [cnt_msg_upfile, btn_procesar, btn_eliminar, "", uploader]
    
    

@app.callback([Output('proces-upfile', 'disabled'),
               Output('msg-upfile', 'children'),
               Output("eliminar-file", "disabled"),
               Output("div_file_aux", "children"),
               Output("url-rem-file", "disabled")],
              [Input('upload-file', 'contents'),
               Input('url-rem-file', 'value')],
              [State('upload-file', 'filename'),
               State('upload-file', 'last_modified'),
               State("session", "data")])
def update_file(list_contenidos, val_url, list_nombres, list_fechas, data_session):
    
    app.logger.info( "@callback: INICIO 'update_file()'" )
    app.logger.info( "@callback: 'update_file() -> val_url: " + str(val_url) )
    app.logger.info( "@callback: 'update_file() -> list_nombres: " + str(list_nombres) )
    app.logger.info( "@callback: 'update_file() -> token_user: " + str(utils.get_session_token(data_session)) )
    
    nombre_file = ''
    token_user = utils.get_session_token(data_session)
    
    if list_contenidos is not None or utils.name_file_valid(val_url):
        app.logger.info( "@callback: 'update_file() -> list_contenidos is None?: " + str(list_contenidos is None) )
        app.logger.info( "@callback: 'update_file() -> val_url: " + str(val_url) )        
        app.logger.info( "@callback: 'update_file() -> list_nombres: " + str(list_nombres) )
        
        if val_url is not None and val_url != '':
            nombre_file = val_url
            app.logger.info("el nombre del fichero URL es: " + str(nombre_file) )
            nombre_file = utils.download_file_url(token_user, nombre_file)
            
        elif list_contenidos is not None :
            nombre_file = list_nombres
            app.logger.info("el nombre del fichero UPL es: " + str(nombre_file) )
            app.logger.info("el contenido del fichero UPL es None?: " + str(list_contenidos is None) )
            utils.save_file_proces(token_user, nombre_file, list_contenidos)
            

        msg_file = html.Div([
                        html.Span("Fichero seleccionado: "),
                        dbc.Badge(nombre_file, color="info", className="mr-1", id="lbl_name_file")]               
                    )
                
        name_file_aux = html.Div(nombre_file, id='name_file_aux', style={'display': 'none'})
    
        app.logger.info("@callback: FIN 'update_file()'")
    
        return [False, msg_file, False, name_file_aux, True]
    
    else:
        
        name_file_aux = html.Div(nombre_file, id='name_file_aux', style={'display': 'none'})
        app.logger.info("@callback: FIN 'update_file()'")
        return [True, None, True, nombre_file, False]



@app.callback(
    Output("fname_process", "value"),
    [Input("proces-upfile", "n_clicks")],
    [State("session", "data"),
     State("lbl_name_file", "children")]
)
def process_file(click_button, data_session, name_file):
    app.logger.info("@callback: INICIO 'process_file()'")
    
    app.logger.info("@callback: 'process_file()' -> token_session: " + str(name_file) )
    
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
        ruta_file = cte.DIR_UPLOAD_FILES + fname_uploaded
        app.logger.info("@callback: 'select_first_lead()' -> ruta_file: " + str(ruta_file))
        app.logger.info("@callback: 'select_first_lead()' -> Obteniendo leads...")
        optLeads = get_nleads_array(ruta_file)
        app.logger.info("@callback: 'select_first_lead()' -> optLeads: " + str(optLeads))
        app.logger.info("@callback: FIN 'select_first_lead()'")
        return False, optLeads, 1
    
    app.logger.info("@callback: FIN 'select_first_lead()'")

    return True, None, None



@app.callback(
    Output("plot", "figure"),
    [Input("optLeads", "value"),
     Input("fname_process", "value")]
)
def print_ecg_lead(selected_lead, fname_uploaded):
    app.logger.info("@callback: INICIO 'print_ecg()'")
    
    app.logger.info("@callback: 'print_ecg()' -> selected_lead: " + str(selected_lead))

    app.logger.info("@callback: 'print_ecg()' -> fname_uploaded: " + str(fname_uploaded))
    
    if fname_uploaded is None or selected_lead is None:
        app.logger.info("@callback: FIN 'print_ecg()' by Exception")
        raise dash.exceptions.PreventUpdate()
    
    
    app.logger.info("@callback: 'print_ecg()' -> Configurando parametros para pintar")
    ruta_file = cte.DIR_UPLOAD_FILES + fname_uploaded
    app.logger.info("@callback: 'print_ecg()' -> ruta_file: " + str(ruta_file))
    app.logger.info("@callback: 'print_ecg()' -> Pintando datos...")
    
    fig = build_plot_by_lead(ruta_file, selected_lead)
    app.logger.info("@callback: FIN 'print_ecg()'")
    return fig
    

###############################################################################
############################## Main layout ####################################
###############################################################################
def layout():
    return html.Div([body, footer])

