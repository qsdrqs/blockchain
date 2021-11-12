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
from Crypto.Signature import pkcs1_15
from Crypto import Random
from Crypto.Hash import SHA256


def generate_key_pair():
    '''
    Generate a key pair for the user.
    '''
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)
    public_key = key.publickey()
    return key, public_key


def sign_message(private_key, message):
    '''
    Sign a message with the private key.
    '''
    return pkcs1_15.new(private_key).sign(message)


def verify_signature(public_key, signature, message):
    '''
    Verify the signature of a message.
    '''
    try:
        pkcs1_15.new(public_key).verify(message, signature)
        return True
    except (ValueError, TypeError):
        return False


def hash_message(message):
    '''
    Hash a message.
    '''
    return SHA256.new(message)
