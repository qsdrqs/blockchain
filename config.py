#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file is the configs file for the project.

'''

from random import randint
from math import log, ceil


class Config:
    # Public config
    network_row = 20
    network_col = 20
    users = 100


class TimeConfig(Config):
    # Time config
    walk_time = 10
    delegates_select_time = 60
    delegates_sign_time = 20

    @staticmethod
    def transaction_time():
        return randint(10, 10)


class SimulationConfig(Config):
    # Simulation config
    delegate_count = ceil(log(Config.users))
    visual_mode = True
    server_port = 5000
    server_url = 'http://localhost:' + str(server_port)
    radius_max = 3
    radius_min = 3
    walk_min_num = 5
    walk_max_num = 15
