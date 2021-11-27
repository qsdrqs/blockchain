#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file defines the ledger class that every user will have.

The ledeger should provide method to caculate the weight of every user.
And provide method to caculate the balance of every user.

'''

from . import *
from .transaction import Transaction
import statistics


class UserDigest():
    '''
    UserDigest is a class that contains the digest of a user.
    We need to define this class so that we can use it in the ledger.
    Put the User class in the ledger is dangerous because it will be able to access the private key of every user.
    '''

    def __init__(self, id, public_key, init_balance):
        self.id = id
        self.public_key = public_key
        self.init_balance = init_balance


class Ledger():
    '''
    The ledger class is used to caculate the weight of every user.
    And provide method to caculate the balance of every user.
    '''

    # def __init__(self, user_list: list[UserDigest], init_transactions: list[Transaction]):
    def __init__(self, user_list, init_transactions):
        '''
        Initialize the ledger.

        Args:
            user_list: a list of user digest.
        '''
        self.user_list = {}
        for user in user_list:
            self.user_list[user.id] = user
        self.transactions = init_transactions

    def get_user_public_key(self, id):
        '''
        Get the user object by user id.

        Args:
            id: the user id.

        Returns:
            the user's public key.
        '''
        return self.user_list[id].public_key

    def get_user_balance(self, id, init_balance=-1):
        '''
        Get the balance of the user.
        We need to caculate the balance of every user from the transactions.
        FIXME: Can be optimized.
        '''
        if init_balance == -1:
            init_balance = self.user_list[id].init_balance

        balance = init_balance
        if len(self.transactions) == 0:
            return balance

        for transaction in self.transactions:
            if transaction.sender_id == id:
                balance -= transaction.amount
            elif transaction.receiver_id == id:
                balance += transaction.amount

        return balance

    def calculate_weight(self, user_id):
        '''
        Calculate the weight of the user.
        '''
        # TODO: implement this method
        if user_id not in self.user_list:
            return None
        traned_user = set()
        traned_amt = []
        for transaction in self.transactions:
            if transaction.is_pending:
                continue
            if transaction.sender_id == user_id:
                traned_user.add(transaction.receiver_id)
                traned_amt.append(transaction.amount)
            elif transaction.receiver_id == user_id:
                traned_user.add(transaction.sender_id)
                traned_amt.append(transaction.amount)

        if len(traned_amt) != 0:
            return statistics.median(traned_amt) * len(traned_user)
        else:
            return 0

    def append(self, transaction: Transaction):
        '''
        Append a transaction to the ledger.
        Before appending, the ledger should add the hash verification on the head of this transaction.

        Args:
            transaction: the transaction object.
        '''
        self.transactions.append(transaction)

    def deepcopy(self):
        '''
        Deep copy the ledger.
        '''
        # deep copy the user list
        user_list = []
        for (user_id, user) in self.user_list.items():
            user_list.append(UserDigest(
                user.id, user.public_key, user.init_balance))

        # deep copy the transactions
        transactions = []
        for transaction in self.transactions:
            transactions.append(transaction.deepcopy())

        return Ledger(user_list, transactions)

    def delegates_sign_len(self) -> int:
        pass

    def __str__(self):
        return f"\nLedger {id(self)}\n User list: {self.user_list.keys()}\n Transactions: {['\n\t' + str(t) for t in self.transactions]}"

    