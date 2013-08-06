#!/usr/bin/env python

# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

import logging as log
import ctpy.utils as utils
import ctpy.data as data
import ming
import datetime


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
    log.info("INITIALIZE_EXPERIMENT - Starting program")
    config = data.getMingConfiguration()
    ming.configure(**config)


def check_experiment_exists():
    num_entries = data.ExperimentTracking.m.find(dict(experiment_name=sargs.experiment_name)).count()
    if num_entries != 0:
        log.info("Experiment name: %s already exists in database %s, please choose another and re-run this program", sargs.experiment_name, sargs.database_hostname)
        exit(1)



####### main loop #######

if __name__ == "__main__":
    setup()

    # check if that experiment name already exists
    check_experiment_exists()

    # construct initial ExperimentTracking object and save to database
    data.initializeExperimentRecord(sargs.experiment_name,datetime.datetime.utcnow())

    log.info("Experiment %s initialized in database %s", sargs.experiment_name, sargs.database_hostname)