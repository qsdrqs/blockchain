#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file define the user in the blockchain.

'''

from util import encrypt
from .ledger import Ledger
from .ledger import UserDigest
from .transaction import Transaction


class User:
    '''
    User class.
    '''

    def __init__(self, id, init_ledger: list[Ledger], init_balance):
        self.id = id
        self.private_key, self.public_key = encrypt.generate_key_pair()
        # every user should hold a set of ledgers
        # becuase they may receive from different users
        self.ledgers = init_ledger
        self.balance = init_balance

    def add_transation(self, receiver_id, amount):
        '''
        Add a transaction to every ledger of user.
        return:
            True if the transaction added successfully.
            False if the transaction is invalid.
        '''
        # We should append every ledger in the transaction to the ledger list
        for ledger in self.ledgers:
            # The next step has added the transaction to the ledger
            transaction = Transaction(self.id, receiver_id, amount, ledger)
            transaction.add_signature(
                encrypt.sign_message(self.private_key, transaction.hash))
            if ledger.get_user_balance(self.id) >= amount:
                # We need to add this transaction to the ledger immediately to ensure the hash correct
                ledger.append(transaction)
                return True
            else:
                return False

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
            if transaction.calculate_hash(sub_ledger).hexdigest() != transaction.hash.hexdigest():
                return False

        # verify the signature
        for transaction in ledger.transactions:
            if not transaction.has_signature():
                return False

            sender_public_key = self.ledgers[0].get_user_public_key(
                transaction.sender_id)
            if sender_public_key is None or not encrypt.verify_signature(sender_public_key, transaction.signature, transaction.hash):
                return False

        # verify the balance, make sure everyone has a correct balance
        for user in self.ledgers[0].user_list:
            if ledger.get_user_balance(user.id, user.init_balance) < 0:
                return False

        return True

    def generate_digest(self):
        '''
        Generate the digest of the user.
        Used in initializing the ledger.
        '''
        return UserDigest(self.id, self.public_key, self.balance)

    def receive_ledgers(self, ledger):
        '''
        Receive the ledger from other users.
        '''

    def spread_ledgers(self, user_list):
        '''
        Spread the ledger to other users.
        '''
        for ledger in self.ledgers:
            ledger.spread_ledger()
