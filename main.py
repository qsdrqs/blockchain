#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file the main file of the project.

'''
from test import *
import simulation

if __name__ == '__main__':
    # run_all_tests()
    # run_specific_test_class(TestUtil)
    #run_specific_test_method(TestTransaction, 'test_verify')
    # run_specific_test_class(TestTransaction)
    # run_specific_test_class(TestNetwork)
    # run_specific_test_class(TestDelegate)
    # run_specific_test_method(TestDelegate, 'test_delegate_history')
    # run_specific_test_method(TestMerge, 'test_2')
    # run_specific_test_method(TestSameLedger, 'test_1')
    simulation.run()
