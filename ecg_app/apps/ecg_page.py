#!/usr/bin/env python3
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
import apps.ecg_service as ecg_serv


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
                       

cnt_uploader = html.Div([dcc.Upload(id="upload-file",
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
                            id="alert-format",
                            color="light",
                            is_open=False
                        )
                    ])
            ])

uploader = html.Div(id="cnt-uploader", children=cnt_uploader)
                        
  

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
        
    dbc.FormGroup(children = uploader)
])


formulario = dbc.Form(id="form-uploader", children=[
    form_datos_ecg
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
        dbc.Input( id="st-valid-ant",  type="hidden"),
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
            size = "lg",
            backdrop = "static"
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

edit_point_input = dbc.Row(dbc.FormGroup([
        
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
)

load_intervals_inputs = dbc.Row(dbc.FormGroup([
    dbc.Row([
        html.H6("Intervalos señal"),  
    ]),
    
    dbc.FormGroup([
        html.Div(
            children=[
                 html.P(id="duracion-señal", children=["Duración total aprox: "])
            ]
        )
    ], row=True),
    
    dbc.Row([
        html.H6("Ver señal:"),  
    ]),
    dbc.FormGroup([
        dbc.Label("desde ", html_for="interv_ini", width=3),
        dbc.Col(
            dbc.InputGroup([
                dbc.InputGroupAddon("min", addon_type="prepend"),
                dbc.Input(
                    type="number", id="interv_ini", disabled=True, debounce=True
                ),
            ]),
            width=8,
        ),
        
    ], row=True),
    
    dbc.FormGroup([
        dbc.Label("hasta ", html_for="interv_fin", width=3),
        dbc.Col(
            dbc.InputGroup([
                dbc.InputGroupAddon("min", addon_type="prepend"),
                dbc.Input(
                    type="number", id="interv_fin", disabled=True, debounce=True
                ),
            ]),
            width=8,
        ),
    ], row=True),
    
    dbc.FormGroup([
        dbc.Col([
            dbc.Button(id="ver-intervalo", color="success", disabled=True,
               children=[
                   html.Span([html.I(className="fas fa-play ml-2"), " Cargar"])                   
                  ]
            ),
            dbc.Input(type="hidden", id="diff_interv")
        ]),
    ], className="float-center", row=True)
])
)

btn_next_interval = dbc.Button(id="btn-next-interval", outline=True, color="dark",
                       children=[
                           html.Span([html.I(className="fas fa-step-forward mr-1"), " Next"])
                          ],
                       n_clicks_timestamp='0'
                    )

btn_prev_interval = dbc.Button(id="btn-prev-interval", outline=True, color="dark",
                       children=[
                           html.Span([html.I(className="fas fa-step-backward mr-1"), " Prev"])
                          ],
                       n_clicks_timestamp='0'
                    )

move_controls = dbc.Row(id="move-controls", 
                         children=[
                                 dbc.Col(btn_prev_interval, width={"size": 2, "order": 1, "offset": 4}),
                                 dbc.Col(btn_next_interval, width={"size": 2, "order": "last"})
                         ])



title_controls =  dbc.FormGroup([
                    html.H2("Controles", id="controles-title", style={'text-align': 'left'})
                  ], row=True)

form_controls = html.Div(id="form-controls", children=[title_controls, dropdown_leads, load_intervals_inputs, edit_point_input])

cnt_form_controls = dbc.Form(id="cnt-form-controls", children=form_controls)

title_format = html.H1("Formato", id="formato-title", style={'textAlign': 'center'})


body = dbc.Container([
    html.Div(id="cnt-title-format", children=title_format),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                cnt_form_controls
            ]),
        ], width=3),
        dbc.Col([
            dbc.Row(
                display_ecg
            ),            
            move_controls
        ], width={"size": 9}, className="float-right")  
    ]),
    dbc.Row(
        menu_ecg, className="float-right"
    )
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
     Output("alert-format",     "is_open"),
     Output("alert-format",     "color")],
    [Input("st-valid-data",     "value")],
)
def activar_btn_process(result_upfile):
    app.logger.info("@callback: INICIO 'activar_btn_process()'")
    
    if result_upfile is None:
        app.logger.info( "@callback: FIN by None result 'activar_btn_process()'" )
        return True, False, "light"
    
    is_file_valid, has_annt = result_upfile.split(",")
    is_file_valid = utils.str_to_bool(is_file_valid)
    has_annt = utils.str_to_bool(has_annt)
    
    app.logger.info( "@callback: 'activar_btn_process()' -> is_file_valid: " + str(is_file_valid) )
    app.logger.info( "@callback: 'activar_btn_process()' -> has_annt: " + str(has_annt) )
    if is_file_valid and (has_annt is not None and not has_annt):
        return False, True, "warning"
    
    
    app.logger.info( "@callback: FIN 'activar_btn_process()'" )
    return not is_file_valid, not is_file_valid, "danger"
    


