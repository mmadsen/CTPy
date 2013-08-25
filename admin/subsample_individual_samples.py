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
import ctpy.data as data
import ctpy.utils as utils
import datetime as datetime
import itertools


## setup

def setup():
    global sargs, config, simconfig
    sargs = utils.ScriptArgs()
    if sargs.debug:
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    else:
        log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    simconfig = utils.CTPyConfiguration(sargs.configuration)

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


def record_full_subsample(s,new_dimen,new_ssize,new_sample):
    data.storeIndividualSampleFullDataset(s.replication,
                                          new_dimen,
                                          new_ssize,
                                          s.simulation_time,
                                          s.mutation_rate,
                                          s.population_size,
                                          s.simulation_run_id,
                                          new_sample
                                          )

def subsample_for_dimension(dimension, sample_id, genotype_list):
    """
    Takes a list of genotypes and the desired number of loci to subsample, and returns
    that number of loci from the list
    :param dimension:
    :param genotype_list:
    :return: list of genotypes
    """
    return dict(id=sample_id,genotype=genotype_list[:dimension])



####### main loop #######

if __name__ == "__main__":
    setup()
    if check_prior_completion() == True:
        log.info("Subsampling of experiment %s already complete -- exiting", sargs.experiment_name)
        exit(1)

    # do the subsampling
    # one caveat is that we already have a sample from max(DIMENSIONS_STUDIED) and
    # max(SAMPLE_SIZES_STUDIED) so we need to skip doing that one, and just insert the
    # original data sample into the fulldataset collection.
    existing_dimensionality = max(simconfig.DIMENSIONS_STUDIED)
    existing_sample_size = max(simconfig.SAMPLE_SIZES_STUDIED)

    state_space = [
        simconfig.SAMPLE_SIZES_STUDIED,
        simconfig.DIMENSIONS_STUDIED
    ]


    individual_samples =  data.IndividualSample.m.find()
    # each "individual_sample" has a field called "sample" which is an array of individuals's genotypes
    for s in individual_samples:
        for param_combination in itertools.product(*state_space):
            ssize = param_combination[0]
            dimen = param_combination[1]

            log.debug("subsampling for ssize %s and dim %s", ssize, dimen)

            # this is the original sample document
            if ssize == existing_sample_size and dimen == existing_dimensionality:
                # record original document into the full sample data set
                log.debug("Skipping subsampling for documents with existing ssize and dim, just copying")
                record_full_subsample(s,s.dimensionality,s.sample_size,s.sample)
                continue

            # we subsample each id in the samples array, and then construct a new overall
            # "individual_sample_fulldataset" document from the original "individual_sample"
            # document, inserting "subsampled_indiv" in place of the original list.
            dim_subsampled = []

            for sample in s.sample:

                dim_subsampled.append(subsample_for_dimension(dimen, sample.id, sample.genotype))

            log.debug("dim_subsampled: %s", dim_subsampled)

            # now dim_subsampled contains the dimension-reduced samples, so we just have
            # to reduce it by ssize, and the result is our completely subsampled sample.
            final_subsample = dim_subsampled[:ssize]
            log.debug("final subsample: %s", final_subsample)

            record_full_subsample(s,dimen,ssize,final_subsample)

    # log completion of the subsampling
    record_completion()


