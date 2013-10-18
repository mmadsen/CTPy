#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Process the fulldataset and postclassification data sets for Slatkin exact tests.  Use multiprocessing for
parallelism, because this takes a LONG time to run (even with compound indices) on 10MM data points.

"""

import logging as log
import ming
import argparse
import ctpy.data as data
import ctpy.utils as utils
import ctpy.coarsegraining as cg
import ctpy.math as m
import multiprocessing
import os
import sys
import time



def setup():
    global args, simconfig
    permitted_stage_tags = data.get_experiment_stage_tags()

    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", help="provide name for experiment", required=True)
    parser.add_argument("--debug", help="turn on debugging output")
    parser.add_argument("--dbhost", help="database hostname, defaults to localhost", default="localhost")
    parser.add_argument("--dbport", help="database port, defaults to 27017", default="27017")
    parser.add_argument("--configuration", help="Configuration file for experiment", required=True)
    parser.add_argument("--parallelism", help="Number of concurrent processes to run", default="4")
    parser.add_argument("--collection", choices=['postclassification', 'traits'], help="Collection to retrofit ", required=True)

    args = parser.parse_args()

    simconfig = utils.CTPyConfiguration(args.configuration)

    if args.debug:
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    else:
        log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    log.debug("experiment name: %s", args.experiment)
    data.set_experiment_name(args.experiment)
    data.set_database_hostname(args.dbhost)
    data.set_database_port(args.dbport)
    config = data.getMingConfiguration()
    ming.configure(**config)




def main():
    global tqueue, pcqueue, process_list
    process_list = []


    if(args.collection == 'traits'):
        log.info("Processing trait collection for Slatkin retrofit")
        tqueue = multiprocessing.JoinableQueue()
        trait_sample_cursor = data.IndividualSampleFullDataset.m.find(dict(),dict(timeout=False))
        create_queueing_process(tqueue, trait_sample_cursor, queue_worker)
        # to avoid a race condition where the workers start up and find the queue empty, we wait a bit
        time.sleep(5)
        create_processes(tqueue, traits_worker)
        try:
            tqueue.join()
        except KeyboardInterrupt:
            log.info("trait processing interrupted by ctrl-c")
            for proc in process_list:
                proc.terminate()
            exit(1)

    elif(args.collection == 'postclassification'):
        pcqueue = multiprocessing.JoinableQueue()
        classified_sample_cursor = data.IndividualSampleClassified.m.find(dict(),dict(timeout=False))
        create_queueing_process(pcqueue, classified_sample_cursor, queue_worker)
        # to avoid a race condition where the workers start up and find the queue empty, we wait a bit
        time.sleep(5)
        create_processes(pcqueue, postclassification_worker)
        try:
            pcqueue.join()
        except KeyboardInterrupt:
            log.info("postclassification processing interrupted by ctrl-c")
            for proc in process_list:
                proc.terminate()
            exit(1)

    else:
        log.error("Collection argument not recognized")

    log.info("collection processing complete")


def create_queueing_process(queue, cursor, worker):
    process = multiprocessing.Process(target=worker, args=(queue, cursor, simconfig, args))
    process.daemon = True
    process_list.append(process)
    process.start()

def create_processes(queue, worker):
    for i in range(0, int(args.parallelism)):
        process = multiprocessing.Process(target=worker, args=(queue, simconfig, args))
        process.daemon = True
        process_list.append(process)
        process.start()




def postclassification_worker(queue, simconfig, args):
    completed_count = 0
    while True:
        try:
            sample = queue.get()
            cg.update_with_slatkin_test(simconfig, sample)
            completed_count += 1

            if(completed_count % 1000 == 0):
                log.info("postclassification worker %s: completed %s samples", os.getpid(), completed_count )

        finally:
            queue.task_done()


def traits_worker(queue, simconfig, args):
    completed_count = 0
    while True:
        try:
            sample = queue.get()
            stat = m.TraitStatisticsPerSample(simconfig, sample)
            stat.update_with_slatkin_test()
            completed_count += 1

            if(completed_count % 100 == 0):
                log.info("trait worker %s: completed %s samples", os.getpid(), completed_count )

        finally:
            queue.task_done()


def queue_worker(queue, cursor, simconfig, args):
    """
    Worker routine which will queue database records in batches, so that we can process
    data that will not fit in RAM.


    :param queue:
    :param cursor:
    :param simconfig:
    :param args:
    :return:
    """
    BATCH_SIZE = 500
    completed_count = 0
    total_records = cursor.count()
    log.info("queue worker: total records to process: %s", total_records)

    # For large data collections, we'll work 100K at a time for a batch, which shouldn't exceed 1-2 GB of RAM
    # for the queue.
    if(total_records > 1000000):
        BATCH_SIZE = 100000
    while True:
        # we can't check queue size on OS X given what multiprocessing calls a "broken" semaphore
        # implementation, so for dev and test purposes, we do it cruftily
        try:
            if(sys.platform == 'darwin'):
                log.info("queue worker: queuing %s records using OS X timing approximation", BATCH_SIZE)
                for i in range(0, BATCH_SIZE):
                    queue.put(cursor.next())
                if(BATCH_SIZE == 500):
                    time.sleep(5)
                else:
                    time.sleep(60)
            else:
                if(queue.qsize() < BATCH_SIZE):
                    log.info("queue worker: queuing %s records by watching queue size", BATCH_SIZE)
                    for i in range(0, BATCH_SIZE):
                        queue.put(cursor.next())
                time.sleep(5)
        except StopIteration:
            log.info("queue worker: final records queued")
            break








if __name__ == "__main__":
    setup()
    main()