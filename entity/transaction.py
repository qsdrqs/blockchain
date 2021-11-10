#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file is class of transaction.

'''
from entity import *
import time
import hashlib


class Transaction:
    '''
    Transaction class
    '''

    def __init__(self, sender: User, receiver: User, amount, ledger: Ledger):
        self.sender = sender
        self.receiver = receiver
        self.signature = None
        self.amount = amount
        self.timestamp = time.time()
        self.hash = self.calculate_hash(ledger.transactions)

    def has_signature(self):
        return self.signature is not None

    def add_signature(self, signature):
        self.signature = signature

    def calculate_hash(self, transactions_list):
        self_hash: str = hashlib.sha256(
            self.sender.id + self.receiver.id + self.timestamp).hexdigest()
        tx_hash: str = ""
        for tx in transactions_list:
            tx_hash += hashlib.sha256(tx).hexdigest()

        return hashlib.sha256((self_hash + tx_hash).encode()).hexdigest()
