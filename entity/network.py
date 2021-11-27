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
import queue
from random import randrange
from config import Config
from util.multithreading import ThreadPool


class Network:
    '''
    Network entity.
    '''

    def __init__(self, rows=Config.network_row, cols=Config.network_col, users: list=[]):
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
        self.pos = {}
        pos_count = 0
        for user in self.users.values():
            pos_temp = [randrange(rows), randrange(cols)]
            if(pos_count == 0):
                self.pos[pos_count] = pos_temp
                pos_count += 1
            j = 0
            while j != len(self.pos):
                if(pos_temp == self.pos[j]):
                    pos_temp = [randrange(rows), randrange(cols)]
                else:
                    j = j+1
            self.pos[user.id] = pos_temp
            self.network_matrix[pos_temp[0], pos_temp[1]] = user

        # self.network_matrix[1,2] = self.users[1]
        # Initialize the connect matrix.
        # TODO: initalized as all True for testing. Should be all False.
        self.connect_matrix = matlib.zeros(
            (len(users), len(users)), dtype=bool)
        for user1 in self.users.keys():
            for user2 in self.users.keys():
                if user1 != user2:
                    com_radius = min(self.users[user1].radius, self.users[user2].radius)
                    vec1 = np.array(self.pos[user1])
                    vec2 = np.array(self.pos[user2])
                    distance = np.sqrt((vec1[0]-vec2[0])*(vec1[0]-vec2[0]) + (vec1[1]-vec2[1])*(vec1[1]-vec2[1]))
                    if(distance <= com_radius):
                        self.connect_matrix[user1, user2] = True
                        self.connect_matrix[user2, user1] = True

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
        # Initia
        # lize the network.
        self.network_matrix = matlib.empty((self.rows, self.cols), dtype=User)
        self.pos = {}
        pos_count = 0
        for user in self.users.values():
            pos_temp = [randrange(self.rows), randrange(self.cols)]
            if(pos_count == 0):
                self.pos[pos_count] = pos_temp
            j = 0
            while j != len(self.pos):
                if(pos_temp == self.pos[j]):
                    pos_temp = [randrange(self.rows), randrange(self.cols)]
                else:
                    j = j+1
            self.pos[user.id] = pos_temp
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
                    vec1 = np.array(self.pos[user1])
                    vec2 = np.array(self.pos[user2])
                    distance = np.sqrt((vec1[0]-vec2[0])*(vec1[0]-vec2[0]) + (vec1[1]-vec2[1])*(vec1[1]-vec2[1]))
                    if(distance <= com_radius):
                        self.connect_matrix[user1, user2] = True
                        self.connect_matrix[user2, user1] = True

        
        # pass  # TODO
        while not self.is_connected_graph():
            self.refresh_network()
    
    def is_connected_graph(self):
            '''
            Check if the network is connected.
            '''
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
                current_id = q.get()
                connected_user = self.get_connected_users(current_id)
                for i in range(len(connected_user)):
                    if user_checked[connected_user[i]] == False:
                        q.put(connected_user[i])
                        user_checked[connected_user[i]] = True
                        count = count + 1
            # (count == self.user_count)
            return count == self.user_count


    def get_connected_users(self, user_id):
        '''
        Get the connected users of specified user.
        '''
        # TODO: To be implemented. Currently, return all other users.
        connected_users_id_list = []
        for my_user_id in self.users.keys():
            if(self.connect_matrix[user_id, my_user_id]):
                connected_users_id_list.append(my_user_id)

        return connected_users_id_list

    def is_connected(self, sender, receiver):
        '''
        Check if two users are connected.
        '''
        # TODO: To be implemented. Currently, return True.
        return self.connect_matrix[sender.id, receiver.id]

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

    def random_walk(self):

        walk_min_num = 5
        walk_max_num = 15

        def single_walk(walk_id):
            initial_pos = self.pos[walk_id]
            for i in range(randrange(walk_min_num,walk_max_num)):
                direction = randrange(0,4)
                if(direction == 0):
                    final_pos = [initial_pos[0],initial_pos[1]-1]
                elif(direction == 1):
                    final_pos = [initial_pos[0]+1,initial_pos[1]]
                elif(direction == 2):
                    final_pos = [initial_pos[0],initial_pos[1]+1]
                elif(direction == 3):
                    final_pos = [initial_pos[0]+1,initial_pos[1]]
            return final_pos

        def is_user_connected(walk_id,walk_pos):
            walk_user = self.users[walk_id]
            for user in self.users.keys():
                if(user != walk_user):
                    vec1 = np.array(walk_pos)
                    vec2 = np.array(self.pos[user])
                    distance = np.sqrt((vec1[0]-vec2[0])*(vec1[0]-vec2[0]) + (vec1[1]-vec2[1])*(vec1[1]-vec2[1]))
                    com_radius = min(self.users[walk_id].radius,self.users[user].radius)
                    if(distance < com_radius):
                        return True
            return False

        def is_pos_coincide(walk_pos):
            for user_id in self.users.keys():
                if(walk_pos == self.pos[user_id]):
                    return False
            return True

        walk_list = {}
        id_array = {}
        # select 10 percent users to random walk
        for i in range(int(self.user_count/10)):
            rand_id = randrange(0,self.user_count)
            id_array[i] = rand_id
            j = 0
            while j != i:
                if id_array[i] == id_array[j]:
                   id_array = randrange(0,self.user_count)
                else:
                    j = j+1
        for i in id_array.keys():
            walk_list[id_array[i]] = self.users[id_array[i]]
        
        # final_pos_list = {}
        for walk_id in walk_list.keys():
            initial_pos = self.pos[walk_id]
            final_pos = single_walk(walk_id)
            while not (is_user_connected(walk_id,final_pos) & is_pos_coincide(final_pos)):
                final_pos = single_walk(walk_id)
            self.network_matrix[final_pos[0],final_pos[1]] = self.users[walk_id]
            self.network_matrix[initial_pos[0],initial_pos[1]] = None
            self.pos[walk_id] = final_pos
        
        


            


def test():
    pass


if __name__ == '__main__':
    test()


# 卡在 refresh里了，无法构建出连通图
