#!/usr/bin/env python

# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.
"""
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


## setup
log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument("--experiment", help="provide name for experiment, to be used as prefix for database collections")
args = parser.parse_args()
if args.experiment:
    log.debug("experiment name: %s", args.experiment)
    data.set_experiment_name(args.experiment)

#### main program ####
log.info("SUBSAMPLE_INDIVIDUAL_SAMPLES - Starting program")
config = data.getMingConfiguration()
ming.configure(**config)

