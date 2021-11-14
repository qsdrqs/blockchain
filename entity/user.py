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
from entity import ledger


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
                self.balance -= amount
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
        for (user_id, user) in self.ledgers[0].user_list.items():
            if ledger.get_user_balance(user.id, user.init_balance) < 0:
                return False

        return True

    def generate_digest(self):
        '''
        Generate the digest of the user.
        Used in initializing the ledger.
        '''
        return UserDigest(self.id, self.public_key, self.balance)

    def _append_or_update(self, ledger):
        '''
        Check if the ledger should be appended or replace the old one
        '''

        def same_ledger(ledger1, ledger2):
            '''
            Check if two ledgers are the same.
            '''
            longer = ledger1 if len(ledger1.transactions) >= len(
                ledger2.transactions) else ledger2
            shorter = ledger1 if len(ledger1.transactions) < len(
                ledger2.transactions) else ledger2
            for i in range(len(shorter.transactions)):
                # check the hash value of every common transaction
                if shorter.transactions[i].hash.hexdigest() != longer.transactions[i].hash.hexdigest():
                    return False

            return True

        for my_ledger in self.ledgers:
            if same_ledger(my_ledger, ledger):
                # update the ledger
                self.ledgers.remove(my_ledger)
                self.ledgers.append(ledger)
            else:
                # append the ledger
                self.ledgers.append(ledger)

    def receive_ledger(self, ledger):
        '''
        Receive the ledger from other users.
        Return True if the ledger is valid and added to the user.
        Return False if the ledger is invalid.
        '''
        if self.verify_ledger(ledger):
            self._append_or_update(ledger)
            # update the balance
            self.balance = ledger.get_user_balance(self.id)
            return True
        else:
            return False

    def spread_ledgers(self, network):
        '''
        Spread the ledger to all other user connected.
        '''
        user_id_list = network.get_connected_users(self.id)
        self.send_ledgers(network, user_id_list)

    def send_ledgers(self, network, receiver_list):
        '''
        Send the ledger to specific receivers.
        '''
        for ledger in self.ledgers:
            for receiver_id in receiver_list:
                if network.send_ledger(self.id, receiver_id, ledger).result():
                    continue
                else:
                    raise Exception(
                        "Failed to send ledger from {} to user {}".format(self.id, receiver_id))

    def drop_ledger(self, ledger):
        '''
        Drop the ledger from the user.
        '''
        self.ledgers.remove(ledger)

    def update_balane(self, ledger):
        '''
        Update the balance of the user.
        TODO: We should only accept verified transactions and pending transactions from himself.
        '''
        self.balance = ledger.get_user_balance(self.id)

    def deepcopy(self):
        '''
        Deep copy the user.
        '''
        ledgers = []
        for ledger in self.ledgers:
            ledgers.append(ledger.deepcopy())
        user = User(self.id, ledgers, self.balance)
        user.private_key = self.private_key
        user.public_key = self.public_key
        return user

    def update(self, user):
        '''
        Update the user with the other user.
        '''
        self = user
