#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Given a given a set of classification id's, run through the individual_sample database,
identifying all samples to all of the classifications (matching samples of dimensionality D
to classifications of the same dimensionality).  Insert the results into
individual_sample_classified.

Everything this worker does is independent, and thus multiple workers can run in parallel to
speed up processing.  The only caveat is that classification id's must only be given to
one worker, or duplicate records will occur.

"""

import ctpy.data as data
import ctpy # for constants
import ctpy.coarsegraining as cg
import ctpy.utils as utils
import ming
import logging as log
import pprint as pp
import argparse
import sys
from bson.objectid import ObjectId
import os
from subprocess import Popen
import datetime

# speed things up by caching mode definitions so we hit the DB a minimal number of times
mode_definition_cache = dict()
classification_dimension_cache = dict()

class_worker_script = "analytics/classify_individual_samples_worker.py"


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

    log.info("CLASSIFY_INDIVIDUAL_SAMPLES_WORKER - Starting program")
    config = data.getMingConfiguration()
    ming.configure(**config)

def batch(iterable, n = 1):
   l = len(iterable)
   for ndx in range(0, l, n):
       yield iterable[ndx:min(ndx+n, l)]


def record_completion():
    """
    Once subsampling is complete, we want to record it in the database so we don't do it
    again for the same data set.
    :return: none
    """
    experiment_record = data.ExperimentTracking.m.find(dict(experiment_name=sargs.experiment_name)).one()
    experiment_record["classification_complete"] = True
    experiment_record["classification_tstamp"] = datetime.datetime.utcnow()
    experiment_record.m.save()


### Main Loop ###

if __name__ == "__main__":
    setup()

    # get all classification ID's
    classification_id_list = []
    classifications = data.ClassificationData.m.find()
    for classification in classifications:
        classification_id_list.append(str(classification["_id"]))

    log.info("number of classifications: %s", len(classification_id_list))

    # set up path for child process execution
    wd = os.getcwd()
    sys.path.append(wd)

    # for b in batch(classification_id_list, 6):
    #     print b


    for classification_id in classification_id_list:
        args = []
        args.append(class_worker_script)
        args.append("--experiment ")
        args.append(sargs.experiment_name)
        args.append("--dbhost ")
        args.append(sargs.database_hostname)
        args.append("--dbport ")
        args.append(sargs.database_port)
        args.append("--classifications ")
        args.append(classification_id)
        args.append("--debug")
        args.append("1")

        log.debug("args: %s", args)
        retcode = os.system(" ".join(args))

    record_completion()