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

    def __init__(self, sender_id, receiver_id, amount, ledger=None, timestamp=None, hash=None, signature=None):
        # Manually implement overload...
        # Rubbish Python...
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.is_pending = False
        self.delegates_sign = []
        if timestamp is None and hash is None and signature is None and ledger is not None:
            self.signature = None
            self.timestamp = time.time()
            self.hash = self.calculate_hash(ledger.transactions)
        elif timestamp is not None and hash is not None and signature is not None and ledger is None:
            self.signature = signature
            self.timestamp = timestamp
            self.hash = hash
        else:
            raise ValueError('Invalid transaction initialization')

    def has_signature(self):
        return self.signature is not None

    def add_signature(self, signature):
        self.signature = signature

    def calculate_hash(self, transactions_list):
        self_message = str(
            self.sender_id + self.receiver_id + self.timestamp + self.amount).encode()
        transaction_messages = b''
        for transaction in transactions_list:
            transaction_messages += transaction.hash.hexdigest().encode()

        return util.hash_message(transaction_messages+self_message)

    def deepcopy(self):
        return Transaction(self.sender_id, self.receiver_id,
                           self.amount, timestamp=self.timestamp, hash=self.hash, signature=self.signature)

    def delegates_verify(self, signature):
        self.delegates_sign.append(signature)
        # if len(self.delegates_sign) ==

    def toString(self):
        return f"Time {self.timestamp}, from {self.sender_id} to {self.receiver_id}, amt {self.amount}\n"
