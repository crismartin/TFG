#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 21:40:58 2019

@author: cristian
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import ecg_factory as ecgf
import numpy as np

from dash.dependencies import Input, Output

import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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


                
#Dropdown para elegir los leads del ECG
optsLeads = [ {'value': i+1, 'label': 'Derivacion '+ str(i+1)} for i in range(nLeads)]
print(optsLeads)

#Objeto grafica
ecg_trace = go.Scatter(x = ejeX, y = ejeY,
                    name = 'SF', mode='lines')

layout = go.Layout(title = 'Representacion de ECG con formato ' + ecg.typeECG,
                   hovermode = 'closest')


fig = go.Figure(data = [ecg_trace], layout = layout)

print("esto se hace!")

#Creamos el Dash Layout

app.layout = html.Div(children=[
    html.H1(children='ECG App'),

             
    #Agregamos la figura
    dcc.Graph(id='plot', figure=fig),
    
    # Agregamos el dropdown
    html.P([
        html.Label("Elije una derivacion"),
        dcc.Dropdown(id = 'opt', 
                     options = optsLeads,
                     value = optsLeads[0]['value'])
            ], style = {'width': '400px',
                        'fontSize' : '20px',
                        'padding-left' : '100px',
                        'display': 'inline-block'})
    
])
    
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
    fig = go.Figure(data = [ecg_trace], layout = layout)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)