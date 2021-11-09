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

class Transaction:
    def __init__(self, sender: User, receiver: User, amount):
        self.sender = sender
        self.receiver = receiver
        self.signature = None
        self.amount = amount
        self.timestamp = time.time()
        self.hash = None

    def has_signature(self):
        return self.signature is not None

    def add_signature(self, signature):
        self.signature = signature

    def set_hash(self, hash):
        self.hash = hash
