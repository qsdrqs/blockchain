#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file define the user in the blockchain.

'''

from entity import *


class User:
    '''
    User class.
    '''

    def __init__(self, user_id, public_key, private_key, init_ledger: Ledger):
        self.id = user_id
        self.public_key = public_key
        self.private_key = private_key

        # every user should hold a set of ledgers
        # becuase they may receive from different users
        self.ledger = init_ledger

    def add_transation(self, receiver: User, amount):
        transaction = Transaction(self.public_key, receiver.public_key, amount)
        self.ledger.append(transaction)
        self.signature(transaction, self.private_key)

    def signature(self, transaction: Transaction, signature):
        pass

    def verify_ledger(self, ledger: Ledger):
        '''
        Verify the ledger.
        need to verify every 
        '''
        pass
