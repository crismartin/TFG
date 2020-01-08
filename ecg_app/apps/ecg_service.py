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
    ant_trace = None
    anotaciones = ecg.annt
        
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  anotaciones: " + str(anotaciones))
    if anotaciones.ann_len is not None:
        fs = ecg.header.samplingRate
        ant_ejeX = anotaciones.sample
        ant_ejeX = ant_ejeX / float(fs)        
        ant_ejeX = np.around(ant_ejeX, decimals=5)
        ant_ejeX = ant_ejeX.tolist()        
        app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  ant_ejeX: " + str(len(ant_ejeX)) )        
        ant_ejeY = signal[anotaciones.sample]
        app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  ant_ejeY: " + str(ant_ejeY) )
        simbols = anotaciones.symbol
        ant_trace = go.Scatter(x = ant_ejeX, y = ant_ejeY,
                        name = 'Anotaciones', mode='markers+text', 
                        text=simbols, textposition="top right")
    return ant_trace
    


def build_plot_by_lead(file_name, lead):
    data_fig = []
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
    
    data_fig.append(ecg_trace)
    
    # Datos de las anotaciones    
    ant_trace = build_data_annt(ecg, ejeY)
    
    if ant_trace is not None:
        data_fig.append(ant_trace)
    
    #Objeto grafica
    fig = go.Figure(data = data_fig, layout = layout)
    
    return fig, title



def delete_file_system(token_user, name_file):
    ruta_fichero = token_user + "/" + name_file
    utils.borrar_fichero(ruta_fichero)
    


# Devuelve una lista con el nombre de los ficheros que no tengan una ext valida
def check_ext_files(list_files):
    result = []
    
    if list_files is not None:
        for fname in list_files:
            fname = fname.split("/")[-1]
            ext_file = utils.get_ext_file(fname)
            print("Extension del fichero " + fname + ": " + ext_file )
            if ext_file not in cte.EXT_SUPPORTED:
                result.append(fname)
            
    return result



# Comprueba si existe o no un fichero de datos permitido
def check_data_file(list_files):
    has_file_data = False
    
    if list_files is not None:
        for fname in list_files:
            fname = fname.split("/")[-1]
            ext_file = utils.get_ext_file(fname)
            print("Extension del fichero " + fname + ": " + ext_file )
            if ext_file in cte.EXT_DATA_FILE:
                has_file_data = True
                break
    
    return has_file_data



# True si los ficheros tienen el mismo nombre raiz, False si no lo tienen
def has_rootname_files(list_files):
    result = []
    
    if list_files is not None:
        list_files = [utils.get_name_file(fname, True) for fname in list_files]
        fname_data = list_files[-1]        
        list_files.pop(-1)

        print("fname_data: " + str(fname_data))
        for fname in list_files:
            if fname.split(".")[0] != fname_data.split(".")[0]:
                result.append(fname)
            
    return result


    
