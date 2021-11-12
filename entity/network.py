#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file defines the network entity of the project.

'''
from entity import *
import numpy as np
import numpy.matlib as matlib


class Network:
    '''
    Network entity.
    '''

    def __init__(self, rows, cols, users):
        '''
        Initialize the network.

        Args:
            rows: number of rows in the network.
            cols: number of columns in the network.
            users: user id list in the network.
        '''
        self.users = users

        # Initialize the network.
        self.network_matrix = matlib.empty((rows, cols), dtype=User)
        self.connect_matrix = matlib.empty(
            (len(users), len(users)), dtype=bool)

        # TODO: randomly set users in the network.

        # build the connect matrix.
        self.refresh_network()

    def refresh_network(self):
        '''
        Refresh the whold network.
        Rebuild the connect matrix and network matrix.
        '''
        pass

    def get_connected_users(self, user_id):
        '''
        Get the connected users of specified user.
        '''
        # TODO: To be implemented. Currently, return all other users.
        connected_users = self.users.copy()
        connected_users.remove(user_id)
        return connected_users
