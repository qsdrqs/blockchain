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

    def test_sign(self):
        key, public_key = generate_key_pair()
        message = b'Hello, world!'
        message = hash_message(message)
        my_message = b'Hello, world'
        my_message = hash_message(my_message)
        signature = sign_message(key, message)
        self.assertTrue(verify_signature(public_key, signature, message))

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
