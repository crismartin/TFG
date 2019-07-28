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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



# leemos el ECG que queremos representar
# leemos el ECG que queremos representar
ecgFactory = ecgf.ECGFactory()
ecg = ecgFactory.create_ECG("./matlab_ishne_code/ishne.ecg")

ecgFirstChannel = ecg.getSignal().getECGArray()[0]
fs = ecg.getHeader().samplingRate
offset = 30

channel = ecgFirstChannel[offset:12000] ## ¿De donde salia lo del 12k??
x = np.arange(0, len(channel), 1.0)/fs
             
             


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash App'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': x, 'y': channel, 'type': 'lines', 'name': 'SF'},
                
            ],
            'layout': {
                'title': 'Representación de ECG'
            }
        }
    ),


    html.Div(children=[html.A(html.Button('Reload Page!', className='three columns'), 
                                                    href='http://localhost:8050/')])
])


if __name__ == '__main__':
    app.run_server(debug=True)