#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This module defines some entity classes

'''
import unittest
from entity import *
from util import *
import time


class TestTransaction(unittest.TestCase):
    def setUp(self):
        # init users
        self.user1 = User(1, [], 1000)
        self.user2 = User(2, [], 1000)

        # init ledger
        self.ledger = Ledger(
            [self.user1.generate_digest(), self.user2.generate_digest()], [])
        self.user1.ledgers.append(self.ledger.deepcopy())
        self.user2.ledgers.append(self.ledger.deepcopy())

        # init network
        self.network = Network(100, 100, [self.user1, self.user2])

    def test_verify(self):
        # init transactions
        # we skip the spread process
        self.user1.add_transaction(2, 100)
        self.user2.ledgers[0] = self.user1.ledgers[0].deepcopy()

        self.user2.add_transaction(1, 50)
        self.user1.ledgers[0] = self.user2.ledgers[0].deepcopy()

        self.assertTrue(self.user1.verify_ledger(self.user1.ledgers[0]))

    def test_minus_balance(self):
        self.assertFalse(self.user1.add_transaction(2, 2000))

    def test_change_balance_manually(self):
        # init transactions
        # we skip the spread process
        self.user1.add_transaction(2, 100)
        self.user2.ledgers[0] = self.user1.ledgers[0].deepcopy()

        self.user2.add_transaction(1, 50)
        self.user1.ledgers[0] = self.user2.ledgers[0].deepcopy()

        # test user1 modify his init balance on ledger
        self.user1.ledgers[0].user_list[0].init_balance = 3000
        self.assertTrue(self.user1.add_transaction(2, 2000))
        self.assertFalse(self.user2.verify_ledger(self.user1.ledgers[0]))

    def test_spread_transaction(self):
        # init transactions
        self.user1.add_transaction(2, 100)
        self.user1.spread_ledgers(self.network)
        self.user2.add_transaction(1, 50)
        self.user2.spread_ledgers(self.network)

        def same_ledger(ledger1, ledger2):
            # we only check the transactions
            if len(ledger1.transactions) != len(ledger2.transactions):
                return False
            for i in range(len(ledger1.transactions)):
                if ledger1.transactions[i].hash.hexdigest() != ledger2.transactions[i].hash.hexdigest():
                    return False

            return True

        self.assertTrue(len(self.user1.ledgers) ==
                        len(self.user2.ledgers) == 1)
        self.assertTrue(same_ledger(
            self.user1.ledgers[0], self.user2.ledgers[0]))

    def test_append_ledger(self):
        # init transactions
        self.user1.add_transaction(2, 100)
        self.user2.add_transaction(1, 50)
        self.user1.spread_ledgers(self.network)
        self.user2.spread_ledgers(self.network)

        self.assertTrue(len(self.user1.ledgers) ==
                        len(self.user2.ledgers) == 2)


class TestMultiThreadTransaction(unittest.TestCase):
    def setUp(self):
        # init users
        self.user_list = []
        for i in range(10):
            self.user_list.append(User(i + 1, [], 1000))

        # init ledger
        user_digest = []
        for user in self.user_list:
            user_digest.append(user.generate_digest())

        self.ledger = Ledger(
            user_digest, [])

        for user in self.user_list:
            user.ledgers.append(self.ledger.deepcopy())

        # init network
        self.network = Network(100, 100, self.user_list)

    def test_spread_ledger(self):
        # init transactions
        self.network.thread_pool.run_task_async(
            self.user_list[0].id, "add_transaction", 2, 100, is_write=True)
        self.network.thread_pool.run_task_async(
            self.user_list[1].id, "add_transaction", 3, 200, is_write=True)
        self.network.thread_pool.run_task_async(
            self.user_list[2].id, "add_transaction", 1, 300, is_write=True)

        # spread ledger
        self.network.thread_pool.run_task_async(
            self.user_list[0].id, "send_ledgers", self.network, [2, 3])
        self.network.thread_pool.run_task_async(
            self.user_list[1].id, "send_ledgers", self.network, [3, 1])
        self.network.thread_pool.run_task_async(
            self.user_list[2].id, "send_ledgers", self.network, [1, 2])

        self.network.thread_pool.threadpool.shutdown()

        self.assertTrue(len(self.user_list[0].ledgers)
                        == len(self.user_list[1].ledgers)
                        == len(self.user_list[2].ledgers)
                        == 1)
