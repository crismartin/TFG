#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 13:29:20 2019

@author: cristian
"""

import utils_ecg as utils
import constantes_ecg as cte
import numpy as np
import ecg_reader.ecg_factory as ecgf

import WTdelineator.WTdelineator as wav

from database import db

import plotly.graph_objs as go

from app import app



def build_select_leads(nleads):
    return [ {'value': i+1, 'label': 'Derivacion '+ str(i+1)} for i in range(nleads)]
    


def get_nleads_and_duration(file_name):
    duration_in_min = 0
    # Factoria de ECG
    ecgFactory = ecgf.ECGFactory()    
    ecg = ecgFactory.create_ECG(file_name)

    if ecg.header.signal_len > 0:
        tamanio = ecg.header.signal_len // ecg.header.samplingRate
        app.logger.info("[ecg_service] - 'get_nleads_array()' ->  tamanio: " + str(tamanio) )
        msg_duration = utils.convert_seg_to_hhmm(tamanio)
        app.logger.info("[ecg_service] - 'get_nleads_array()' ->  msg_duration: " + str(msg_duration) )
        duration_in_min = utils.sec_to_min(tamanio)
       
    app.logger.info("[ecg_service] - 'get_nleads_array()' ->  duration: " + str(duration_in_min) )
    
    nLeads = ecg.header.nLeads    
    
    return build_select_leads(nLeads), msg_duration, duration_in_min
    


def build_data_annt(ecg, signal_y, sampFrom, sampTo):
    ecg.read_annotations(sampFrom, sampTo)
    ant_trace = None
    anotaciones = ecg.annt
    
    app.logger.info("[ecg_service] - 'build_data_annt()' ->  signal_y: " + str(len(signal_y)) )
        
    anotaciones.printInfo()
    
    if anotaciones is not None and anotaciones.ann_len is not None and anotaciones.ann_len > 0:
        fs = ecg.header.samplingRate
        ant_ejeX = anotaciones.sample
        ant_ejeX = ant_ejeX / float(fs)
        ant_ejeX = np.around(ant_ejeX, decimals=6)
        ant_ejeX = ant_ejeX.tolist()        
        app.logger.info("[ecg_service] - 'build_data_annt()' ->  ant_ejeX: " + str(ant_ejeX) )    
        
        if sampFrom > 0:
            zeros_array = np.zeros(sampFrom)
            signal_y = np.concatenate((zeros_array, signal_y))
            app.logger.info("[ecg_service] - 'build_data_annt()' ->  signal_y: " + str(signal_y))
            
        ant_ejeY = signal_y[anotaciones.sample]
        app.logger.info("[ecg_service] - 'build_data_annt()' ->  ant_ejeY: " + str(ant_ejeY) )
        simbols = anotaciones.symbol
        ant_trace = go.Scatter(x = ant_ejeX, y = ant_ejeY,
                        name = 'Anotaciones', mode='markers+text', 
                        text=simbols, textposition="top right")
    
    app.logger.info("[ecg_service] - END 'build_data_annt()'")
    return ant_trace
    


def get_delineator_graph(signal, fs, sampFrom):
    ondas = []
    #Delineador de la señal
    app.logger.info("[ecg_service] - 'get_delineator_graph()' -> calculando signalDelination")
    Pwav, QRS, Twav = wav.signalDelineation(signal,fs)
    app.logger.info("[ecg_service] - 'get_delineator_graph()' -> fin signalDelination")
    #app.logger.info("[ecg_service] - 'get_qrs_waves()' ->  Q: " + str(len(QRS[:,1])) )
    #app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  R: " + str(QRS[:,2]) )
    #app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  S: " + str(QRS[:,3]) )
    
    ondaQ = get_qrs_wave(QRS, signal, fs, sampFrom, 1)
    if ondaQ is not None:
        ondas.append(ondaQ)
    
      
    ondaR = get_qrs_wave(QRS, signal, fs, sampFrom, 2)
    if ondaR is not None: 
        ondas.append(ondaR)
    
    ondaS = get_qrs_wave(QRS, signal, fs, sampFrom, 3)
    if ondaS is not None:
        ondas.append(ondaS)
    
    if Pwav != []:
        pWaves = get_p_wave(Pwav, signal, sampFrom, fs)
        for p_wave in pWaves:
            ondas.append(p_wave) 
    
    return ondas



def get_simbol_P(num_sample):
    simbol = None
    text_pos = None
    name = None
    
    if num_sample == 0:
        simbol = 'P('
        text_pos = 'top left'
        name = "P Start"
    elif num_sample == 1:
        simbol = 'P1'
        text_pos = 'top center'
        name = "Peak 1"
    elif num_sample == 2:
        simbol = 'P2'
        text_pos = 'top center'
        name = "Peak 2"
    elif num_sample == 3:
        simbol = ')P'
        text_pos = 'top right'
        name = "P End"
        
    return simbol, text_pos, name



def get_p_wave(pWav, signal, sampFrom, fs):
    traces = []
    
    #app.logger.info("[ecg_service] - 'get_p_wave()' ->  PWave: " + str(pWav) )
    n_wave = [i for i in (range(4))]
    
    for i in n_wave:
        p_i = pWav[:,i]
        if p_i != []:        
            ejeY = signal[p_i]
            if sampFrom > 0:                
                p_i = [sample + sampFrom for sample in p_i]
                p_i = np.asarray(p_i)
            
            ejeX = p_i/float(fs)
            ejeX = np.around(ejeX, decimals=6)
            ejeX = ejeX.tolist()
            #app.logger.info("[ecg_service] - 'get_p_wave()' ->  p_i: " + str(p_i) )
            
            simbolo_onda, text_position, name_wave = get_simbol_P(i)
            simbols = [simbolo_onda for i in range(len(ejeX))]
            
            p_trace = go.Scatter(x = ejeX, y = ejeY,
                                 name = name_wave, mode='markers+text',
                                 text=simbols, textposition=text_position,
                                 visible='legendonly')
            traces.append(p_trace)
    
    return traces
    


def get_qrs_wave(qrs, signal, fs, sampFrom, wave):
    
    app.logger.info("[ecg_service] - 'get_qrs_wave()' ->  signal: " + str(signal) )
    
    simbolo_onda = ''
    text_position = 'top left'
    if wave == 1:
        simbolo_onda = 'Q'
        text_position = 'bottom left'
    elif wave == 2:
        simbolo_onda = 'R'
    elif wave == 3:
        simbolo_onda = 'S'
        text_position = 'bottom right'
    
    if simbolo_onda != '':
        qWave = qrs[:,wave]
        if qWave != []:                        
            app.logger.info("[ecg_service] - 'get_qrs_waves()' ->  qwave: " + str(qWave) )
            ejeY = signal[qWave]
            if sampFrom > 0:                
                qWave = [sample + sampFrom for sample in qWave]
                qWave = np.asarray(qWave)
            
            app.logger.info("[ecg_service] - 'get_qrs_waves()' ->  qwave final: " + str(qWave) )
            ejeX = qWave/float(fs)
            ejeX = np.around(ejeX, decimals=6)
            ejeX = ejeX.tolist()
            
            app.logger.info("[ecg_service] - 'get_qrs_waves()' ->  ejeX: " + str(ejeX) )
            
            simbols = [simbolo_onda for i in range(len(ejeX))]
    
            name_wave = 'Onda ' + str(simbolo_onda)
            q_trace = go.Scatter(x = ejeX, y = ejeY,
                                name = name_wave, mode='markers+text',
                                text=simbols, textposition=text_position,
                                visible='legendonly')
            return q_trace
    
    return None
    


def build_ecg_trace(ejeX, ejeY, nLead, range_min):
    
    layout = go.Layout(title = "Representacion de la Derivación " + str(nLead),
                    hovermode = 'closest', uirevision=True, autosize=True, 
                    xaxis=go.layout.XAxis(
                                rangeselector=dict(
                                    
                                ),
                                rangeslider=dict(
                                    visible=True
                                ),
                                range=[range_min, range_min+12]
                            ),
                    yaxis=dict(gridcolor="LightPink"),
                    plot_bgcolor='rgb(248,248,248)'
                    )
        
    ecg_trace = go.Scatter(x = ejeX, y = ejeY,
                    name = 'ECG', mode='lines')
    return layout, ecg_trace
    


# Comprueba si el intervalo introducido es correcto o no
def is_interv_valid(interv_ini, interv_fin):
    if (interv_ini is not None and interv_fin is not None):
        num_ini = int(interv_ini)
        num_fin = int(interv_fin)
        
        if num_fin > num_ini:
            return num_ini, num_fin
        
    return None, None


def get_interval_samples(interv_ini, interv_fin, signal_len, fs):

    num_ini, num_fin = is_interv_valid(interv_ini, interv_fin)
    
    if num_ini is not None and num_fin is not None:
        sampFrom = utils.min_to_sec(num_ini) * fs
        sampTo = utils.min_to_sec(num_fin) * fs
        
        if sampFrom < signal_len and sampTo > sampFrom and sampTo <= signal_len:
            return int(sampFrom), int(sampTo)
    
    sampFrom = int(60*fs)
    return 0, sampFrom if sampFrom <= signal_len else signal_len
        
    

# Contruye la grafica para el lead correspondiente
def build_plot_by_lead(file_name, lead, interv_ini, interv_fin):
    app.logger.info("\n[ecg_service] - INICIO 'build_plot_by_lead()'")
    data_fig = []
    ecgFactory = ecgf.ECGFactory()    
    ecg = ecgFactory.create_ECG(file_name)
    
    signal_len = ecg.header.signal_len
    nLeads = ecg.header.nLeads
    fs = ecg.header.samplingRate
    
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  signal_len: " + str(signal_len) )
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  fs: " + str(fs) )
    
    sampFrom, sampTo = get_interval_samples(interv_ini, interv_fin, signal_len, fs)    
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  sampFrom: " + str(sampFrom) )
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  sampTo: " + str(sampTo) )
    
    ecg.read_signal(sampFrom, sampTo)
    
    signals = ecg.signal
    
    title = ecg.fileName + " | Formato " + ecg.typeECG
    
    
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  nLeads: " + str(nLeads) )
    if lead > nLeads:
        app.logger.info("[ecg_service] - 'build_plot_by_lead()' -> return None, no hay leads: " + str(nLeads) )
        return None    
    
    #Datos de la señal (Y(x))
    ejeY = signals[lead-1]
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  ejeY: " + str(ejeY) )
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  len(ejeY): " + str(len(ejeY)) )
    
    ejeX = np.arange(sampFrom, sampTo, 1.0)/fs
    
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' ->  ejeX: " + str(ejeX) )
 
    optsLeads = build_select_leads(nLeads)
    lead_value = optsLeads[lead-1]['value']
        
    range_min = 0 if interv_ini is None else utils.min_to_sec(interv_ini)
    
    #Devuelve el gráfico principal (el ECG)
    layout, ecg_trace = build_ecg_trace(ejeX, ejeY, lead_value, range_min)    
    data_fig.append(ecg_trace)
    
    # Datos de las anotaciones    
    ant_trace = build_data_annt(ecg, ejeY, sampFrom, sampTo)
    
    if ant_trace is not None:
        data_fig.append(ant_trace)
        
    #Datos de QRS    
        
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' -> sampFrom: " + str(sampFrom))    
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' -> fs: " + str(fs))
    
    qrs_wave = get_delineator_graph(ejeY, fs, sampFrom)
    if qrs_wave != []:   
        for wave in qrs_wave:
            data_fig.append(wave) 
            
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' -> Fin datos QRS. Creando objeto grafica")
    
    #Objeto grafica
    fig = go.Figure(data = data_fig, layout = layout)
    
    app.logger.info("[ecg_service] - 'build_plot_by_lead()' -> Fin creacion objeto grafica. Devolviendo grafico")
    
    return fig, title


# Borrar un fichero en el sistema y en BBDD
def delete_file_system(token_session, name_file):
    app.logger.info( "[ecg_service] - 'delete_file_system()' -> name_file: " + str(name_file))
    ruta_fichero = token_session + "/" + name_file
    utils.borrar_fichero(ruta_fichero)
    delete_file_session(name_file, token_session)
    


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
def guardar_ficheros(list_contents, list_nombres, token_session):
    
    num_files = len(list_nombres)

    #Paso 0, 1 y 2
    msg_error = comprobar_ficheros(list_nombres)
    if msg_error is not None:
        return msg_error, False, None
    
    #Paso 2.9 Compruebo si el nombre raiz del fichero no existe en BBDD para esta sesion
    nom_raiz_fichero = utils.get_name_file(list_nombres[0], False)
    es_fichero_repetido = exist_file_user_by_name(nom_raiz_fichero, token_session)
    if es_fichero_repetido is not None and es_fichero_repetido == True:
        msg_error = "Error: El fichero ya existe. Utilice el historial de ficheros para cargarlo, "
        msg_error += "cambie el nombre del archivo a subir o borre los ficheros antiguos y suba los nuevos"
        return msg_error, False, nom_raiz_fichero
    
    elif es_fichero_repetido is None:
        msg_error = "Warning: Se ha encontrado un error de sesion. Vuelva a cargar la página"
        return msg_error, False, None
    
    #Paso 3
    list_err_files = upload_files(num_files, list_contents, list_nombres, token_session)
    msg_error = check_save_files(list_err_files)
    if msg_error is not None:
        return msg_error, False, nom_raiz_fichero
    
    #Paso 4, si todo ha ido bien, compruebo si el fichero es de un formato valido    
    ruta_abs_file = utils.dir_files + token_session + "/" + nom_raiz_fichero
    fichero_valido, nombre_file, hay_anotaciones, formato  = is_file_soported(ruta_abs_file)
    
    app.logger.info( "[ecg_service] - 'guardar_ficheros()' -> INICIO PASO 4. Comprobar si tiene un formato soportado" )
    app.logger.info( "[ecg_service] - 'guardar_ficheros()' -> fichero_valido: " + str(fichero_valido) )
    app.logger.info( "[ecg_service] - 'guardar_ficheros()' -> nombre_file: " + str(nombre_file) )
    app.logger.info( "[ecg_service] - 'guardar_ficheros()' -> hay_anotaciones: " + str(hay_anotaciones) )
    
    if fichero_valido :
        # creo un registro del fichero en la BBDD
        insert_file_session(nombre_file, formato, token_session)
        
        if not hay_anotaciones:
            app.logger.info( "[ecg_service] - 'guardar_ficheros()' -> no hay_anotaciones ")
            msg_error = "Warning: El fichero de anotaciones no existe, no se ha leído correctamente o no es válido"
            return msg_error, True, nombre_file

        return None, True, nombre_file
    
    msg_error = "Error! El fichero de datos no se ha podido leer correctamente."
    msg_error += " Compruebe los ficheros de datos y de cabecera introducidos y vuelva a intentarlo"
        
    return msg_error, False, nom_raiz_fichero



# Comprueba si el fichero es de los formatos soportados o no
def is_file_soported(file_route):
    formato = ""
    ecgFactory = ecgf.ECGFactory()
    filename_aux = utils.get_name_file(file_route, False)
    
    try:
        ecg_data = ecgFactory.create_ECG(file_route)
        header = ecg_data.header
        if header is None or header == []:
            print( "[ecg_service] - 'is_file_soported()' -> Cabecera vacía para el fichero " + str(file_route) )    
            return False, filename_aux, False, formato
        
        sig_len = ecg_data.header.signal_len
        if sig_len is None or sig_len <= 0:
            print( "[ecg_service] - 'is_file_soported()' -> No hay datos de señal ECG para fichero " + str(file_route) )    
            return False, filename_aux, False, formato
        
        app.logger.info( "[ecg_service] - 'is_file_soported()' -> sig_len: " + str(sig_len))
        filename = ecg_data.fileName
        formato = ecg_data.typeECG
        ecg_data.read_annotations(0, sig_len)
        annt = ecg_data.annt        
        app.logger.info( "[ecg_service] - 'guardar_ficheros()' -> annt: " + str(annt))
        print( "[ecg_service] - 'is_file_soported()' -> fileName: " + str(filename) )
        return True, filename, annt is not None and annt.ann_len > 0, formato
    
    except ValueError:
        print( "[ecg_service] - 'is_file_soported()' -> Ha ocurrido un error al comprobar el fichero " + str(file_route) )
        return False, filename_aux, False, formato
    
    except IOError:
        print( "[ecg_service] - 'is_file_soported()' -> Ha ocurrido un error de lectura al comprobar el fichero " + str(file_route) )    
        return False, filename_aux, False, formato
    
    except:
        print( "[ecg_service] - 'is_file_soported()' -> Ha ocurrido un error interno al leer datos del fichero " + str(file_route) )
        return False, filename_aux, False, formato
    
    



def set_token_session(data_session):
    return db.set_token_session(data_session)  


# Devuelve la lista de ficheros asociados a una sesion de usuario
def get_list_files_user(token_session):    
    try:
        return db.get_list_files_user(token_session)
    except RuntimeError:
        app.logger.info("[ecg_service] - 'insert_file_session()' -> Token de session incorrecto" )
    
    return None        


# Devuelve el fichero de nombre "filename" asociado a una sesion de usuario 
def get_file_user_by_name(filename, token_session):
    try:
        return db.get_file_user_by_name(filename, token_session)
    except RuntimeError:
        app.logger.info("[ecg_service] - 'insert_file_session()' -> Token de session incorrecto" )
    
    return None


# Compruebo si existe o no el fichero de nombre "filename" asociado una sesion de usuario
def exist_file_user_by_name(filename, token_session):
    try:
        app.logger.info("[ecg_service] - 'exist_file_user_by_name()' -> filename: " + str(filename) )
        fichero = db.get_file_user_by_name(filename, token_session)
        return fichero is not None
    except RuntimeError:
        app.logger.info("[ecg_service] - 'insert_file_session()' -> Token de session incorrecto" )
    
    return None


# Inserto el fichero en la BBDD, siempre que el fichero no tenga un nombre repetido
def insert_file_session(nombre_file, formato, token_session):
    try:
        app.logger.info("[ecg_service] - 'insert_file_session()' -> filename: " + str(nombre_file) )
        app.logger.info("[ecg_service] - 'insert_file_session()' -> formato: " + str(formato) )
        id_file = db.insert_file_session(nombre_file, formato, token_session)
        return id_file
    except RuntimeError:
        app.logger.info("[ecg_service] - 'insert_file_session()' -> Token de session incorrecto")
    
    return None


# Elimina el fichero de nombre "nombre_file" asociado a una sesion de usuario
def delete_file_session(nombre_file, token_session):
    try:
        app.logger.info("[ecg_service] - 'delete_file_session()' -> filename: " + str(nombre_file) )
        borrado = db.delete_file_session(nombre_file, token_session)
        if borrado is True:
            msg = "El fichero con nombre '"+ str(nombre_file) + "' no se ha borrado correctamente en BBDD"
            app.logger.info( "[ecg_service] - 'delete_file_system()' -> " + str(msg))
        
    except RuntimeError:
        app.logger.info("[ecg_service] - 'delete_file_session()' -> Token de session incorrecto")
    
    