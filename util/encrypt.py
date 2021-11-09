#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file handles everything about encryption and decryption.
Such as creating the key pairs, make signatures on transactions with private keys, and verify signatures.

'''
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast

def generate_key_pair():
    '''
    Generate a key pair for the user.
    '''
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)
    public_key = key.publickey()
    return key, public_key

def verify_signature(public_key, signature, message):
    '''
    Verify the signature of a message.
    '''
    return public_key.verify(message, signature)
