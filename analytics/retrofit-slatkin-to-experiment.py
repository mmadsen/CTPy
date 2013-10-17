#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

"""
Process the fulldataset for trait-level statistics.  This is independent of classify_individual_samples,
and neither affects the original data set.

"""

import logging as log
import argparse
import ctpy.data as data
import ctpy.utils as utils
import ctpy.coarsegraining as cg
import ctpy.math as m
import ming
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

if __name__ == "__main__":
    setup()




    # get a reference to the individual samples classified, make sure there's no timeout because it's big
    # and then iterate, calling the classification method to just do slatkin tests
    classified_sample_cursor = data.IndividualSampleClassified.m.find(dict(),dict(timeout=False))

    if(args.collections == 'postclassification' or args.collections == 'both'):
        for s in classified_sample_cursor:
            cg.update_with_slatkin_test(simconfig, s)

    if(args.collections == 'traits' or args.collections == 'both'):
        # get a reference to the individual sample fulldata set for traits, no timeout
        # iterate, calling trait_statistics to update slatkin
        trait_sample_cursor = data.IndividualSampleFullDataset.m.find(dict(),dict(timeout=False))

        for s in trait_sample_cursor:
            stat = m.TraitStatisticsPerSample(simconfig, s)
            stat.update_with_slatkin_test()



    # print a message saying that you should reexport any data sets....
    print "Retrofit complete -- you should re-export and post-process this experiment again to get the neutrality test columns"

