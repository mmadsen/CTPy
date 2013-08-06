#!/usr/bin/env python

# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.
"""
For a specific experiment name, we subsample raw data into a "full dataset".

Given a collection of individual samples, raw from a simuPOP/CTPy simulation, which have
been done at maximum levels of individual sample size and trait dimensionality, subsample
for smaller sample sizes and dimensionalities.

See http://notebook.madsenlab.org/coarse%20grained%20model%20project/2013/07/29/classification-experiment-protocol.html
for more details on this data reduction approach.

The resulting samples are copies of the original individual sample documents, but with a subset
of the original genotype (e.g., 3 loci instead of 4), or number of individuals (e.g., 30 individuals
sampled rather than 100).

The original sample document **and** each of the subsampled documents are inserted into
individual_sample_fulldataset.  This collection is then usable for further data reduction, such
as classification, time averaging, or other statistical analysis.

"""
import logging as log
import argparse
import ming
import ctpy
import ctpy.data as data
import ctpy.utils as utils
import datetime as datetime


## setup

def setup():
    global sargs, config
    sargs = utils.ScriptArgs()
    if sargs.debug:
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    else:
        log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    log.debug("experiment name: %s", sargs.experiment_name)
    data.set_experiment_name(sargs.experiment_name)
    data.set_database_hostname(sargs.database_hostname)
    data.set_database_port(sargs.database_port)
    #### main program ####
    log.info("SUBSAMPLE_INDIVIDUAL_SAMPLES - Starting program")
    log.info("Performing subsampling for experiment named: %s", data.experiment_name)
    config = data.getMingConfiguration()
    ming.configure(**config)


def check_prior_completion():
    """
    We do not want to run this subsampling if we've done it previously to the same raw
    data collection, because we'll be creating duplicate data sets.
    :return: boolean
    """
    experiment_record = data.ExperimentTracking.m.find(dict(experiment_name=sargs.experiment_name)).one()
    if experiment_record["subsampling_complete"] == True:
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
    experiment_record["subsampling_complete"] = True
    experiment_record["subsampling_tstamp"] = datetime.datetime.utcnow()
    experiment_record.m.save()



####### main loop #######

if __name__ == "__main__":
    setup()
    if check_prior_completion() == True:
        log.info("Subsampling of experiment %s already complete -- exiting", sargs.experiment_name)
        exit(1)

    # do the subsampling


    # log completion of the subsampling
    record_completion()


