#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file the web router file that control the whole network

'''
import re
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
from config import *

app = Flask(__name__, static_folder='visible/dist', static_url_path='')
allow_origins = [
    "http://localhost:8080", "http://127.0.0.1:8080",
    "http://127.0.0.1:"+str(SimulationConfig.server_port), SimulationConfig.server_url]
socketio = SocketIO(app, cors_allowed_origins=allow_origins)
CORS(app, origins=allow_origins)

connect_magic_number = 64  # can be everything


@app.route('/')
def index():
    return app.send_static_file('index.html')


@socketio.on('connect_front', namespace='/ws')
def connect():
    '''
    Handle the connection event
    '''
    print("Connected")
    join_room(connect_magic_number)
    from simulation import network_entity
    update_topo(network_entity)


def update_topo(network):
    '''
    Update the topology of the network
    '''
    coordinates = []
    network_matrix = network.network_matrix

    for i in range(network_matrix.shape[0]):
        for j in range(network_matrix.shape[1]):
            if network_matrix[i, j] is not None:
                connected_users = network.get_connected_users(
                    network_matrix[i, j].id)
                coordinates.append(
                    {"user_id": network_matrix[i, j].id, "position": {
                        "x": i, "y": j}, "connected_users": connected_users.__str__()})

    print(coordinates)
    emit("update_topo", coordinates, namespace='/ws', to=connect_magic_number)


def update_delegate(delegate_id, is_delegate):
    '''
    Update the delegates of the network
    '''
    with app.app_context():
        emit("update_delegate", {"user_id": delegate_id, "is_delegate": is_delegate},
             namespace='/ws', to=connect_magic_number)


def spread_ledger(src, dest):
    '''
    Spread the ledger to the destination user
    '''
    # print("Spread ledger from {} to {}".format(src, dest))
    emit("spread_ledger", {"src": src, "dest": dest},
         namespace='/ws', to=connect_magic_number)


@app.route('/user_list')
def get_user_list():
    '''
    Get all user list in the network
    '''
    from simulation import network_entity
    users = network_entity.users
    return list(users.keys()).__str__()


@app.route('/spread_ledger')
def spread_ledger_route():
    '''
    Spread the ledger to the destination user
    '''
    src = request.args.get('src')
    dest = request.args.get('dest')
    spread_ledger(src, dest)
    return "OK"


@app.route('/update_delegate')
def update_delegate_route():
    '''
    Update the delegates of the network
    '''
    delegate_id = request.args.get('delegate_id')
    is_delegate = request.args.get('is_delegate')
    update_delegate(delegate_id, is_delegate)
    return "OK"


@app.route('/update_topo')
def update_topo_call():
    '''
    Update the topology of the network
    '''
    from simulation import network_entity
    update_topo(network_entity)
    return "OK"


@app.route('/get_running_time')
def get_running_time():
    '''
    Get the running time of the network
    '''
    from simulation import running_time
    return str(running_time)


@app.route('/update_chain_length')
def update_chain_length():
    '''
    Update the chain length of the network
    '''
    length = request.args.get('chain_length')
    emit("update_chain_length", length,
         namespace='/ws', to=connect_magic_number)
    return "OK"


@app.route('/update_transactions')
def update_transactions():
    '''
    Update the transactions of the network
    '''
    transactions = request.args.get('transactions')
    emit("update_transactions", transactions,
         namespace='/ws', to=connect_magic_number)
    return "OK"


@app.route('/get_transactions')
def get_transactions():
    '''
    Get the transactions of the network
    '''
    from simulation import transactions
    return str(transactions)


@app.route('/get_admitted_chains')
def get_admitted_chains():
    '''
    Get the admitted_chains of the network
    '''
    from simulation import admitted_chains
    return str(admitted_chains)
