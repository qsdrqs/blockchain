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


def run():
    '''
    Run the simulation
    '''
    # Initialize the entities
    user_list = []
    for i in range(1, SimulationConfig.users+1):
        user_list.append(User(i, [], 1000, randint(
            SimulationConfig.radius_min, SimulationConfig.radius_max)))

    # Initialize the ledger
    ledger = Ledger([user.generate_digest() for user in user_list], [])
    for user in user_list:
        user.ledgers.append(ledger.deepcopy())

    print("finish init the users")
    global network_entity
    network_entity = Network(Config.network_row, Config.network_col, user_list)

    print("finish init the whole simulation")
    #run_timer(TimeConfig.transaction_time(), user_transaction)
    run_timer(10, user_transaction)

    socketio.run(app, port=SimulationConfig.server_port, log_output=True)


def user_transaction():
    '''
    Generate a transaction from any user to any user
    '''
    # Get the user
    user_from = network_entity.users[randint(
        1, network_entity.user_count)]
    user_to = network_entity.users[randint(
        1, network_entity.user_count)]
    if user_from.balance > 1:
        if user_from.add_transaction(user_to.id, randint(1, ceil(user_from.balance/4))):
            user_from.spread_ledgers(network_entity)

    run_timer(5, user_transaction)
