#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 18:55:25 2020

@author: cristian
"""

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import src.apps.auth_module.auth_page as auth_page

navlink_home = dbc.NavItem(dbc.NavLink(children=html.Span([html.I(className="fa fa-home"), " Home"]), 
                                        href="/"))


navbar = dbc.NavbarSimple(
            id="nav-auth",
            children = auth_page.nologged_component(),
            brand="ECG App",
            brand_href="/",
            sticky="top",
        )


store_session   = dcc.Store(id='session', storage_type='session')



class Inicio:
    
    cards = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("Dash", className="card-title"),
                    html.P(
                        "This card has some text content, which is a little "
                        "bit longer than the second card.",
                        className="card-text",
                    ),
                    dbc.Nav(
                        dbc.NavLink(dbc.Button(children=[
                                           html.Span([html.I(className="fa fa-link ml-2"), " Dash"])
                                           ], color="primary"
                                    ), href="https://dash.plotly.com/"
                        ), className="float-right"
                    )
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("MongoDB", className="card-title"),
                    html.P(
                        "This card has some text content, which is longer "
                        "than both of the other two cards, in order to "
                        "demonstrate the equal height property of cards in a "
                        "card group.",
                        className="card-text",
                    ),
                    dbc.Nav(
                        dbc.NavLink(dbc.Button(children=[
                                           html.Span([html.I(className="fa fa-database ml-2"), " PyMongo"])
                                           ], color="primary"
                                    ), href="https://pymongo.readthedocs.io/"
                        ), className="float-right"
                    )
                ]
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H5("WDelineator", className="card-title"),
                    html.P(
                        "This card has some text content.",
                        className="card-text",
                    ),
                    dbc.Nav(
                        dbc.NavLink(dbc.Button(children=[
                                           html.Span([html.I(className="fa fa-code-fork ml-2"), " WDelineator"])
                                           ], color="primary"
                                    ), href="https://github.com/caledezma/WTdelineator"
                        ), className="float-right"
                    )
                ]
            )
        ),
    ])
    
    card_img = dbc.Card([
        dbc.CardImg(src="/src/assets/img_principal.png", top=True),
    ])
    
    
    parte_img = dbc.Col([
        card_img
    ]),
    
    body = dbc.Jumbotron([
        html.H1("ECG App"),
        dbc.Row([
            dbc.Col([
                html.P(
                    "Use a jumbotron to call attention to "
                    "Use a jumbotron to call attention to "
                    "Use a jumbotron to call attention to "
                    "Use a jumbotron to call attention to "
                    "Use a jumbotron to call attention to "
                    "Use a jumbotron to call attention to "
                    "Use a jumbotron to call attention to "
                    "Use a jumbotron to call attention to "
                    "Use a jumbotron to call attention to "
                    "Use a jumbotron to call attention to "
                    "Use a jumbotron to call attention to "
                    "featured content or information.",
                    className="lead",
                ),
                html.P(
                    "Formatos soportados: Physionet, Ishne"
                ),
                html.Br(),
                html.Hr(className="my-2"),                
                dbc.Row([
                    dbc.Col([    
                        dbc.Nav(
                            dbc.NavLink(dbc.Button(children=[
                                               html.Span([html.I(className="fa fa-code-fork ml-2"), " Ver en GitHub"])
                                               ], color="primary"
                                        ), href="https://github.com/crismartin/TFG"
                            ), className="float-right"
                        )
                    ])
                ])
            ]),
            dbc.Col([
                dbc.Card([
                    dbc.CardImg(src="/src/static/img_principal.png", top=True),
                ])
            ]),
        ])
    ])
    
    footer = html.Footer([
        dbc.Nav([
            dbc.NavLink("© Universidad Rey Juan Carlos 2019-2020 "),
            dbc.NavLink(" | "),
            dbc.NavLink("Escuela Técnica Superior de Ingeniería en Telecomunicación", href="https://www.urjc.es/etsit"),
            dbc.NavLink(" | "),
            dbc.NavLink("Protección de datos", href="https://www.urjc.es/proteccion-de-datos"),
        ]),
    ])
    
    body = dbc.Container(children=[
        html.Br(),
        body,
        html.H4("Tecnologías utilizadas"),
        cards,
        html.Br(),
        html.Br(),
        html.Br(),
        footer,
        html.Br()
    ])
    
    

    @staticmethod
    def layout():
        return html.Div([
            Inicio.body            
        ])


###############################################################################
############################## Main layout ####################################
###############################################################################
def layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        navbar,        
        html.Div(id="page-content"),
        auth_page.layout(),
        store_session
    ])