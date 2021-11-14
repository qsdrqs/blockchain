#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Copyright (C) 2021

Authors: Tianyang Zhou <t7zhou@ucsd.edu>
         Weifan Ou <w3ou@ucsd.edu>
         Xuanxi Du <xud015@ucsd.edu>

This file contains multi-threading helper functions.
Implemented by thread pool library.

'''
from concurrent.futures import ThreadPoolExecutor
import time


class ThreadPool:
    '''
    Thread pool helper class.
    We need to make sure that every entity in the pool can work asynchronously.
    But make sure that every entity in the pool should only do one task at a time.

    We use Read-Write lock to make sure that one entity can only do one work at a time.
    We use Copy-on-Write(CoW) to avoid dead locks.
    '''

    def __init__(self, entities: list):
        '''
        Initialize the thread pool.
        The thread pool will help every entities to work in parallel.
        '''
        self.threadpool = ThreadPoolExecutor(max_workers=len(entities))
        self.entities = {}
        for entity in entities:
            self.entities[entity.id] = entity
        # signal
        self.signal = {}  # use dict to store signals
        for entity in entities:
            self.signal[entity.id] = 0

    def run_task_async(self, entity_id, entity_fun: str, * args, is_write=False, **kwargs):
        '''
        Add a task to the thread pool asynchronously.
        Return the future object which can get the result from `result()`.

        No write on reading
        No write on writing
        Permit read on reading
        Permit read on writing (CoW)add_done_callback
        '''
        if self.signal[entity_id] < 0:
            raise Exception(
                'FATAL: signal value of {} is less than zero!'.format(entity_id))

        # get entity function
        if hasattr(self.entities[entity_id], entity_fun):
            reflection = getattr(self.entities[entity_id], entity_fun)
        else:
            raise Exception('Entity {} does not have function {}'.format(
                self.entities[entity_id].__str__(), entity_fun))

        if is_write:
            # check the lock
            while self.signal[entity_id] > 0:
                # The entity is not vacant.
                # Wait until the entity is vacant.
                time.sleep(0.1)

            def cow_helper(self, entity_id, copy):
                self.entities[entity_id].update(copy)
                self.signal[entity_id] -= 1
                print(self.signal[entity_id])

                # copy on write
            self.signal[entity_id] += 1  # add signal
            print(str(entity_id) + ":" + str(self.signal[entity_id]))
            copy = self.entities[entity_id].deepcopy()
            copy_reflection = getattr(copy, entity_fun)
            executor = self.threadpool.submit(
                copy_reflection, *args, **kwargs)
            executor.add_done_callback(
                lambda future: cow_helper(self, entity_id, copy))
            return executor

        else:
            def read_helper(self):
                self.signal[entity_id] -= 1
                print(self.signal[entity_id])

            self.signal[entity_id] += 1  # add signal
            print(str(entity_id) + ":" + str(self.signal[entity_id]))
            executor = self.threadpool.submit(
                reflection, *args, **kwargs)
            executor.add_done_callback(
                lambda future: read_helper(self))
            return executor
