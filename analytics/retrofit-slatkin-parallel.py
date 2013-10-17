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
    parser.add_argument("--collections", choices=['postclassification', 'traits', 'both'], help="Collections to retrofit ", required=True)

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

    if(args.collections == 'traits' or args.collections == 'both'):
        tqueue = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()
        create_processes(tqueue, results, traits_worker)
        queue_trait_jobs()
        try:
            tqueue.join()
        except KeyboardInterrupt:
            log.info("trait processing interrupted by ctrl-c")
            for proc in process_list:
                proc.terminate()
            exit(1)

    process_list = []

    if(args.collections == 'postclassification' or args.collections == 'both'):
        pcqueue = multiprocessing.JoinableQueue()
        create_processes(pcqueue, results, postclassification_worker)
        queue_postclassification_jobs()
        try:
            pcqueue.join()
        except KeyboardInterrupt:
            log.info("postclassification processing interrupted by ctrl-c")
            for proc in process_list:
                proc.terminate()
            exit(1)

    log.info("collection processing complete")


def create_processes(queue, results_queue, worker):
    for i in range(0, int(args.parallelism)):
        process = multiprocessing.Process(target=worker, args=(queue, simconfig, args))
        process.daemon = True
        process_list.append(process)
        process.start()


def queue_trait_jobs():

    trait_sample_cursor = data.IndividualSampleFullDataset.m.find(dict(),dict(timeout=False))
    for sample in trait_sample_cursor:
        tqueue.put(sample)


def queue_postclassification_jobs():

    classified_sample_cursor = data.IndividualSampleClassified.m.find(dict(),dict(timeout=False))
    for sample in classified_sample_cursor:
        pcqueue.put(sample)


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


if __name__ == "__main__":
    setup()
    main()