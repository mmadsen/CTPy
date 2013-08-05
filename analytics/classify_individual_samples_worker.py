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



def setup():
    sargs = utils.ScriptArgs()

    if sargs.debug:
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


def process_classification_ids():
    """
    Process list of classification id's from sys.argv - there should be only classification id's
    past argv[0].

    :return: list of classification dicts from the database
    """
    classification_list = []
    for i in range(1, len(sys.argv)):
        log.debug("%s", sys.argv[i])
        classification_list.append(sys.argv[i])

    clist = []
    for c in classification_list:
        clist.append(ObjectId(c))

    classifications = data.ClassificationData.m.find(dict(_id={'$in':clist})).all()
    log.debug("%s", classifications)
    return classifications


def get_individual_cursor_for_dimensionality(dimensionality):
    sample_cursor = data.IndividualSample.m.find(dict(dimensionality=dimensionality))
    return sample_cursor


def identify_genotype_to_class_for_classification(genotype,classification):
    """

    :param genotype:
    :param classification:
    :return:
    """
    pass



### Main Loop ###

if __name__ == "__main__":
    setup()
    classifications = process_classification_ids()
    for classification in classifications:
        dimensionality = classification["dimensions"]
        indiv_samples = get_individual_cursor_for_dimensionality(dimensionality)
        for s in indiv_samples:
            # each database sample records ssize individuals, so we loop through the "sample" list
            classified_indiv = []
            for sample in s.sample:

                identified_class = identify_genotype_to_class_for_classification(sample.genotype,classification)
                indiv = dict(id=sample.id,classid=identified_class)
                classified_indiv.append(indiv)

            data.storeIndividualSampleClassified()



