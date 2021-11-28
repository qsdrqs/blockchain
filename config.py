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


class Config:
    # Public config
    network_row = 30
    network_col = 30
    users = 100


class TimeConfig(Config):
    # Time config
    @staticmethod
    def transaction_time():
        return randint(1, 2)


class SimulationConfig(Config):
    # Simulation config
    delegate_percentage = 20
    visual_mode = True
    server_port = 5000
    server_url = 'http://localhost:' + str(server_port)
    radius_max = 5
    radius_min = 5
