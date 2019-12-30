#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 13:29:20 2019

@author: cristian
"""


import utils_ecg as utils
import constantes_ecg as cte
import numpy as np
from ecg_reader import ecg_factory as ecgf

import plotly.graph_objs as go

from app import app



def build_select_leads(nleads):
    return [ {'value': i+1, 'label': 'Derivacion '+ str(i+1)} for i in range(nleads)]
    


def get_nleads_array(file_name):
    # Factoria de ECG
    ecgFactory = ecgf.ECGFactory()
    
    ecg = ecgFactory.create_ECG(file_name)
    nLeads = ecg.header.nLeads    
    
    return build_select_leads(nLeads)    
    

def build_data_annt(ecg, signal):
    ant_trace = []
    anotaciones = ecg.annt
        
    if anotaciones is not None:
        fs = ecg.header.samplingRate
        ant_ejeX = anotaciones.sample
        ant_ejeX = ant_ejeX / float(fs)        
        ant_ejeX = np.around(ant_ejeX, decimals=5)
        ant_ejeX = ant_ejeX.tolist()        
        app.logger.info("[ecg_service] - 'build_plot_by_lead() ->  ant_ejeX: " + str(len(ant_ejeX)) )        
        ant_ejeY = signal[anotaciones.sample]
        app.logger.info("[ecg_service] - 'build_plot_by_lead() ->  ant_ejeY: " + str(ant_ejeY) )
        simbols = anotaciones.symbol
        ant_trace = go.Scatter(x = ant_ejeX, y = ant_ejeY,
                        name = 'Anotaciones', mode='markers+text', 
                        text=simbols, textposition="top right")
    return ant_trace
    

def build_plot_by_lead(file_name, lead):
    ecgFactory = ecgf.ECGFactory()    
    ecg = ecgFactory.create_ECG(file_name)
    
    signals = ecg.signal
    nLeads = ecg.header.nLeads
    fs = ecg.header.samplingRate
    title = "Formato " + ecg.typeECG
    
    if lead > nLeads:
        return None    
    
    #Datos de la señal (Y(x))
    ejeY = signals[lead-1]
    ejeX = np.arange(0, len(ejeY), 1.0)/fs
    
    optsLeads = build_select_leads(nLeads)
    
    layout = go.Layout(title = "Representacion de la Derivación " + str(optsLeads[lead-1]['value']),
                    hovermode = 'closest', uirevision=True, autosize=True, 
                    xaxis=dict(gridcolor="LightPink", range=[0, 12]), 
                    yaxis=dict(gridcolor="LightPink"),
                    plot_bgcolor='rgb(248,248,248)'
                    )
        
    ecg_trace = go.Scatter(x = ejeX, y = ejeY,
                    name = 'ECG', mode='lines')
    
    
    # Datos de las anotaciones    
    ant_trace = build_data_annt(ecg, ejeY)
        
    #Objeto grafica
    fig = go.Figure(data = [ecg_trace, ant_trace], layout = layout)
    
    return fig, title


def delete_file_system(token_user, name_file):
    ruta_fichero = token_user + "/" + name_file
    utils.borrar_fichero(ruta_fichero)
    
    

def upload_file(nombre_file, content_file, token_user):
    app.logger.info("** INICIO 'update_file()")
        
    if content_file is not None:
        nombre_file = nombre_file
        app.logger.info("** 'update_file() -> el nombre del fichero UPL es: " + str(nombre_file) )
        app.logger.info("** 'update_file() -> el contenido del fichero UPL es None?: " + str(content_file is None) )
        utils.save_file_proces(token_user, nombre_file, content_file)
    
    ruta_fichero = cte.DIR_UPLOAD_FILES + token_user + "/" + nombre_file
    app.logger.info( "** 'update_file()' -> ruta_fichero: " + str(ruta_fichero) )
    
    app.logger.info("** FIN 'update_file()")
    return nombre_file, ruta_fichero



def upload_file_by_url(file_url, token_user):
    app.logger.info("** INICIO 'upload_file_by_url()")
    
    if utils.name_file_valid(file_url):
        nombre_file = file_url
        app.logger.info("** 'upload_file_by_url() -> el nombre del fichero URL es: " + str(nombre_file) )
        nombre_file = utils.download_file_url(token_user, nombre_file)
        
    ruta_fichero = cte.DIR_UPLOAD_FILES + token_user + "/" + nombre_file
    app.logger.info( "** 'upload_file_by_url()' -> ruta_fichero: " + str(ruta_fichero) )
    
    app.logger.info("** FIN 'upload_file_by_url()")
    return nombre_file, ruta_fichero    