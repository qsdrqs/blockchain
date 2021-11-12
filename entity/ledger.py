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

    def __init__(self, user_list: list[UserDigest], init_transactions: list[Transaction]):
        '''
        Initialize the ledger.

        Args:
            user_list: a list of user objects.
        '''
        self.user_list = user_list
        self.transactions = init_transactions

    def get_user_public_key(self, id):
        '''
        Get the user object by user id.

        Args:
            id: the user id.

        Returns:
            the user's public key.
        '''
        for user in self.user_list:
            if user.id == id:
                return user.public_key
        return None

    def get_user_balance(self, id, init_balance=-1):
        '''
        Get the balance of the user.
        We need to caculate the balance of every user from the transactions.
        FIXME: Can be optimized.
        '''
        if init_balance == -1:
            for user in self.user_list:
                if user.id == id:
                    init_balance = user.init_balance
                    break

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
        pass

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
        for user in self.user_list:
            user_list.append(UserDigest(
                user.id, user.public_key, user.init_balance))

        # deep copy the transactions
        transactions = []
        for transaction in self.transactions:
            transactions.append(transaction.deepcopy())

        return Ledger(user_list, transactions)
