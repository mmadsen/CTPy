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
import ctpy.utils as utils
import ming
import logging as log
import pprint as pp
import argparse
import sys
import os
from bson.objectid import ObjectId

# speed things up by caching mode definitions so we hit the DB a minimal number of times
mode_definition_cache = dict()
classification_dimension_cache = dict()
classification_list = []
global sargs

def setup():
    #log.debug("Executing in %s", os.getcwd())
    #log.debug("Arguments: %s", sys.argv)
    sargs = utils.ScriptArgs()

    if sargs.debug == 1:
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    else:
        log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    classification_list.extend(sargs.classification_list)

    #log.debug("experiment name: %s", sargs.experiment_name)
    data.set_experiment_name(sargs.experiment_name)
    data.set_database_hostname(sargs.database_hostname)
    data.set_database_port(sargs.database_port)

    log.info("CLASSIFY_INDIVIDUAL_SAMPLES_WORKER - Starting program")
    config = data.getMingConfiguration()
    ming.configure(**config)


def process_classification_ids():
    """
    Process list of classification id's from sys.argv - there should be only classification id's
    past argv[0].

    :return: list of classification dicts from the database
    """
    # classification_list = []
    # for i in range(1, len(sys.argv)):
    #     log.debug("%s", sys.argv[i])
    #     classification_list.append(sys.argv[i])

    clist = []
    for c in classification_list:
        clist.append(ObjectId(c))

    classifications = data.ClassificationData.m.find(dict(_id={'$in':clist})).all()
    #log.debug("%s", classifications)
    return classifications


def get_individual_cursor_for_dimensionality(dimensionality):
    sample_cursor = data.IndividualSampleFullDataset.m.find(dict(dimensionality=dimensionality))
    return sample_cursor


def get_and_cache_mode_definition(mode_id):
    if mode_id in mode_definition_cache:
        return mode_definition_cache[mode_id]
    else:
        mode_defn = data.ClassificationModeDefinitions.m.find(dict(_id=mode_id)).one()
        mode_definition_cache[mode_id] = mode_defn["boundary_map"]
        return mode_defn["boundary_map"]


def get_and_cache_dimensions_for_classification(class_id):
    if class_id in classification_dimension_cache:
        return classification_dimension_cache[class_id]
    else:
        classification = data.ClassificationData.m.find(dict(_id=class_id)).one()
        dimension_list = classification["modes_for_dimensions"]
        classification_dimension_cache[class_id] = dimension_list
        return dimension_list

def identify_genotype_to_class_for_classification(genotype,classification):
    """

    :param genotype:
    :param classification:
    :return:
    """
    mode_dimension_id_list = classification["modes_for_dimensions"]
    coarseness = classification["mean_coarseness"]

    identified_modes = []

    for dim_num in range(0, classification["dimensions"]):
        dimension_id = mode_dimension_id_list[dim_num]
        mode_boundaries = get_and_cache_mode_definition(dimension_id)
        trait_for_dim = genotype[dim_num]

        #log.debug("mode_boundaries: %s", mode_boundaries)

        for mode_num in range(0, coarseness):
            mode_defn = mode_boundaries[mode_num]
            lower = mode_defn["lower"]
            upper = mode_defn["upper"]
            if lower <= trait_for_dim < upper:
                identified_modes.append(mode_num)
                break

        # at the end of looping through the dimensions, we ought to have an ordered list of
    # which modes the alleles each identified to given the mode boundaries
    #log.debug("identified modes: %s", identified_modes)
    return '-'.join([`num` for num in identified_modes])

### Main Loop ###

if __name__ == "__main__":
    setup()
    classifications = process_classification_ids()
    for classification in classifications:
        class_id = classification["_id"]
        dimensionality = classification["dimensions"]
        coarseness = classification["mean_coarseness"]
        class_type = classification["classification_type"]

        #log.info("Processing samples for classification: %s", class_id)

        indiv_samples = get_individual_cursor_for_dimensionality(dimensionality)
        for s in indiv_samples:
            # each database sample records ssize individuals, so we loop through the "sample" list
            classified_indiv = []
            for sample in s.sample:
                identified_class = identify_genotype_to_class_for_classification(sample.genotype,classification)
                indiv = dict(id=sample.id,classid=identified_class)
                classified_indiv.append(indiv)

            data.storeIndividualSampleClassified(s.simulation_time,ObjectId(class_id),class_type,dimensionality,
                                                 coarseness,s.replication,s.sample_size,s.population_size,
                                                 s.mutation_rate, s.simulation_run_id, classified_indiv)



