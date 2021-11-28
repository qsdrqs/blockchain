#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file is the configs file for the project.

'''


class Config:
    # Public config
    network_row = 1000
    network_col = 1000
    users = 100


class TimeConfig(Config):
    # Time config
    pass


class SimulationConfig(Config):
    # Simulation config
    delegate_percentage = 20
