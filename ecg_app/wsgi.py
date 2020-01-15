#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 23:49:46 2019

@author: cristian
"""

from index import app

application=app.server


if __name__=='__main__':
   application.run(host='0.0.0.0', port=8050, debug=True)
