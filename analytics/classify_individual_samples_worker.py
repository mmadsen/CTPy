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
import ming
import logging as log
import pprint as pp
import argparse
import sys
from bson.objectid import ObjectId

log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

config = data.getMingConfiguration()
ming.configure(**config)




# Process the list of classification id's from the command line
# There should be no other arguments beyond the script path at sys.argv[0]

classification_list = []


for i in range(1, len(sys.argv)):
    log.debug("%s", sys.argv[i])
    classification_list.append(sys.argv[i])

clist = []
for c in classification_list:
    clist.append(ObjectId(c))

classifications = data.ClassificationData.m.find(dict(_id={'$in':clist})).all()

log.debug("%s", classifications)

num_loci_values = []
for classification in classifications:



### Main Loop ###





sample_cursor = data.IndividualSample.m.find().all()
for classification in classifications:
    dimensionality = classification["dimensions"]
    for s in sample_cursor:
        # each database sample records ssize individuals, so we loop through those
        classified_indiv = []
        for sample in s.sample:

            identified_class = identify_genotype_to_class_for_classification(sample.genotype,classification)
            indiv = dict(id=sample.id,classid=identified_class)
            classified_indiv.append(indiv)

        data.storeIndividualSampleClassified()



