# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache License, Version 2.0.  See the file LICENSE for details
#

"""
construct_classifications.py

Initializes the database collections ClassificationModeDefinitions and ClassificationData.  This script
assumes that both collections (a) are empty of documents or (b) don't yet exist.

The initialization first constructs a series of EVEN dimension/mode definitions which can be used in many classifications, for a
variety of numbers of modes.

Second, the script constructs a set of random dimension/mode definitions, for each value of num_modes.

Third, we construct
"""

import logging as log
import random
# provides system-wide constants
import ctpy
import ctpy.data as data
import ctpy.coarsegraining as cg
import ming


## setup
log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')









#### main program ####

log.info("CONSTRUCT CLASSIFICATIONS - Starting program")


config = data.getMingConfiguration()
ming.configure(**config)


log.info("Constructing even partitions")

for nmodes in ctpy.DIMENSION_PARTITIONS:
    boundaries = cg.dmb.build_even_dimension(nmodes)
    data.storeClassificationModeDefinition(ctpy.MODETYPE_EVEN,ctpy.MAXALLELES,nmodes,boundaries)


log.info("Constructing random partitions: %s replicates per partition size", ctpy.NUM_REPLICATES_FOR_RANDOM_DIMENSION_MODES)


for nmodes in ctpy.DIMENSION_PARTITIONS:
    for i in range(0, ctpy.NUM_REPLICATES_FOR_RANDOM_DIMENSION_MODES):
        boundaries = cg.dmb.build_random_dimension(nmodes)
        data.storeClassificationModeDefinition(ctpy.MODETYPE_RANDOM, ctpy.MAXALLELES, nmodes, boundaries)


log.info("CONSTRUCT CLASSIFICATIONS - Completed")