@app.callback(
    [Output("form-uploader",        "children"),
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
    
    return [form_datos_ecg, cnt_state_fdata, ecg_fig, cnt_form_controls, title_format]
    


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
        
        app.logger.info( "@callback: 'updload_file() -> msg_error: " + str(msg_error) )
        app.logger.info( "@callback: 'updload_file() -> fichero_valido: " + str(fichero_valido) )
        
        if fichero_valido:
            hay_annt = msg_error is None
            app.logger.info( "@callback: 'updload_file() -> hay_annt: " + str(hay_annt) )
            st_val_data = str(fichero_valido) + "," + str(hay_annt)
            return [nombre_file, True, True, True, True, st_val_data, msg_error]
        
        else:
            st_val_data = str(fichero_valido) + "," + str(None)
            return [None, False, False, False, True, st_val_data, msg_error]
    
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
    
    app.logger.info("@callback: 'process_file()' -> ruta_file: " + str(ruta_file))
    
    return ruta_file



@app.callback(
    [Output("optLeads","disabled"),
     Output("optLeads","options"),
     Output("optLeads","value"),
     Output("duracion-señal", "children"),
     Output("ver-intervalo", "disabled")],
    [Input("fname_process", "value")]
)
def select_first_lead(fname_uploaded):
    app.logger.info("@callback: INICIO 'select_first_lead()'")
    
    if fname_uploaded is not None:
        app.logger.info("@callback: 'select_first_lead()' -> Configurando parametros para pintar")
        ruta_file = utils.dir_files + fname_uploaded
        app.logger.info("@callback: 'select_first_lead()' -> ruta_file: " + str(ruta_file))
        app.logger.info("@callback: 'select_first_lead()' -> Obteniendo leads...")
        optLeads, duracion = ecg_serv.get_nleads_and_duration(ruta_file)
        app.logger.info("@callback: 'select_first_lead()' -> optLeads: " + str(optLeads))
        app.logger.info("@callback: FIN 'select_first_lead()'")
        text_duracion = "Duración total aprox: " + duracion
        return False, optLeads, 1, text_duracion, False
    
    app.logger.info("@callback: FIN 'select_first_lead()'")

    return True, None, None, None, True



@app.callback(
    [Output("ecg-fig", "figure"),
     Output("formato-title", "children"),     
     Output("point-y", "disabled"),
     Output("interv_ini", "disabled"),
     Output("interv_fin", "disabled")],
    [Input("optLeads", "value"),
     Input("ver-intervalo", "n_clicks")],
    [State("fname_process", "value"),
     State("interv_ini", "value"),
     State("interv_fin", "value")]
)
def print_ecg_lead(selected_lead, ver_intervalo, fname_uploaded, interv_ini, interv_fin):
    app.logger.info("\n@callback: INICIO 'print_ecg()'")
    
    app.logger.info("@callback: 'print_ecg()' -> selected_lead: " + str(selected_lead))
    app.logger.info("@callback: 'print_ecg()' -> fname_uploaded: " + str(fname_uploaded))
    
    if fname_uploaded is None or selected_lead is None:
        app.logger.info("@callback: FIN 'print_ecg()' by Exception")
        raise dash.exceptions.PreventUpdate()
        
    app.logger.info("@callback: 'print_ecg()' -> Configurando parametros para pintar")
    ruta_file = utils.dir_files + fname_uploaded
    app.logger.info("@callback: 'print_ecg()' -> ruta_file: " + str(ruta_file))
    app.logger.info("@callback: 'print_ecg()' -> Pintando datos...")
    
    fig, title = ecg_serv.build_plot_by_lead(ruta_file, selected_lead, interv_ini, interv_fin)
    app.logger.info("@callback: FIN 'print_ecg()'")
    return fig, title, False, False, False
    


@app.callback(
    Output('diff_interv', 'value'),
    [Input("interv_ini", "value"),
     Input("interv_fin", "value")]
)
def change_diff_interv(ini_value, fin_value):
    app.logger.info("@callback: INICIO 'change_diff_interv()'")
    
    if ini_value is None or fin_value is None:
        app.logger.info("@callback: FIN 'change_diff_interv()' by Exception: None value")
        raise dash.exceptions.PreventUpdate()
    
    if fin_value > ini_value:
        diff = fin_value - ini_value
    else:        
        diff = ""
    
    app.logger.info("@callback: 'change_diff_interv()': diff: " + str(diff))
    app.logger.info("@callback: FIN 'change_diff_interv()'")
    
    return diff



@app.callback(
    [Output("interv_ini", "value"),
     Output("interv_fin", "value"),
     Output("ver-intervalo", "n_clicks")],
    [Input("btn-next-interval", "n_clicks_timestamp"),
     Input("btn-prev-interval", "n_clicks_timestamp")],
    [State("diff_interv", "value"),
     State("interv_ini", "value"),
     State("interv_fin", "value"),
     State("ver-intervalo", "n_clicks")]
    
)
def next_interval_signal(next_btn, prev_btn, diff_interv, interv_ini, interv_fin, click_ver_interv):
    app.logger.info("@callback: INICIO 'next_interval_signal()'")
    
    next_btn = int(next_btn)
    prev_btn = int(prev_btn)
    
    if prev_btn > next_btn:
        diff_interv = (-1)*diff_interv
    
    new_interv_ini = interv_ini + diff_interv
    new_interv_fin = interv_fin + diff_interv
        
    app.logger.info("@callback: INICIO 'next_interval_signal()'")
    
    return [new_interv_ini, new_interv_fin, click_ver_interv+1]
    

###############################################################################
############################## Main layout ####################################
###############################################################################
def layout():
    return html.Div([body, footer])

