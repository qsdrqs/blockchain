#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file the web router file that control the whole network

'''
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'
