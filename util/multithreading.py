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
        self.executor = {}  # use dict to store executor
        for entity in entities:
            self.executor[entity.id] = None

    def run_task_async(self, entity_id, entity_fun, * args, is_write=False, **kwargs):
        '''
        Add a task to the thread pool asynchronously.
        Return the future object which can get the result from `result()`.
        '''
        if self.executor[entity_id] is None or self.executor[entity_id].done():
            self.executor[entity_id] = self.threadpool.submit(
                entity_fun, *args, **kwargs)
        else:
            self.executor[entity_id].result()
            if is_write:
                self.executor[entity_id] = self.threadpool.submit(
                    entity_fun, *args, **kwargs)
            else:
                # entity is readable while writing
                copy = self.entities[entity_id].deepcopy()
                copy_executor = self.threadpool.submit(
                    entity_fun, *args, **kwargs)
                copy_executor.add_done_callback(
                    lambda future: self.entities[entity_id].update(copy))
        return self.executor[entity_id]
