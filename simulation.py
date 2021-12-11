#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file the simulation file

'''
from router import *
from config import *
from entity import *
from random import randint
from util import *
from util.multithreading import run_timer
from math import ceil
import requests
import sys


def run():
    '''
    Run the simulation
    '''
    # Initialize the python environment
    sys.setrecursionlimit(10000)
    # Initialize the entities
    print("Initializing the entities...")
    user_list = []
    for i in range(1, SimulationConfig.users+1):
        user_list.append(User(i, [], 1000, randint(
            SimulationConfig.radius_min, SimulationConfig.radius_max)))

    # Initialize the ledger
    ledger = Ledger([user.generate_digest() for user in user_list], [])
    for user in user_list:
        user.ledgers.append(ledger.deepcopy())

    print("finish init the users")
    global network_entity, running_time, transactions, admitted_chains
    network_entity = Network(Config.network_row, Config.network_col, user_list)
    running_time = 0
    transactions = 0
    admitted_chains = 0

    print("finish init the whole simulation")
    run_timer(5, user_transaction)
    run_timer(10, select_delegates)
    run_timer(11, delegates_sign)
    run_timer(10, random_walk)

    run_timer(1, add_running_time)
    print(f"Server now running on {SimulationConfig.server_url}")
    socketio.run(app, port=SimulationConfig.server_port, log_output=False)


def user_transaction():
    '''
    Generate a transaction from any user to any user
    '''
    # Get the user
    from_id = randint(1, network_entity.user_count)
    to_id = randint(1, network_entity.user_count)
    while from_id == to_id:
        to_id = randint(1, network_entity.user_count)
    user_from = network_entity.users[from_id]
    user_to = network_entity.users[to_id]
    if user_from.balance > 1:
        if user_from.add_transaction(user_to.id, randint(1, 1)):
            global transactions
            transactions += 1
            requests.get(SimulationConfig.server_url+'/update_transactions',
                         params={'transactions': transactions})
            user_from.spread_ledgers(network_entity)

    run_timer(TimeConfig.transaction_time(), user_transaction)


def random_walk():
    '''
    Make users walk randomly
    '''
    network_entity.random_walk()
    run_timer(TimeConfig.walk_time, random_walk)


def select_delegates():
    '''
    Select the delegates
    '''
    for user in network_entity.users.values():
        user.choose_delegate()
    run_timer(TimeConfig.delegates_select_time, select_delegates)


def delegates_sign():
    '''
    Make all delegates to sign the ledger
    '''
    delegates = []
    for user in network_entity.users.values():
        result = user.sign_delegate()
        if result is not None:
            delegates.append(user)

    # Update the ledger
    for user in delegates:
        user.spread_ledgers(network_entity)

    run_timer(TimeConfig.delegates_sign_time, delegates_sign)


def add_running_time():
    '''
    Add running time
    '''
    global running_time
    running_time += 1
    run_timer(1, add_running_time)
