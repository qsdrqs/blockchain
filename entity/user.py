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
from util import encrypt


class User:
    '''
    User class.
    '''

    def __init__(self, user_id, init_ledger: list[Ledger]):
        self.id = user_id
        self.public_key, self.private_key = encrypt.generate_key_pair()
        # every user should hold a set of ledgers
        # becuase they may receive from different users
        self.ledgers = init_ledger

    def add_transation(self, receiver: User, amount):
        # We should append every ledger in the transaction to the ledger list
        for ledger in self.ledgers:
            transaction = Transaction(self, receiver, amount, ledger)
            transaction.add_signature(
                self.sign(transaction, self.private_key, ledger))
            ledger.transactions.append(transaction)

    def sign(self, transaction: Transaction, private_key, ledger):
        '''
        Sign the transaction.
        signature is the only position that a user can use its private key.
        '''
        private_key.sign(transaction.hash, transaction.signature)

    def verify_ledger(self, ledger: Ledger):
        '''
        Verify the ledger.
        need to verify the hash value of every transaction in the ledger.
        And the signature of every transaction.
        '''
        for i in range(len(ledger.transactions)):
            # verify the hash value
            transaction = ledger.transactions[i]
            sub_ledger = ledger.transactions[:i]
            if transaction.calculate_hash(sub_ledger) != transaction.hash:
                return False

        # verify the signature
        for transaction in ledger.transactions:
            sender_public_key = transaction.sender.public_key
            if not sender_public_key.verify(transaction.hash, transaction.signature):
                return False
