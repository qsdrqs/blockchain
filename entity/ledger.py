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

from entity import *


class Ledger:
    '''
    The ledger class is used to caculate the weight of every user.
    And provide method to caculate the balance of every user.
    '''

    def __init__(self, user_list, init_transactions):
        '''
        Initialize the ledger.

        Args:
            user_list: a list of user objects.
        '''
        self.user_list = user_list
        self.transactions = init_transactions

    def get_user_list(self):
        '''
        Get the user list.

        Returns:
            a list of user objects.
        '''
        return self.user_list

    def get_user_by_id(self, user_id):
        '''
        Get the user object by user id.

        Args:
            user_id: the user id.

        Returns:
            the user object.
        '''
        for user in self.user_list:
            if user.get_id() == user_id:
                return user
        return None

    def calculate_weight(self, user_id):
        '''
        Calculate the weight of the user.
        '''
        user = self.get_user_by_id(user_id)
        if user is None:
            return None

        # TODO: implement this method

    def append(self, transaction: Transaction):
        '''
        Append a transaction to the ledger.
        Before appending, the ledger should add the hash verification on the head of this transaction.

        Args:
            transaction: the transaction object.
        '''
        hash_value = self.calculate_hash(transaction)
        transaction.set_hash(hash_value)
        self.transactions.append(transaction)

    def calculate_hash(self, transaction):
        '''
        Calculate the hash value of the original chain adds on this transaction.
        '''
        pass
