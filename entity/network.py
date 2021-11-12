#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file defines the network entity of the project.

'''
from .user import User
import numpy as np
import numpy.matlib as matlib


class Network:
    '''
    Network entity.
    '''

    def __init__(self, rows, cols, users: list):
        '''
        Initialize the network.

        Args:
            rows: number of rows in the network.
            cols: number of columns in the network.
            users: user list in the network.
        '''
        self.users = users

        # Initialize the network.
        self.network_matrix = matlib.empty((rows, cols), dtype=User)
        # Initialize the connect matrix.
        # TODO: initalized as all True for testing. Should be all False.
        self.connect_matrix = matlib.ones(
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
        connected_users_id_list = []
        for user in self.users:
            if user.id != user_id:
                connected_users_id_list.append(user.id)

        return connected_users_id_list

    def is_connected(self, sender, receiver):
        '''
        Check if two users are connected.
        '''
        # TODO: To be implemented. Currently, return True.
        return True

    def get_user_by_id(self, user_id):
        '''
        Get user by id.
        '''
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def send_ledger(self, sender_id, receiver_id, ledger):
        '''
        Send a ledger to the receiver.
        '''
        # get user by id.
        sender = self.get_user_by_id(sender_id)
        receiver = self.get_user_by_id(receiver_id)
        if sender is None or receiver is None:
            return False

        # check if the sender and receiver are connected.
        if not self.is_connected(sender.id, receiver.id):
            return False

        # send the ledger.
        return receiver.receive_ledger(ledger)
