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

from dash.dependencies import Input, Output

import plotly.graph_objs as go



# Factoria de ECG
ecgFactory = ecgf.ECGFactory()
        
#FORMATO PHYSIONET: ./sample-data/100
#FORMATO ISHNE:     ./matlab_ishne_code/ishne.ecg
ecg = ecgFactory.create_ECG("./sample-data/100")
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

body = dbc.Container([
        
    html.H1(children='Formato ' + ecg.typeECG),

    #Agregamos la figura
    dcc.Graph(id='plot', figure=fig),
    
    # Agregamos el dropdown
    html.P([
        html.Label("Elije una derivacion"),
        dcc.Dropdown(id = 'opt', 
                     options = optsLeads,
                     value = optsLeads[0]['value'],
                     clearable=False)
            ], style = {'width': '400px',
                        'fontSize' : '20px',
                        'padding-left' : '100px',
                        'display': 'inline-block'})
])


# Dash APP
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([navbar, body])
    
# Agregamos el callback para actualizar el dropdown
@app.callback(Output('plot', 'figure'),
             [Input('opt', 'value')])
def update_figure(lead):
    # Actualizamos la derivacion de acuerdo a lo seleccionado en el dropdown
    print(lead)
    ejeY = signals[lead-1]
    ejeX = np.arange(0, len(ejeY), 1.0)/fs
                    
    ecg_trace = go.Scatter(x = ejeX, y = ejeY,
                    name = 'SF', mode='lines')
    layout = go.Layout(title = "Representacion de la Derivacion " + str(lead),
                   hovermode = 'closest')
    fig = go.Figure(data = [ecg_trace], layout = layout)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)