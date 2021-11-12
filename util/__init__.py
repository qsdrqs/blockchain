#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This module is used to provide some utilities of project.

'''
import struct
from .encrypt import *


def float_to_bytes(f_value: float):
    '''
    Convert float to bytes.
    '''
    return struct.pack('>f', f_value)
