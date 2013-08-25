#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Given a given a set of classification id's, run through the individual_sample database,
identifying all samples to all of the classifications (matching samples of dimensionality D
to classifications of the same dimensionality).  Insert the results into
individual_sample_classified.

Uses workerpool to create a number of parallel threads to speed processing

"""

import ctpy.data as data
import ctpy.coarsegraining as cg
import ctpy.utils as utils
import ming
import logging as log
import pprint as pp
import argparse
import sys
from bson.objectid import ObjectId
import os
import workerpool



def setup():
    sargs = utils.ScriptArgs()
    global sargs

    if sargs.debug == 1:
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    else:
        log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    log.debug("experiment name: %s", sargs.experiment_name)
    data.set_experiment_name(sargs.experiment_name)
    data.set_database_hostname(sargs.database_hostname)
    data.set_database_port(sargs.database_port)

    log.info("CLASSIFY_INDIVIDUAL_SAMPLES_PARALLEL - Starting program")
    config = data.getMingConfiguration()
    ming.configure(**config)




if __name__ == "__main__":
    setup()
    pool = workerpool.WorkerPool(size=sargs.parallelization)

    # get all classification ID's
    classification_id_list = []
    classifications = data.ClassificationData.m.find()


    log.info("number of classifications: %s", len(classifications))

    for classification in classifications:
        classifier = cg.ClassIdentifier(classification)


    pool.shutdown()
    pool.wait()
