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