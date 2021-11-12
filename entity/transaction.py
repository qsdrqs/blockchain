#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file is class of transaction.

'''
from . import *
import time
import util


class Transaction:
    '''
    Transaction class
    '''

    def __init__(self, sender_id, receiver_id, amount, ledger):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.signature = None
        self.amount = amount
        self.timestamp = time.time()
        self.hash = self.calculate_hash(ledger.transactions)
        # We need to add this transaction to the ledger immediately to ensure the hash correct
        ledger.append(self)

    def has_signature(self):
        return self.signature is not None

    def add_signature(self, signature):
        self.signature = signature

    def calculate_hash(self, transactions_list):
        self_message = util.float_to_bytes(
            self.sender_id + self.receiver_id + self.timestamp)
        transaction_messages = b''
        for transaction in transactions_list:
            transaction_messages += transaction.hash.hexdigest().encode()

        return util.hash_message(transaction_messages+self_message)
