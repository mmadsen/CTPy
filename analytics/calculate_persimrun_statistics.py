#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Iterates over individual simulation runs, instead of just taking jumbled samples from the database,
and calculating any statistics that need to be aggregated over a whole simulation run, recording it in the database.

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

    log.info("CALCULATE_PERSIMRUN_STATISTICS - Starting program")
    config = data.getMingConfiguration()
    ming.configure(**config)




if __name__ == "__main__":
    setup()

    # get all simulation run id's
    res = data.SimulationRun.m.find(dict(),dict(simulation_run_id=1)).all()




    simruns = set([run.simulation_run_id for run in [x for x in res ]])
    #log.debug("%s", simruns)
    log.info("Processing %s simulation runs for experiment: %s", len(simruns), sargs.experiment_name)
    stats_processor = cg.ClassificationStatsPerSimrun(simconfig)
    for run_id in simruns:
        stats_processor.process_simulation_run(run_id)
