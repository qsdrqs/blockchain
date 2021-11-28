#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This module defines some entity classes

'''
import unittest
from entity import *
from util import *
import time


class TestTransaction(unittest.TestCase):
    def setUp(self):
        # init users
        self.user1 = User(1, [], 1000)
        self.user2 = User(2, [], 1000)

        # init ledger
        self.ledger = Ledger(
            [self.user1.generate_digest(), self.user2.generate_digest()], [])
        self.user1.ledgers.append(self.ledger.deepcopy())
        self.user2.ledgers.append(self.ledger.deepcopy())

        # init network
        self.network = Network(100, 100, [self.user1, self.user2])

    @unittest.skip("skip")
    def test_verify(self):
        # init transactions
        # we skip the spread process
        self.user1.add_transaction(2, 100)
        self.user2.ledgers[0] = self.user1.ledgers[0].deepcopy()

        self.user2.add_transaction(1, 50)
        self.user1.ledgers[0] = self.user2.ledgers[0].deepcopy()

        self.assertTrue(self.user1.verify_ledger(self.user1.ledgers[0]))

    def test_minus_balance(self):
        self.assertFalse(self.user1.add_transaction(2, 2000))

    def test_change_balance_manually(self):
        # init transactions
        # we skip the spread process
        self.user1.add_transaction(2, 100)
        self.user2.ledgers[0] = self.user1.ledgers[0].deepcopy()

        self.user2.add_transaction(1, 50)
        self.user1.ledgers[0] = self.user2.ledgers[0].deepcopy()

        # test user1 modify his init balance on ledger
        self.user1.ledgers[0].user_list[self.user1.id].init_balance = 3000
        self.assertTrue(self.user1.add_transaction(2, 2000))
        self.assertFalse(self.user2.verify_ledger(self.user1.ledgers[0]))

    def test_spread_transaction(self):
        # init transactions
        self.user1.add_transaction(2, 100)
        self.user1.spread_ledgers(self.network)
        self.user2.add_transaction(1, 50)
        self.user2.spread_ledgers(self.network)
        print(self.user2.ledgers[0].toString())

        def same_ledger(ledger1, ledger2):
            # we only check the transactions
            if len(ledger1.transactions) != len(ledger2.transactions):
                return False
            for i in range(len(ledger1.transactions)):
                if ledger1.transactions[i].hash.hexdigest() != ledger2.transactions[i].hash.hexdigest():
                    return False

            return True

        self.assertTrue(len(self.user1.ledgers) ==
                        len(self.user2.ledgers) == 1)
        self.assertTrue(same_ledger(
            self.user1.ledgers[0], self.user2.ledgers[0]))

    def test_append_ledger(self):
        # init transactions
        self.user1.add_transaction(2, 100)
        self.user2.add_transaction(1, 50)
        self.user1.spread_ledgers(self.network)
        self.user2.spread_ledgers(self.network)

        self.network.thread_pool.threadpool.shutdown()

        self.assertTrue(len(self.user1.ledgers) ==
                        len(self.user2.ledgers) == 2)

class TestMergeSign(unittest.TestCase):
    def setUp(self):
        # init users
        num_user = 3
        self.users = []
        for i in range(1, num_user + 1):
            self.users.append(User(i, [], 1000))

        # init ledger
        self.ledger = Ledger(
            [user.generate_digest() for user in self.users], [])
    
    def test_merge_sign_pend_only(self):
        ledger_1 = self.ledger.deepcopy()
        tA = Transaction(1, 2, 30, ledger_1)
        tA.signature = 0
        tA.delegates_sign[1] = True
        tA.delegates_sign[2] = True
        tA.delegates_sign[3] = True
        ledger_1.append(tA)
        tB = Transaction(1, 2, 40, ledger_1)
        tB.signature = 0
        tB.delegates_sign[1] = True
        tB.delegates_sign[2] = True
        tB.delegates_sign[3] = True
        ledger_1.append(tB)
        tC = Transaction(1, 2, 50, ledger_1)
        tC.signature = 0
        tC.delegates_sign[1] = True
        ledger_1.append(tC)
        tD = Transaction(1, 2, 60, ledger_1)
        tD.signature = 0
        ledger_1.append(tD)
        ledger_1.transactions[0].is_pending = False
        ledger_1.transactions[1].is_pending = False
        self.users[0].ledgers.append(ledger_1.deepcopy())
        print("\n")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())
        ledger_1.transactions.remove(ledger_1.transactions[-1])
        tE = Transaction(1, 2, 70, ledger_1)
        tE.signature = 0
        del ledger_1.transactions[2].delegates_sign[1]
        ledger_1.transactions[2].delegates_sign[2] = True
        ledger_1.append(tE)
        print("In ledger: \n" + str(ledger_1))
        self.users[0].handle_new_ledger(ledger_1)
        print("----- Merging Ledger -----")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())

    def test_merge_sign_pend_chg(self):
        ledger_1 = self.ledger.deepcopy()
        tA = Transaction(1, 2, 30, ledger_1)
        tA.signature = 0
        tA.delegates_sign[1] = True
        tA.delegates_sign[2] = True
        tA.delegates_sign[3] = True
        ledger_1.append(tA)
        tB = Transaction(1, 2, 40, ledger_1)
        tB.signature = 0
        tB.delegates_sign[1] = True
        tB.delegates_sign[2] = True
        tB.delegates_sign[3] = True
        ledger_1.append(tB)
        tC = Transaction(1, 2, 50, ledger_1)
        tC.signature = 0
        tC.delegates_sign[1] = True
        ledger_1.append(tC)
        tD = Transaction(1, 2, 60, ledger_1)
        tD.signature = 0
        ledger_1.append(tD)
        ledger_1.transactions[0].is_pending = False
        ledger_1.transactions[1].is_pending = False
        self.users[0].ledgers.append(ledger_1.deepcopy())
        print("\n")
        self.users[0].delegate_percentage = 100
        dels = self.users[0].choose_delegate()
        print(dels)
        print("Local ledger: \n" + self.users[0].get_ledgers_str())
        ledger_1.transactions.remove(ledger_1.transactions[-1])
        tE = Transaction(1, 2, 70, ledger_1)
        tE.signature = 0
        del ledger_1.transactions[2].delegates_sign[1]
        ledger_1.transactions[2].delegates_sign[2] = True
        ledger_1.transactions[2].delegates_sign[3] = True
        ledger_1.append(tE)
        print("In ledger: \n" + str(ledger_1))
        self.users[0].handle_new_ledger(ledger_1)
        print("----- Merging Ledger -----")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())



class TestMerge2(unittest.TestCase):
    def setUp(self):
        # init users
        num_user = 3
        self.users = []
        for i in range(1, num_user + 1):
            self.users.append(User(i, [], 1000))

        # init ledger
        self.ledger = Ledger(
            [user.generate_digest() for user in self.users], [])

    def test_1(self):
        ledger_1 = self.ledger.deepcopy()
        tA = Transaction(1, 2, 30, ledger_1)
        tA.signature = 0
        ledger_1.append(tA)
        tB = Transaction(1, 2, 40, ledger_1)
        tB.signature = 0
        ledger_1.append(tB)
        tC = Transaction(1, 2, 50, ledger_1)
        tC.signature = 0
        ledger_1.append(tC)
        tD = Transaction(1, 2, 60, ledger_1)
        tD.signature = 0
        ledger_1.append(tD)
        ledger_1.transactions[0].is_pending = False
        ledger_1.transactions[1].is_pending = False
        self.users[0].ledgers.append(ledger_1.deepcopy())
        print("\n")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())
        ledger_1.transactions[2].is_pending = False
        print("In ledger: \n" + str(ledger_1))
        self.users[0].handle_new_ledger(ledger_1)
        print("----- Merging Ledger -----")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())

    def test_2(self):
        ledger_1 = self.ledger.deepcopy()
        tA = Transaction(1, 2, 30, ledger_1)
        tA.signature = 0
        ledger_1.append(tA)
        tB = Transaction(1, 2, 40, ledger_1)
        tB.signature = 0
        ledger_1.append(tB)
        tC = Transaction(1, 2, 50, ledger_1)
        tC.signature = 0
        ledger_1.append(tC)
        tD = Transaction(1, 2, 60, ledger_1)
        tD.signature = 0
        ledger_1.append(tD)
        ledger_1.transactions[0].is_pending = False
        ledger_1.transactions[1].is_pending = False
        self.users[0].ledgers.append(ledger_1.deepcopy())
        print("\n")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())
        ledger_1.transactions.remove(ledger_1.transactions[-1])
        ledger_1.transactions.remove(ledger_1.transactions[-1])
        tE = Transaction(1, 2, 50, ledger_1)
        tE.signature = 0
        ledger_1.append(tE)
        tF = Transaction(1, 2, 60, ledger_1)
        tF.signature = 0
        ledger_1.append(tF)
        print("In ledger: \n" + str(ledger_1))
        self.users[0].handle_new_ledger(ledger_1)
        print("----- Merging Ledger -----")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())

    def test_3(self):
        ledger_1 = self.ledger.deepcopy()
        tA = Transaction(1, 2, 30, ledger_1)
        tA.signature = 0
        ledger_1.append(tA)
        tB = Transaction(1, 2, 40, ledger_1)
        tB.signature = 0
        ledger_1.append(tB)
        tC = Transaction(1, 2, 50, ledger_1)
        tC.signature = 0
        ledger_1.append(tC)
        tD = Transaction(1, 2, 60, ledger_1)
        tD.signature = 0
        ledger_1.append(tD)
        ledger_1.transactions[0].is_pending = False
        ledger_1.transactions[1].is_pending = False
        self.users[0].ledgers.append(ledger_1.deepcopy())
        print("\n")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())
        ledger_1.transactions.remove(ledger_1.transactions[-1])
        tE = Transaction(1, 2, 70, ledger_1)
        tE.signature = 0
        ledger_1.append(tE)
        print("In ledger: \n" + str(ledger_1))
        self.users[0].handle_new_ledger(ledger_1)
        print("----- Merging Ledger -----")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())

    def test_4(self):
        ledger_1 = self.ledger.deepcopy()
        tA = Transaction(1, 2, 30, ledger_1)
        tA.signature = 0
        ledger_1.append(tA)
        tB = Transaction(1, 2, 40, ledger_1)
        tB.signature = 0
        ledger_1.append(tB)
        tC = Transaction(1, 2, 50, ledger_1)
        tC.signature = 0
        ledger_1.append(tC)
        tD = Transaction(1, 2, 60, ledger_1)
        tD.signature = 0
        ledger_1.append(tD)
        ledger_1.transactions[0].is_pending = False
        ledger_1.transactions[1].is_pending = False
        self.users[0].ledgers.append(ledger_1.deepcopy())
        print("\n")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())
        ledger_1.transactions.remove(ledger_1.transactions[-1])
        tE = Transaction(1, 2, 70, ledger_1)
        tE.signature = 0
        ledger_1.append(tE)
        ledger_1.transactions[2].is_pending = False
        print("In ledger: \n" + str(ledger_1))
        self.users[0].handle_new_ledger(ledger_1)
        print("----- Merging Ledger -----")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())

    def test_5(self):
        ledger_1 = self.ledger.deepcopy()
        tA = Transaction(1, 2, 30, ledger_1)
        tA.signature = 0
        ledger_1.append(tA)
        tB = Transaction(1, 2, 40, ledger_1)
        tB.signature = 0
        ledger_1.append(tB)
        tC = Transaction(1, 2, 50, ledger_1)
        tC.signature = 0
        ledger_1.append(tC)
        tD = Transaction(1, 2, 60, ledger_1)
        tD.signature = 0
        ledger_1.append(tD)
        ledger_1.transactions[0].is_pending = False
        ledger_1.transactions[1].is_pending = False
        self.users[0].ledgers.append(ledger_1.deepcopy())
        print("\n")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())
        ledger_1.transactions.remove(ledger_1.transactions[-1])
        print("In ledger: \n" + str(ledger_1))
        self.users[0].handle_new_ledger(ledger_1)
        print("----- Merging Ledger -----")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())

    def test_6(self):
        ledger_1 = self.ledger.deepcopy()
        tA = Transaction(1, 2, 30, ledger_1)
        tA.signature = 0
        ledger_1.append(tA)
        tB = Transaction(1, 2, 40, ledger_1)
        tB.signature = 0
        ledger_1.append(tB)
        tC = Transaction(1, 2, 50, ledger_1)
        tC.signature = 0
        ledger_1.append(tC)
        tD = Transaction(1, 2, 60, ledger_1)
        tD.signature = 0
        ledger_1.append(tD)
        ledger_1.transactions[0].is_pending = False
        ledger_1.transactions[1].is_pending = False
        self.users[0].ledgers.append(ledger_1.deepcopy())
        print("\n")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())
        ledger_1.transactions.remove(ledger_1.transactions[-1])
        ledger_1.transactions.remove(ledger_1.transactions[-1])
        tE = Transaction(1, 2, 50, ledger_1)
        tE.signature = 0
        ledger_1.append(tE)
        tF = Transaction(1, 2, 60, ledger_1)
        tF.signature = 0
        ledger_1.append(tF)
        ledger_1.transactions[2].is_pending = False
        print("In ledger: \n" + str(ledger_1))
        self.users[0].handle_new_ledger(ledger_1)
        print("----- Merging Ledger -----")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())

    def test_7(self):
        ledger_1 = self.ledger.deepcopy()
        tA = Transaction(1, 2, 30, ledger_1)
        tA.signature = 0
        ledger_1.append(tA)
        tB = Transaction(1, 2, 40, ledger_1)
        tB.signature = 0
        ledger_1.append(tB)
        tC = Transaction(1, 2, 50, ledger_1)
        tC.signature = 0
        ledger_1.append(tC)
        tD = Transaction(1, 2, 60, ledger_1)
        tD.signature = 0
        ledger_1.append(tD)
        ledger_1.transactions[0].is_pending = False
        ledger_1.transactions[1].is_pending = False
        self.users[0].ledgers.append(ledger_1.deepcopy())
        print("\n")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())
        ledger_1.transactions[1].is_pending = True
        print("In ledger: \n" + str(ledger_1))
        self.users[0].handle_new_ledger(ledger_1)
        print("----- Merging Ledger -----")
        print("Local ledger: \n" + self.users[0].get_ledgers_str())


class TestDelegate(unittest.TestCase):
    def setUp(self):
        # init users
        num_user = 5
        self.users = []
        for i in range(1, num_user + 1):
            self.users.append(User(i, [], 1000))

        # init ledger
        self.ledger = Ledger(
            [user.generate_digest() for user in self.users], [])

        for user in self.users:
            user.ledgers.append(self.ledger.deepcopy())

        # init network
        self.network = Network(100, 100, self.users)

    def test_delegate_score1(self):

        def tran(f, t, amt):
            self.users[f-1].add_transaction(t, amt)
            self.users[0].spread_ledgers(self.network)
            return
        # init transactions
        tran(1, 2, 100)
        tran(2, 4, 60)
        tran(5, 3, 70)
        tran(3, 2, 100)
        print(self.users[0].ledgers[0].toString())
        delegate = self.users[0].choose_delegate()
        print(delegate)
        print(type(delegate))
        self.assertTrue(len(delegate) == 1)
        self.assertTrue(delegate[0] == 2)

    def test_delegate_history(self):

        def tran(f, t, amt):
            self.users[f-1].add_transaction(t, amt)
            self.users[0].spread_ledgers(self.network)
            print(f"Transaction from {f} to {t}, amt: {amt}")
            return
        # init transactions

        delegates = [user.choose_delegate() for user in self.users]
        print(delegates)

        tran(1, 2, 60)
        tran(2, 4, 60)
        tran(5, 3, 70)
        tran(3, 2, 100)
        for i in range(5):
            time.sleep(0.05)
            delegates = [user.choose_delegate() for user in self.users]
            print(delegates)

        print(self.users[0].delegate_history)
        print(self.users[1].delegate_history)


class TestMultiThreadTransaction(unittest.TestCase):
    def setUp(self):
        # init users
        self.user_list = []
        for i in range(10):
            self.user_list.append(User(i + 1, [], 1000))

        # init ledger
        user_digest = []
        for user in self.user_list:
            user_digest.append(user.generate_digest())

        self.ledger = Ledger(
            user_digest, [])

        for user in self.user_list:
            user.ledgers.append(self.ledger.deepcopy())

        # init network
        self.network = Network(100, 100, self.user_list)

    def test_spread_ledger(self):
        # init transactions
        self.network.thread_pool.run_task_async(
            self.user_list[0].id, "add_transaction", 2, 100, is_write=True)
        self.network.thread_pool.run_task_async(
            self.user_list[1].id, "add_transaction", 3, 200, is_write=True)
        self.network.thread_pool.run_task_async(
            self.user_list[2].id, "add_transaction", 1, 300, is_write=True)

        # spread ledger
        self.network.thread_pool.run_task_async(
            self.user_list[0].id, "send_ledgers", self.network, [2, 3])
        self.network.thread_pool.run_task_async(
            self.user_list[1].id, "send_ledgers", self.network, [3, 1])
        self.network.thread_pool.run_task_async(
            self.user_list[2].id, "send_ledgers", self.network, [1, 2])

        self.network.thread_pool.threadpool.shutdown()

        self.assertTrue(len(self.user_list[0].ledgers)
                        == len(self.user_list[1].ledgers)
                        == len(self.user_list[2].ledgers)
                        == 1)

    def test_copy_on_write(self):
        self.network.thread_pool.run_task_async(
            self.user_list[0].id, "add_transaction", 2, 100, is_write=True)

        self.network.thread_pool.run_task_async(
            self.user_list[0].id, "send_ledgers", self.network, [2, 3])

        self.network.thread_pool.threadpool.shutdown()

        self.assertTrue(len(self.user_list[0].ledgers)
                        == len(self.user_list[1].ledgers)
                        == len(self.user_list[2].ledgers)
                        == 1)
