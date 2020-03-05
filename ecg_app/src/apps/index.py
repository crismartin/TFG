#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 18:55:25 2020

@author: cristian
"""

import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html


navbar = dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Link", href="/")),
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
            brand_href="/ecg",
            sticky="top",
        )


store_session = dcc.Store(id='session', storage_type='session')


layout_index = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content'),
    store_session
])

###############################################################################
############################## Main layout ####################################
###############################################################################
def layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        navbar,
        html.Div(id='page-content'),
        store_session
    ])