def comprobar_ficheros(list_files):
    
    app.logger.info( "[ecg_service] - 'updload_file()' -> INICIO PASO 0. Comprobando fichero de datos" )
    has_file_data = check_data_file(list_files)
    if not has_file_data:
        msg = "Error! No se ha encontrado un fichero de datos ECG válido"
        app.logger.info( "[ecg_service] - 'updload_file()' -> FIN PASO 0. FAIL - No hay fichero de datos valido" )
        return msg
    app.logger.info( "[ecg_service] - 'updload_file()' -> INICIO PASO 0. SUCCESS" )
    
    
    app.logger.info( "[ecg_service] - 'updload_file()' -> INICIO PASO 1. Comprobando extensiones ficheros" )
    files_err_ext = check_ext_files(list_files)
    if len(files_err_ext) > 0 :
        app.logger.info( "[ecg_service] - 'updload_file()' -> files_err_ext: " + str(files_err_ext) )         
        msg = ", ".join(files_err_ext)
        app.logger.info( "[ecg_service] - 'updload_file()' -> msg: " + str(msg) )      
        msg = "Error! El/Los fichero/s [" + str(msg) + "] no tienen una extensión soportada"
        app.logger.info( "[ecg_service] - 'updload_file()' -> FIN PASO 1. FAIL - Detectadas extensiones no admitidas" )     
        return msg    
    app.logger.info( "[ecg_service] - 'updload_file()' -> FIN PASO 1. SUCCESS" )

    
    app.logger.info( "[ecg_service] - 'updload_file()' -> INICIO PASO 2. Comprobando mismo nombre raiz" )        
    files_err_ext = has_rootname_files(list_files)
    if len(files_err_ext) > 0:
        app.logger.info( "[ecg_service] - 'updload_file()' -> files_err_ext: " + str(files_err_ext) )        
        msg = ", ".join(files_err_ext)
        app.logger.info( "[ecg_service] - 'updload_file()' -> msg: " + str(msg) )
        msg = "Error! El/Los fichero/s [" + str(msg) + "] no tienen el mismo nombre raíz que el fichero de datos ECG"
        app.logger.info( "[ecg_service] - 'updload_file()' -> FIN PASO 2. FAIL - Detectados nombres no identicos" )
        return msg        
    app.logger.info( "[ecg_service] - 'updload_file()' -> FIN PASO 2. SUCCESS" )
    
    return None
    


# Guarda el fichero obtenido desde el contenedor
def upload_file_content(nombre_file, content_file, token_user):
    app.logger.info("[ecg_service] - INICIO 'upload_file_content()")
        
    if content_file is not None:        
        app.logger.info("[ecg_service] - 'upload_file_content()' -> el nombre del fichero UPL es: " + str(nombre_file) )
        app.logger.info("[ecg_service] - 'upload_file_content()' -> el contenido del fichero UPL es None?: " + str(content_file is None) )
        nombre_file, saved_file = utils.save_file_proces(token_user, nombre_file, content_file)
    
    #ruta_fichero = cte.DIR_UPLOAD_FILES + token_user + "/" + nombre_file if(nombre_file is not None) else None    
    app.logger.info( "[ecg_service] - 'upload_file_content()' -> nombre_file: " + str(nombre_file) )
    app.logger.info( "[ecg_service] - 'upload_file_content()' -> saved_file: " + str(saved_file) )
    
    app.logger.info("[ecg_service] - FIN 'upload_file_content()'")
    


# Descarga y guarda el fichero introducido por url
def upload_file_by_url(file_url, token_user):
    app.logger.info("[ecg_service] - INICIO 'upload_file_by_url()'")
    
    if utils.name_file_valid(file_url):
        url_file = file_url
        app.logger.info("[ecg_service] - 'upload_file_by_url()' -> el fichero URL a descargar es: " + str(url_file) )
        nombre_file, saved_file = utils.download_file_url(token_user, url_file)
        
        # ruta_fichero = cte.DIR_UPLOAD_FILES + token_user + "/" + nombre_file if (nombre_file is not None) else None    
    app.logger.info( "[ecg_service] - 'upload_file_by_url()' -> nombre_file: " + str(nombre_file) )
    app.logger.info( "[ecg_service] - 'upload_file_by_url()' -> saved_file: " + str(saved_file) )
    
    app.logger.info("[ecg_service] - FIN 'upload_file_by_url()'")
    


# Guarda los ficheros y devuelve una lista de los ficheros que no se han podido descargar
def upload_files(num_files, list_contents, list_nombres, token_user):
    nombre_file = None
    saved_file = None
    files_not_saved = []
    
    for i in range(num_files):
        if list_contents is not None:
            app.logger.info( "[ecg_service] - 'updload_file()' -> Guardo datos desde el contenedor" )
            content_file = list_contents[i]
            file_name = list_nombres[i]
            nombre_file, saved_file = utils.save_file_proces(token_user, file_name, content_file)
        else:
            app.logger.info( "[ecg_service] - 'updload_file()' -> Guardo datos descargando URLs" )
            url_data = list_nombres[i]
            nombre_file, saved_file = utils.download_file_url(token_user, url_data)
          
        if saved_file is not None and not saved_file:
            files_not_saved.append(nombre_file)
        
    return files_not_saved



