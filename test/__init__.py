#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This is unit test module for the project.

'''
import unittest
from .transaction import TestTransaction
from .transaction import TestMultiThreadTransaction
from .util import TestUtil
from .transaction import TestDelegate
<<<<<<< HEAD
from .transaction import TestMerge
from .transaction import TestMerge2
=======
from .network import TestNetwork
>>>>>>> 007b254e1aff119c27d9de3098a239fb9753a8aa


def run_all_tests():
    '''
    Run all unit tests.
    '''
    unittest.main(verbosity=2)


def run_specific_test_class(class_name):
    '''
    Run a specific test class.
    '''
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(class_name))
    unittest.TextTestRunner(verbosity=2).run(suite)


def run_specific_test_method(class_name, method_name: str):
    '''
    Run a specific test method.
    '''
    suite = unittest.TestSuite()
    suite.addTest(class_name(method_name))
    unittest.TextTestRunner(verbosity=2).run(suite)
