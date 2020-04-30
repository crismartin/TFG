#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:49:46 2019

@author: cristian
"""

from router import app
import os
from flask import send_from_directory

server = app.server


@server.route('/src/static/<path:path>')
def static_file(path):
    print("Path es: " + path)
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)


@server.route('/src/assets/<path:path>')
def assets_file(path):
    print("Path es: " + path)
    static_folder = os.path.join(os.getcwd(), 'assets')
    return send_from_directory(static_folder, path)


if __name__=='__main__':
   server.run(host='0.0.0.0', port=8050, debug=True)
