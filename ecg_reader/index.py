#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 21:40:58 2019

@author: cristian
"""

import json


import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import ecg_factory as ecgf
import numpy as np
import datetime
import logging
import base64
import os
import urllib2


from dash.dependencies import Input, Output, State

import plotly.graph_objs as go


DIR_UPLOAD_FILES = "./uploaded_files/"

# Factoria de ECG
ecgFactory = ecgf.ECGFactory()
        
#FORMATO PHYSIONET: ./sample-data/100
#FORMATO ISHNE:     ./matlab_ishne_code/ishne.ecg
ecg = ecgFactory.create_ECG("./matlab_ishne_code/ishne.ecg")
signals = ecg.signal
nLeads = ecg.header.nLeads
fs = ecg.header.samplingRate

#Datos de la señal (Y(x))
ejeY = signals[0]
ejeX = np.arange(0, len(ejeY), 1.0)/fs


                
############################## ##### #############################
############################## FRONT #############################
############################## ##### #############################
                
#Dropdown para elegir los leads del ECG
optsLeads = [ {'value': i+1, 'label': 'Derivacion '+ str(i+1)} for i in range(nLeads)]

#Objeto grafica
ecg_trace = go.Scatter(x = ejeX, y = ejeY,
                    name = 'SF', mode='lines')

print(optsLeads)
layout = go.Layout(title = "Representacion de la Derivación " + str(optsLeads[0]['value']),
                   hovermode = 'closest', clickmode= 'event+select', uirevision=True,
                   autosize=True, xaxis=dict(gridcolor="LightPink") )


fig = go.Figure(data = [ecg_trace], layout = layout)


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Link", href="#")),
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
    brand_href="#",
    sticky="top",
)
        

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


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
                 children=[
                        html.Div(id="msg-upfile"),
                        html.Div(id="div_file_aux", 
                                 children= html.Div(id='name_file_aux', style={'display': 'none'})
                       )
                    ]
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
        
         
controls_ecg = html.Div([
    
    html.Label("Elije una derivación"),
    
    dcc.Dropdown(
        id = 'optLeads',
        options = optsLeads,
        value = optsLeads[0]['value'],
        clearable=False             
    ),
        
])

modal_component = html.Div([
    dbc.ModalHeader("Cargar Fichero"),
    dbc.ModalBody([
        formulario
    ]),
    dbc.ModalFooter([
        html.Div(id="btn-eliminar-file",
                 children=dbc.Button("Eliminar fichero/s", id="eliminar-file",
                    className="mr-1", color="danger", disabled=True)
                 ),
        dbc.Button("Cerrar", id="close-upfile", className="mr-1"),
        html.Div(id="btn-proces",
                 children=dbc.Button("Procesar", id="proces-upfile", color="success", 
                    disabled=True),
                 ),
    ]),
])

display_ecg = html.Div([   
        
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
              style={'height': 600, 'width':1000}),
])
        
menu_ecg = html.Div([
    dbc.Button("HRV", id="hrvGraph", outline=True, color="danger", className="mr-1"),
    dbc.Button("Otro",id="otroGraph", outline=True, color="secondary", className="mr-1"),
    dbc.Button("Subir fichero", id="open-upfile", color="primary")
])



body = dbc.Container([
    dbc.Row([
     html.H1(children='Formato ' + ecg.typeECG)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                html.Div([
                    html.Label("")
                ])
            ]),
            dbc.Row([
                controls_ecg
            ]),
            dbc.Row([
                html.Div([
                    html.P("Edicion de punto."),
                    html.P(id="point-x", children=["eje X: "]),
                    dbc.Input(type="number", id="point-y", placeholder="eje Y"),
                    dbc.Button("Guardar", id="guardar-modif", color="success", n_clicks_timestamp=0),
                    dbc.Input(type="hidden", id="time-guardar-modif"),
                ])
            ])
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

footer = html.Div()



# Dash APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"])
logging.basicConfig(filename="ecgApp.log", level=logging.DEBUG, 
                    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
app.title = "ECGApp"
app.layout = html.Div([navbar, body, footer])



###############################################################################
############################## FUNCIONES AUXILIARES ###########################
###############################################################################

def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


def save_file_proces(nombre_file, contenido):
    ruta_fichero = DIR_UPLOAD_FILES + nombre_file
    content_type, content_string = contenido.split(',')
    decoded = base64.b64decode(content_string)
    
    fh = open(ruta_fichero, "wb")
    fh.write(decoded)
    fh.close()
    
    return None


def save_file_url(url_file):
    name_file = url_file.split('/')[-1]
    save_file = DIR_UPLOAD_FILES + name_file
    
    try:
        response = urllib2.urlopen(url_file)
        datatowrite = response.read()
        fh = open(save_file, "wb")
        fh.write(datatowrite)
        fh.close()    
        return name_file
    except:
        return None
   


def borrar_fichero(nombre_fichero):
    app.logger.info("def: INICIO 'borrar_fichero()'")
    ruta = DIR_UPLOAD_FILES + nombre_fichero
    app.logger.info("def: 'borrar_fichero()' -> url a borrar: " + str(ruta) )
    
    if os.path.exists(ruta):
        app.logger.info("def: 'borrar_fichero()' -> removiendo ruta" )
        os.remove(ruta)
    else:
        app.logger.info("def: 'borrar_fichero()'. El fichero con nombre '"+
                        nombre_fichero +"' no existe.")
        
    app.logger.info("def: FIN 'borrar_fichero()'")
    

def name_file_valid(nombre_file):
    if nombre_file is not None and nombre_file != "":
        return True
        
    return False    
###############################################################################
############################### CALLBACKS #####################################
###############################################################################



# Agregamos el callback para actualizar el dropdown
@app.callback(Output('plot', 'figure'),
             [Input('optLeads', 'value'),
              Input("guardar-modif", "n_clicks_timestamp"),
              Input("point-x", "children"),
              Input("point-y", "value")],
              )
def update_figure(lead, curr_click, point_x, point_y ):
    # Actualizamos la derivacion de acuerdo a lo seleccionado en el dropdown
    app.logger.info("@callback: Inicio 'update_figure()'")
    ejeY = signals[lead-1]
    ejeX = np.arange(0, len(ejeY), 1.0)/fs
    
    app.logger.info("@callback: 'update_figure() -> tclicks: '" + str(curr_click))
        
    if point_x is not None and point_y is not None:    
        app.logger.info("@callback: 'update_figure()' -> point-x: " + str(point_x))
        app.logger.info("@callback: 'update_figure()' -> point-y: " + str(point_y))
        val_pt_x = point_x.split(": ")[1]
        data_x = float(val_pt_x) * fs
        data_x = int(data_x)
        ejeY[data_x] = float(point_y)
        app.logger.info("@callback: 'update_figure()' -> data-x: " + str(data_x))
    
   
                    
    ecg_trace = go.Scatter(x = ejeX, y = ejeY,
                    name = 'SF', mode='lines')
    layout = go.Layout(title = "Representacion de la Derivacion " + str(lead),
                   hovermode = 'closest', uirevision=True, autosize=True, 
                   xaxis=dict(gridcolor="LightPink"), yaxis=dict(gridcolor="LightPink") )
    fig = go.Figure(data = [ecg_trace], layout = layout)
    
    app.logger.info("@callback: FIN 'update_figure()'")
    return fig



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
    
    if name_file_valid(name_file):
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
)
def delete_file(eliminar_file, name_file):
    
    app.logger.info("@callback: INICIO 'delete_file()'")
    app.logger.info( "@callback: delete_file() -> eliminar_file: " + str(eliminar_file) )

    if eliminar_file <= 0 or name_file is None:
        app.logger.info("@callback: FIN by exception 'delete_file()'")
        raise dash.exceptions.PreventUpdate()
    
    if name_file is not None:   
        app.logger.info( "@callback: 'delete_file(): Borrando fichero: '" + str(name_file) )        
        borrar_fichero(name_file)
        
        container = html.Div([
                        html.Div(id="msg-upfile"),
                        html.Div(id="div_file_aux",
                                 children= html.Div(id='name_file_aux', style={'display': 'none'})
                       )
                    ])
        btn_procesar = dbc.Button("Procesar", id="proces-upfile", color="success", 
                disabled=True)
        
        btn_eliminar = dbc.Button("Eliminar fichero/s", id="eliminar-file", n_clicks=None,
                                className="mr-1", color="danger", disabled=True)

        app.logger.info( "@callback: FIN 'delete_file()'" )
        
        return [container, btn_procesar, btn_eliminar, "", uploader]
        
    


@app.callback([Output('proces-upfile', 'disabled'),
               Output('msg-upfile', 'children'),
               Output("eliminar-file", "disabled"),
               Output("div_file_aux", "children"),
               Output("url-rem-file", "disabled")],
              [Input('upload-file', 'contents'),
               Input('url-rem-file', 'value')],
              [State('upload-file', 'filename'),
               State('upload-file', 'last_modified')])
def update_file(list_contenidos, val_url, list_nombres, list_fechas):
    
    app.logger.info("@callback: INICIO 'update_file()'")
    app.logger.info( "url?: " + str(val_url) )
    app.logger.info( "nombre uploader?: " + str(list_nombres) )
    
    nombre_file = ''
    
    if list_contenidos is not None or name_file_valid(val_url):
        app.logger.info( "@callback: 'update_file() -> list_contenidos is None?: " + str(list_contenidos is None) )
        app.logger.info( "@callback: 'update_file() -> val_url: " + str(val_url) )        
        app.logger.info( "@callback: 'update_file() -> list_nombres: " + str(list_nombres) )
        
        if val_url is not None and val_url != '':
            nombre_file = val_url
            app.logger.info("el nombre del fichero URL es: " + str(nombre_file) )
            nombre_file = save_file_url(nombre_file)
            
        elif list_contenidos is not None :
            nombre_file = list_nombres
            app.logger.info("el nombre del fichero UPL es: " + str(nombre_file) )
            app.logger.info("el contenido del fichero UPL es None?: " + str(list_contenidos is None) )
            save_file_proces(nombre_file, list_contenidos)
            

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



### Modificacion de puntos de la grafica

@app.callback(
    [Output("point-x", "children"),
     Output("point-y", "value")],
    [Input('plot', 'clickData')])
def display_click_data(clickData):
    app.logger.info("@callback: INICIO 'display_click_data()'")
    if clickData is None:
        raise dash.exceptions.PreventUpdate()
        
    data_json = json.dumps(clickData, indent=2)
    y = json.loads(data_json)
    app.logger.info("@callback: 'display_click_data() -> data_json: " + str(data_json))
    app.logger.info("@callback: 'display_click_data() -> data_python: " + str(y["points"][0]["x"]))
    app.logger.info("@callback: FIN 'display_click_data()'")
    return "eje X: " + str(y["points"][0]["x"]), y["points"][0]["y"]


@app.callback(
    Output("time-guardar-modif", "value"),
    [Input("guardar-modif", "n_clicks_timestamp")]
)
def savetime_guardar_modif(time_click):
    app.logger.info("*** @callback: INICIO 'savetime_guardar_modif()")
    if time_click > 0:
        app.logger.info("*** @callback: 'savetime_guardar_modif() -> time_click: " + str(time_click))
        return time_click
###############################################################################
############################### RUNER APP #####################################
###############################################################################
if __name__ == '__main__':
    app.run_server(debug=True)
    