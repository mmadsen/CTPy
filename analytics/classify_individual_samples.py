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
import datetime as datetime


def setup():
    global sargs, config, simconfig
    sargs = utils.ScriptArgs()

    if sargs.debug == 1:
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    else:
        log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    simconfig = utils.CTPyConfiguration(sargs.configuration)

    log.debug("experiment name: %s", sargs.experiment_name)
    data.set_experiment_name(sargs.experiment_name)
    data.set_database_hostname(sargs.database_hostname)
    data.set_database_port(sargs.database_port)

    log.info("CLASSIFY_INDIVIDUAL_SAMPLES_PARALLEL - Starting program")
    config = data.getMingConfiguration()
    ming.configure(**config)

def check_prior_completion():
    """
    We do not want to run this subsampling if we've done it previously to the same raw
    data collection, because we'll be creating duplicate data sets.
    :return: boolean
    """
    experiment_record = data.ExperimentTracking.m.find(dict(experiment_name=sargs.experiment_name)).one()
    if experiment_record["classification_complete"] == True:
        return True
    else:
        return False

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


if __name__ == "__main__":
    setup()
    if check_prior_completion() == True:
        log.info("Classification identification of experiment %s already complete -- exiting", sargs.experiment_name)
        exit(1)

    # get all classification ID's
    classification_id_list = []
    # The runtime on this cursor might be extremely long, and we don't want the server timing out, so snag all the data at once.
    classifications = data.ClassificationData.m.find().all()


    for classification in classifications:
        classifier = cg.ClassificationStatsPerSample(simconfig, classification, save_identified_indiv=True)
        classifier.identify_individual_samples()

    record_completion()