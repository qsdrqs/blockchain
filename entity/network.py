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
import numpy.random as npr
import numpy.matlib as matlib
from util.multithreading import ThreadPool


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
        self.users = {}
        for user in users:
            self.users[user.id] = user

        # Initialize the network.
        self.network_matrix = matlib.empty((rows, cols), dtype=User)
        # self.network_matrix[1,2] = self.users[1]
        # Initialize the connect matrix.
        # TODO: initalized as all True for testing. Should be all False.
        self.connect_matrix = matlib.ones(
            (len(users), len(users)), dtype=bool)

        # Initialize the thread pool.
        self.thread_pool = ThreadPool(users)

        # TODO: randomly set users in the network.

        # build the connect matrix.
        self.refresh_network()

    def refresh_network(self):
        '''
        Refresh the whold network.
        Rebuild the connect matrix and network matrix.
        Step 1: randomly set users position in the network.
        Step 2: build the connect matrix.
        '''

        def is_connected_graph(self):
            '''
            Check if the network is connected.
            '''
            return True

        pass  # TODO
        if not is_connected_graph(self):
            self.refresh_network()

    def get_connected_users(self, user_id):
        '''
        Get the connected users of specified user.
        '''
        # TODO: To be implemented. Currently, return all other users.
        connected_users_id_list = []
        for my_user_id in self.users:
            if my_user_id != user_id:
                connected_users_id_list.append(my_user_id)

        return connected_users_id_list

    def is_connected(self, sender, receiver):
        '''
        Check if two users are connected.
        '''
        # TODO: To be implemented. Currently, return True.
        return True

    def _get_user_by_id(self, user_id):
        '''
        Get user by id.
        '''
        return self.users[user_id]

    def send_ledger(self, sender_id, receiver_id, ledger):
        '''
        Send a ledger to the receiver.
        Return a boolean "future" indicating if the ledger is sent successfully.
        The result can be accessed by the `result()` method.
        '''
        # get user by id.
        sender = self._get_user_by_id(sender_id)
        receiver = self._get_user_by_id(receiver_id)
        if sender is None or receiver is None:
            raise Exception(
                "Failed to send ledger from {} to user {}".format(sender_id, receiver_id))

        # check if the sender and receiver are connected.
        if not self.is_connected(sender.id, receiver.id):
            raise Exception(
                "Failed to send ledger from {} to user {}".format(sender_id, receiver_id))

        return self.thread_pool.run_task_async(receiver_id, "receive_ledger", ledger, is_write=True)
