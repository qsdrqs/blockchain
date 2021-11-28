#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file is the test file of network.

'''
import unittest
import entity.network
from entity import *
from random import randrange


class TestNetwork(unittest.TestCase):
    def setUp(self):
        # init users
        self.user_list = []
        for i in range(100):
            self.user_list.append(User(i, [], 1000, randrange(10, 20)))

        # init ledger
        user_digest = []
        for user in self.user_list:
            user_digest.append(user.generate_digest())

        self.ledger = Ledger(
            user_digest, [])

        for user in self.user_list:
            user.ledgers.append(self.ledger.deepcopy())

        # init network
        self.network = Network(cols=100, rows=100, users=self.user_list)

    def test_refresh_network(self):
        self.network.refresh_network()
        print(self.network.connect_matrix)
        previous = self.network.network_matrix.copy()
        self.network.random_walk()
        print(self.network.connect_matrix)
        now = self.network.network_matrix
        count = 0
        for i in range(100):
            for j in range(100):
                if(previous[i, j] != now[i, j]):
                    count += 1
        print(count)
        self.assertTrue(self.network.is_connected_graph())

    # def test_connect_users(self):
    #     # user1 and user2 are connected
    #     self.assertTrue(self.network.is_connected(
    #         self.user_list[0], self.user_list[1]))

    def tearDown(self):
        pass
