#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 21:40:58 2019

@author: cristian
"""

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import ecg_factory as ecgf
import numpy as np
import datetime
import logging

from dash.dependencies import Input, Output, State

import plotly.graph_objs as go



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
layout = go.Layout(title = "Representacion de la Derivacion " + str(optsLeads[0]['value']),
                   hovermode = 'closest')


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

formulario = dbc.Form([
        
    dbc.FormGroup([
        dbc.Label("Desde url remota: ", html_for="url-rem-file"),
        dbc.Input(type="url", id="url-rem-file", placeholder="http://"),
    ]),
        
    html.P([
        html.Label("ó")
    ], style={'text-align': 'center'} ),
        
    dbc.FormGroup([
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
        html.Div(id='out-upload-file'),        
    ])
])

body = dbc.Container([
        
    html.H1(children='Formato ' + ecg.typeECG),
    
    
    html.Div([
        dbc.Button("Subir fichero", id="open", color="primary"),
        dbc.Modal(
            [
                dbc.ModalHeader("Cargar Fichero"),
                dbc.ModalBody([
                    formulario
                ]),
                dbc.ModalFooter([
                    dbc.Button("Cerrar", id="close", className="mr-1"),
                    dbc.Button("Procesar", id="save", color="success", 
                               className="col-md-2"),
                ]),
            ],
            id="modal",
            size="lg"
        ),
    ]),
        

    #Agregamos la figura
    dcc.Graph(id='plot', figure=fig),
    
    # Agregamos el dropdown
    html.P([
            html.Label("Elije una derivacion"),
            dcc.Dropdown(
                        id = 'opt', 
                        options = optsLeads,
                        value = optsLeads[0]['value'],
                        clearable=False
                    )
            ], style = {'width': '400px',
                        'fontSize' : '20px',
                        'padding-left' : '100px',
                        'display': 'inline-block'}
        ),
        
])





# Dash APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"])
logging.basicConfig(filename="ecgApp.log", level=logging.DEBUG, 
                    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")
app.layout = html.Div([navbar, body])



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




###############################################################################
############################### CALLBACKS #####################################
###############################################################################



# Agregamos el callback para actualizar el dropdown
@app.callback(Output('plot', 'figure'),
             [Input('opt', 'value')])
def update_figure(lead):
    # Actualizamos la derivacion de acuerdo a lo seleccionado en el dropdown
    app.logger.info("@callback: Inicio 'update_figure'")
    
    ejeY = signals[lead-1]
    ejeX = np.arange(0, len(ejeY), 1.0)/fs
                    
    ecg_trace = go.Scatter(x = ejeX, y = ejeY,
                    name = 'SF', mode='lines')
    layout = go.Layout(title = "Representacion de la Derivacion " + str(lead),
                   hovermode = 'closest')
    fig = go.Figure(data = [ecg_trace], layout = layout)
    return fig



@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks"), Input("save", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, n3, is_open):
    if n1 or n2 or n3:
        return not is_open
    return is_open



@app.callback(Output('out-upload-file', 'children'),
              [Input('upload-file', 'contents')],
              [State('upload-file', 'filename'),
               State('upload-file', 'last_modified')])
def update_file(list_contenidos, list_nombres, list_fechas):
    
    app.logger.info("@callback: Inicio 'update_file'")
    
    """if list_contenidos is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_contenidos, list_nombres, list_fechas)
        ]"""
        
    if list_nombres is not None:
        app.logger.info("el nombre del fichero es: " + list_nombres)
        app.logger.info("longitud del fichero?: " + str(len(list_contenidos)))
        return html.Div([
                    html.Span("Fichero seleccionado: "),
                    dbc.Badge(list_nombres, color="info", className="mr-1")
                    ],                
                )
    

        
###############################################################################
############################### RUNER APP #####################################
###############################################################################
if __name__ == '__main__':
    app.run_server(debug=True)
    