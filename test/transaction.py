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
        self.user1.add_transation(2, 100)
        self.user2.ledgers[0] = self.user1.ledgers[0].deepcopy()

        self.user2.add_transation(1, 50)
        self.user1.ledgers[0] = self.user2.ledgers[0].deepcopy()

        self.assertTrue(self.user1.verify_ledger(self.user1.ledgers[0]))

    def test_minus_balance(self):
        self.assertFalse(self.user1.add_transation(2, 2000))

    def test_change_balance_manually(self):
        # init transactions
        # we skip the spread process
        self.user1.add_transation(2, 100)
        self.user2.ledgers[0] = self.user1.ledgers[0].deepcopy()

        self.user2.add_transation(1, 50)
        self.user1.ledgers[0] = self.user2.ledgers[0].deepcopy()

        # test user1 modify his init balance on ledger
        self.user1.ledgers[0].user_list[0].init_balance = 3000
        self.assertTrue(self.user1.add_transation(2, 2000))
        self.assertFalse(self.user2.verify_ledger(self.user1.ledgers[0]))

    def test_spread_transaction(self):
        # init transactions
        self.user1.add_transation(2, 100)
        self.user1.spread_ledgers(self.network)
        self.user2.add_transation(1, 50)
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
        self.user1.add_transation(2, 100)
        self.user2.add_transation(1, 50)
        self.user1.spread_ledgers(self.network)
        self.user2.spread_ledgers(self.network)

        self.assertTrue(len(self.user1.ledgers) ==
                        len(self.user2.ledgers) == 2)
