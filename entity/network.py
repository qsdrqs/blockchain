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
<<<<<<< HEAD
=======
import queue
from random import randrange
from config import Config
>>>>>>> 007b254e1aff119c27d9de3098a239fb9753a8aa
from util.multithreading import ThreadPool


class Network:
    '''
    Network entity.
    '''

<<<<<<< HEAD
    def __init__(self, rows, cols, users: list):
=======
    def __init__(self, rows=Config.network_row, cols=Config.network_col, users: list=[]):
>>>>>>> 007b254e1aff119c27d9de3098a239fb9753a8aa
        '''
        Initialize the network.

        Args:
            rows: number of rows in the network.
            cols: number of columns in the network.
            users: user list in the network.
        '''
        self.users = {}
        # len(self.users) always return 1, so add new variable self.user_count
        self.user_count = 0
        self.rows = rows
        self.cols = cols

        for user in users:
            self.users[user.id] = user
            self.user_count = self.user_count+1

        # Initialize the network.
        self.network_matrix = matlib.empty((rows, cols), dtype=User)
<<<<<<< HEAD
=======
        pos = {}
        pos_count = 0
        for user in self.users.values():
            pos_temp = [randrange(rows), randrange(cols)]
            if(pos_count == 0):
                pos[pos_count] = pos_temp
                pos_count += 1
            j = 0
            while j != len(pos):
                if(pos_temp == pos[j]):
                    pos_temp = [randrange(rows), randrange(cols)]
                else:
                    j = j+1
            pos[user.id] = pos_temp
            self.network_matrix[pos_temp[0], pos_temp[1]] = user

>>>>>>> 007b254e1aff119c27d9de3098a239fb9753a8aa
        # self.network_matrix[1,2] = self.users[1]
        # Initialize the connect matrix.
        # TODO: initalized as all True for testing. Should be all False.
        self.connect_matrix = matlib.ones(
            (len(users), len(users)), dtype=bool)
<<<<<<< HEAD

        # Initialize the thread pool.
=======
        for user1 in self.users.keys():
            for user2 in self.users.keys():
                if user1 != user2:
                    com_radius = min(self.users[user1].radius, self.users[user2].radius)
                    vec1 = np.array(pos[user1])
                    vec2 = np.array(pos[user2])
                    distance = np.sqrt((vec1[0]-vec2[0])*(vec1[0]-vec2[0]) + (vec1[1]-vec2[1])*(vec1[1]-vec2[1]))
                    if(distance <= com_radius):
                        self.connect_matrix[user1, user2] = True
                        self.connect_matrix[user2, user1] = True

            # Initialize the thread pool.
>>>>>>> 007b254e1aff119c27d9de3098a239fb9753a8aa
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
        # Initia
        # lize the network.
        self.network_matrix = matlib.empty((self.rows, self.cols), dtype=User)
        pos = {}
        pos_count = 0
        for user in self.users.values():
            pos_temp = [randrange(self.rows), randrange(self.cols)]
            if(pos_count == 0):
                pos[pos_count] = pos_temp
            j = 0
            while j != len(pos):
                if(pos_temp == pos[j]):
                    pos_temp = [randrange(self.rows), randrange(self.cols)]
                else:
                    j = j+1
            pos[user.id] = pos_temp
            self.network_matrix[pos_temp[0], pos_temp[1]] = user

        # self.network_matrix[1,2] = self.users[1]
        # Initialize the connect matrix.
        # TODO: initalized as all True for testing. Should be all False.
        self.connect_matrix = matlib.zeros(
            (self.user_count, self.user_count), dtype=bool)
        for user1 in self.users.keys():
            for user2 in self.users.keys():
                if user1 != user2:
                    com_radius = min(self.users[user1].radius, self.users[user2].radius)
                    vec1 = np.array(pos[user1])
                    vec2 = np.array(pos[user2])
                    distance = np.sqrt((vec1[0]-vec2[0])*(vec1[0]-vec2[0]) + (vec1[1]-vec2[1])*(vec1[1]-vec2[1]))
                    if(distance <= com_radius):
                        self.connect_matrix[user1, user2] = True
                        self.connect_matrix[user2, user1] = True

        def is_connected_graph(self):
            '''
            Check if the network is connected.
            '''
<<<<<<< HEAD
            return True

        pass  # TODO
        if not is_connected_graph(self):
=======
            # initialize checked user dict
            user_checked = {}
            for user_id in self.users:
                user_checked[user_id] = False
            # bfs determine graph is connect or not
            q = queue.Queue()
            q.put(list(self.users.keys())[0])
            user_checked[0] = True
            count = 1
            while not q.empty():
                print('dxx')
                current_id = q.get()
                connected_user = self.get_connected_users(current_id)
                for i in range(len(connected_user)):
                    if user_checked[connected_user[i]] == False:
                        q.put(connected_user[i])
                        user_checked[connected_user[i]] = True
                        count = count + 1
            return count == self.user_count

        # pass  # TODO
        while not is_connected_graph():
>>>>>>> 007b254e1aff119c27d9de3098a239fb9753a8aa
            self.refresh_network()

    def get_connected_users(self, user_id):
        '''
        Get the connected users of specified user.
        '''
        # TODO: To be implemented. Currently, return all other users.
        connected_users_id_list = []
<<<<<<< HEAD
        for my_user_id in self.users:
            if my_user_id != user_id:
=======
        for my_user_id in self.users.keys():
            if(self.connect_matrix[user_id, my_user_id]):
>>>>>>> 007b254e1aff119c27d9de3098a239fb9753a8aa
                connected_users_id_list.append(my_user_id)

        return connected_users_id_list

    def is_connected(self, sender, receiver):
        '''
        Check if two users are connected.
        '''
        # TODO: To be implemented. Currently, return True.
<<<<<<< HEAD
        return True
=======
        return self.connect_matrix[sender.id, receiver.id]
>>>>>>> 007b254e1aff119c27d9de3098a239fb9753a8aa

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


def test():
    pass


if __name__ == '__main__':
    test()


# 卡在 refresh里了，无法构建出连通图
