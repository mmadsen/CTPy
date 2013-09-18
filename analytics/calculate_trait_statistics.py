#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Process the fulldataset for trait-level statistics.  This is independent of classify_individual_samples,
and neither affects the original data set.

"""

import ctpy.data as data
import ctpy.coarsegraining as cg
import ctpy.math as m
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

    log.info("CALCULATE_TRAIT_STATISTICS - Starting program")
    config = data.getMingConfiguration()
    ming.configure(**config)

def check_prior_completion():
    """
    We do not want to run this subsampling if we've done it previously to the same raw
    data collection, because we'll be creating duplicate data sets.
    :return: boolean
    """
    experiment_record = data.ExperimentTracking.m.find(dict(experiment_name=sargs.experiment_name)).one()
    if experiment_record["trait_statistics_complete"] == True:
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
    experiment_record["trait_statistics_complete"] = True
    experiment_record["trait_statistics_tstamp"] = datetime.datetime.utcnow()
    experiment_record.m.save()


if __name__ == "__main__":
    setup()
    if check_prior_completion() == True:
        log.info("Trait statistics of experiment %s already complete -- exiting", sargs.experiment_name)
        exit(1)

    # Result set for the fulldataset, with no cursor timeout in case it's very large
    sample_cursor = data.IndividualSampleFullDataset.m.find(dict(),dict(timeout=False))


    for sample in sample_cursor:
        stat = m.TraitStatisticsPerSample(simconfig, sample)
        stat.process_trait_statistics()

    record_completion()