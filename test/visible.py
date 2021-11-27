#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file test file of the visible layer.
These tests not use the unittest framework.

'''
from router import *


def run():
    '''
    Run the tests.
    '''
    network_entity = Network(
        4, 4, [User(1, [], 1), User(2, [], 1), User(3, [], 1)])
    network = network_entity
    network_matrix = network.network_matrix
    network_matrix[1, 1] = network.users[1]
    network_matrix[2, 2] = network.users[2]
    network_matrix[1, 3] = network.users[3]
    socketio.run(app, port=5000, debug=False)

###############################################################################
# Tests


@app.route('/test_ledger')
def test_ledger():
    '''
    Test the ledger
    '''
    src = request.args.get('src')
    dest = request.args.get('dest')
    spread_ledger(src, dest)
    return "OK"


@app.route('/test_update')
def test_update():
    '''
    Test the update
    '''
    network = network_entity
    network_matrix = network.network_matrix
    network_matrix[2, 1] = network.users[1]
    network_matrix[1, 2] = network.users[2]
    network_matrix[3, 3] = network.users[3]
    update_topo(network)
    return "OK"
