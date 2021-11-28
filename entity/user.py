#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file define the user in the blockchain.

'''

import requests
from util import encrypt
from .ledger import Ledger
from .ledger import UserDigest
from .transaction import Transaction
from entity import ledger
import math
import time
from config import Config, SimulationConfig
from router import update_delegate


class User:
    '''
    User class.
    '''

    def __init__(self, id, init_ledger, init_balance, radius=10):
        self.id: int = id
        self.private_key, self.public_key = encrypt.generate_key_pair()
        # every user should hold a set of ledgers
        # becuase they may receive from different users
        self.ledgers = init_ledger
        self.balance = init_balance
        self.radius = radius
        self.delegate_history = []
        self.delegate_percentage = SimulationConfig.delegate_percentage
        self.is_delegate = False

    def add_transaction(self, receiver_id, amount):
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
            if i == 0:
                last_transaction = None
            else:
                last_transaction = ledger.transactions[i - 1]
            if transaction.calculate_hash(last_transaction).hexdigest() != transaction.hash.hexdigest():
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

        # verify the pending status
        if not self.check_delegate_signature(ledger):
            return False

        return True

    def choose_delegate(self):
        scores = {}
        for uid in self.ledgers[0].user_list.keys():
            scores[uid] = self.ledgers[0].calculate_weight(uid)
            for i in range(1, 4):
                if len(self.delegate_history) >= i and (uid in self.delegate_history[-i][1]):
                    scores[uid] = scores[uid] * 0.8
        print(scores)
        result = list(dict(
            sorted(scores.items(), key=lambda item: item[1])).keys())
        result.reverse()
        num_delegate = int(
            math.ceil(len(result) * self.delegate_percentage / 100))
        delegate_group = set(result[:num_delegate])
        self.delegate_history.append((time.time(), delegate_group))

        # judge that the user is delegate or not
        if self.id in delegate_group:
            self.is_delegate = True
            if SimulationConfig.visual_mode:
                requests.get(SimulationConfig.server_url+"/update_delegate", params={
                             "delegate_id": self.id, "is_delegate": self.is_delegate})
        else:
            self.is_delegate = False
            if SimulationConfig.visual_mode:
                requests.get(SimulationConfig.server_url+"/update_delegate", params={
                             "delegate_id": self.id, "is_delegate": self.is_delegate})

        return delegate_group

    def sign_delegate(self):
        '''
        delegate sign the ledger
        '''
        if self.is_delegate:
            # Sign the longest and the largest ledger
            longest_length = max(
                [len(ledger.transactions) for ledger in self.ledgers])
            longest_ledgers = [
                ledger for ledger in self.ledgers if len(ledger.transactions) == longest_length]
            final_ledger = None
            for ledger in longest_ledgers:
                if len(ledger.transactions) == 0:
                    return

                def a_larger_than_b(a, b):
                    '''
                    Return True if a is larger than b.
                    args a and b are bytes
                    '''
                    return int.from_bytes(a, byteorder='big') > int.from_bytes(b, byteorder='big')

                if final_ledger is None or a_larger_than_b(
                        ledger.transaction[-1].hash.hexdigest().encode(), final_ledger.transaction[-1].hash.hexdigest().encode()):
                    final_ledger = ledger

            if final_ledger is None:
                raise Exception("No ledger to sign!")

            final_ledger.transactions[-1].delegates_verify(
                self.id, encrypt.sign_message(self.private_key, final_ledger.transactions[-1].hash))

    def check_delegate_signature(self, ledger):
        '''
        Check the delegates signature of the ledger.
        '''
        # TODO: To be tested
        def verify_delegates_sign(transaction):
            '''
            Verify if signature is fully signed.
            '''
            for i in range(len(self.delegate_history)):
                if self.delegate_history[-i - 1][1] == transaction.delegates_sign.keys():
                    for id_sign in transaction.delegates_sign.items():
                        if not encrypt.verify_signature(self.ledgers[0].get_user_public_key(
                                id_sign[0]), id_sign[1], transaction.hash):
                            return False
                    return True
            return False

        for i in range(len(ledger.transactions)):
            if not ledger.transactions[-i - 1].is_pending:
                return verify_delegates_sign(ledger.transactions[-i - 1])

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
                self.ledgers.append(ledger.deepcopy())
            else:
                # append the ledgerdebugOptions
                self.ledgers.append(ledger.deepcopy())

    def handle_new_ledger(self, in_ledger):
        valid_len_in = 0
        for transaction in in_ledger.transactions:
            if not transaction.is_pending:
                valid_len_in += 1
            else:
                break
        valid_hash_in = in_ledger.transactions[valid_len_in -
                                               1].hash.hexdigest()

        valid_len_present = 0
        for transaction in self.ledgers[0].transactions:
            if not transaction.is_pending:
                valid_len_present += 1
            else:
                break

        if valid_len_in < valid_len_present:
            # New ledger has shorter singed chain
            return

        # Existing ledger all have shorter signed chain
        for ledger in self.ledgers:
            if len(ledger.transactions) <= valid_len_in:
                # Exisitng ledger is shorter than new ledger's valid length
                self.ledgers.remove(ledger)
            elif ledger.transactions[valid_len_in - 1].hash.hexdigest() != valid_hash_in:
                # Existing ledger is not on the same chain as the common chain
                self.ledgers.remove(ledger)

        saved_ledgers = []
        for index in range(valid_len_in, len(in_ledger.transactions)):
            for ledger in self.ledgers:
                if len(ledger.transactions) <= index:
                    self.ledgers.remove(ledger)
                elif ledger.transactions[index].hash.hexdigest() != in_ledger.transactions[index].hash.hexdigest():
                    saved_ledgers.append(ledger)
                    self.ledgers.remove(ledger)
                else:
                    ledger.transactions[index].delegates_sign.update(
                        in_ledger.transactions[index].delegates_sign)
                    in_ledger.transactions[index].delegates_sign.update(
                        ledger.transactions[index].delegates_sign)
                    end_pend = True
                    for uid in self.delegate_history[-1][1]:
                        if uid not in in_ledger.transactions[index].delegates_sign:
                            end_pend = False
                    if end_pend:
                        in_ledger.transactions[index].is_pending = False
                        ledger.transactions[index].is_pending = False
        if len(self.ledgers) == 0:
            self.ledgers.append(in_ledger.deepcopy())
        self.ledgers += saved_ledgers
        for ledger in self.ledgers:
            ledger.transactions[:valid_len_in] = [
                a.deepcopy() for a in in_ledger.transactions[:valid_len_in]]

    def receive_ledger(self, ledger, network=None):
        '''
        Receive the ledger from other users.
        Return True if the ledger is valid and added to the user.
        Return False if the ledger is invalid.
        '''
        # judge whether the user already have a same one
        if self.check_ledger_same(ledger):
            return

        if self.verify_ledger(ledger):

            self.handle_new_ledger(ledger)
            # TODO: should be inserted into handle_new_ledger function
            if network is not None:
                self.spread_ledger(ledger, network)
            else:
                print("No network to spread ledger!")
            # update the balance
            self.update_balance(ledger)
        else:
            print("Failed to send ledger from others to user {}".format(self.id))

    def spread_ledger(self, ledger, network):
        '''
        Spread a specific ledger to other users.
        '''
        user_id_list = network.get_connected_users(self.id)
        for receiver_id in user_id_list:
            network.send_ledger(self.id, receiver_id, ledger)

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
        for receiver_id in receiver_list:
            for ledger in self.ledgers:
                network.send_ledger(self.id, receiver_id, ledger)

    def drop_ledger(self, ledger):
        '''
        Drop the ledger from the user.
        '''
        self.ledgers.remove(ledger)

    def update_balance(self, ledger):
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
        self.ledgers = user.ledgers
        self.balance = user.balance
        self.radius = user.radius

    def get_ledgers_str(self):
        return "\n".join(str(l) for l in self.ledgers)

    def check_ledger_same(self, ledger_in):
        def check_two_ledger(ledger_my, ledger_in):
            if(len(ledger_my.transactions) != len(ledger_in.transactions)):
                return False
            if(len(ledger_in.transactions) == 0):
                # should warn others this is bad node
                print(str(self.id) + ' is currently under attack')
                return True

            if ledger_my.transactions[-1].hash.hexdigest() != ledger_in.transactions[-1].hash.hexdigest():
                return False

            # check sign
            checked_length_my = ledger_my.delegates_sign_len()
            checked_length_in = ledger_in.delegates_sign_len()
            if(checked_length_in != checked_length_my):
                return False
            for i in range(checked_length_in, len(ledger_my.transactions)):
                if ledger_my.transactions[i].delegates_sign.keys() != ledger_in.transactions[i].delegates_sign.keys():
                    return False
            return True

        for ledger in self.ledgers:
            if check_two_ledger(ledger, ledger_in):
                return True

        return False