# Devuelve un mensaje de error si alguno de los ficheros no se ha descargado de forma correcta
def check_save_files(list_files):
    
    app.logger.info( "[ecg_service] - 'check_save_files()' -> INICIO PASO 3. Comprobando ficheros no descargados" )
    
    if len(list_files) > 0:
        msg = ", ".join(list_files)
        msg = "Error! El/Los fichero/s [" + str(msg) + "] no se han podido descargar correctamente"
        
        app.logger.info( "[ecg_service] - 'check_save_files()' -> FIN PASO 3. FAIL - Devuelvo mensaje de error" )
        return msg
    
    app.logger.info( "[ecg_service] - 'check_save_files()' -> FIN PASO 3. SUCCESS" )
    return None



# guardar ficheros
def guardar_ficheros(list_contents, list_nombres, token_user):
    
    num_files = len(list_nombres)

    #Paso 0, 1 y 2
    msg_error = comprobar_ficheros(list_nombres)
    if msg_error is not None:
        return msg_error, False, None
    
    #Paso 3
    list_err_files = upload_files(num_files, list_contents, list_nombres, token_user)
    msg_error = check_save_files(list_err_files)
    if msg_error is not None:
        return msg_error, False, None
    
    #Paso 4, si todo ha ido bien, compruebo si el fichero es de un formato valido
    nom_raiz_fichero = utils.get_name_file(list_nombres[0], False)
    ruta_abs_file = utils.dir_files + token_user + "/" + nom_raiz_fichero
    fichero_valido, nombre_file, hay_anotaciones  = is_file_soported(ruta_abs_file)
    
    app.logger.info( "[ecg_service] - 'guardar_ficheros()' -> INICIO PASO 4. Comprobar si tiene un formato soportado" )
    app.logger.info( "[ecg_service] - 'guardar_ficheros()' -> fichero_valido: " + str(fichero_valido) )
    app.logger.info( "[ecg_service] - 'guardar_ficheros()' -> nombre_file: " + str(nombre_file) )
    app.logger.info( "[ecg_service] - 'guardar_ficheros()' -> hay_anotaciones: " + str(hay_anotaciones) )
    
    if fichero_valido :
        if not hay_anotaciones:
            app.logger.info( "[ecg_service] - 'guardar_ficheros()' -> no hay_anotaciones ")
            msg_error = "Warning: El fichero de anotaciones no existe, no se ha leído correctamente o no es válido"
            return msg_error, True, nombre_file
        
        return None, True, nombre_file
    
    msg_error = "Error! El fichero de datos no se ha podido leer correctamente."
    msg_error += " Compruebe los ficheros de datos y de cabecera introducidos y vuelva a intentarlo"
        
    return msg_error, False, None



# Comprueba si el fichero es de los formatos soportados o no
def is_file_soported(file_route):

    ecgFactory = ecgf.ECGFactory()
    filename_aux = utils.get_name_file(file_route, False)
    
    try:
        ecg_data = ecgFactory.create_ECG(file_route)
        filename = ecg_data.fileName
        print( "[ecg_service] - 'is_file_soported()' -> fileName: " + str(filename) )
        return True, filename, ecg_data.annt.ann_len is not None
    
    except ValueError:
        print( "[ecg_service] - 'is_file_soported()' -> Ha ocurrido un error al comprobar el fichero" + str(file_route) )
        return False, filename_aux, False
    
    except IOError:
        print( "[ecg_service] - 'is_file_soported()' -> Ha ocurrido un error de lectura al comprobar el fichero" + str(file_route) )    
        return False, filename_aux, False
    
    except:
        print( "[ecg_service] - 'is_file_soported()' -> Ha ocurrido un error interno al leer datos del fichero" + str(file_route) )
        return False, filename_aux, False
    