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

    def __init__(self, sender_id, receiver_id, amount, ledger=None, timestamp=None, hash=None, signature=None, is_pending = True):
        # Manually implement overload...
        # Rubbish Python...
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.is_pending = is_pending
        self.delegates_sign = {}
        if timestamp is None and hash is None and signature is None and ledger is not None:
            self.signature = None
            self.timestamp = time.time()
            if (len(ledger.transactions) == 0):
                self.hash = self.calculate_hash(None)
            else:
                self.hash = self.calculate_hash(ledger.transactions[-1])
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

    def calculate_hash(self, last_transaction):
        self_message = str(
            self.sender_id + self.receiver_id + self.timestamp + self.amount).encode()
        if last_transaction is None:
            last_message = b''
        else:
            last_message = last_transaction.hash.hexdigest().encode()

        return util.hash_message(last_message+self_message)

    def deepcopy(self):
        return Transaction(self.sender_id, self.receiver_id,
                           self.amount, timestamp=self.timestamp, hash=self.hash, signature=self.signature, is_pending=self.is_pending)

    def delegates_verify(self, did, signature):
        self.delegates_sign[did] = signature
        # if len(self.delegates_sign) ==

    def toString(self):
        return f"Time {self.timestamp}, from {self.sender_id} to {self.receiver_id}, amt {self.amount}, pend {self.is_pending}\n"
