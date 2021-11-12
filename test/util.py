#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file is utility functions for test.

'''

from util import *
import unittest


class TestUtil(unittest.TestCase):
    def test_sign(self):
        key, public_key = generate_key_pair()
        message = b'Hello, world!'
        message = hash_message(message)
        signature = sign_message(key, message)
        self.assertTrue(verify_signature(public_key, signature, message))

    def test_sign_with_wrong_message(self):
        key, public_key = generate_key_pair()
        message = b'Hello, world!'
        message = hash_message(message)
        my_message = b'Hello, world'
        my_message = hash_message(my_message)
        signature = sign_message(key, message)
        self.assertFalse(verify_signature(public_key, signature, my_message))
