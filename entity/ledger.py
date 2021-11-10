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


class Ledger():
    '''
    The ledger class is used to caculate the weight of every user.
    And provide method to caculate the balance of every user.
    '''

    def __init__(self, user_list: list[User], init_transactions: list[Transaction]):
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
            the user' public key.
        '''
        for user in self.user_list:
            if user.id == id:
                return user.public_key
        return None

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
