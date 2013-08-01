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

Third, we construct classifications as a combination of these dimensions, using the following algorithm:

1.  We construct classifications for all dimensions D listed in ctpy.DIMENSIONS_STUDIED.
2.  We construct even dimensions by combining D copies of each even dimension partition size (e.g., 2-modes, 3-modes).
3.  For each D, we construct ctpy.NUM_REPLICATES_FOR_RANDOM_DIMENSION_MODES classifications by selecting D random dimensions
    from the database of dimensions.
4.  This procedure results in ctpy.math.simulation_calculations.compute_total_classifications() pre-built classifications
    in the database.

At this time, I am not constructing classifications with different sized dimension/modes (e.g., a 3-mode and 2-mode classification).
Although this might be highly useful after first examining the equal sized partitions and random partitions.

"""

import logging as log
import random
# provides system-wide constants
import ctpy
import ctpy.data as data
import ctpy.coarsegraining as cg
import ctpy.math.simulation_calculations as sc
import ming


## setup
log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')



#### main program ####

log.info("CONSTRUCT CLASSIFICATIONS - Starting program")


config = data.getMingConfiguration()
ming.configure(**config)

log.info("Removing previous classification data from database")
data.ClassificationModeDefinitions.m.remove()
log.info("Records for dimension/modes: %s", data.ClassificationModeDefinitions.m.count())
data.ClassificationData.m.remove()
log.info("Records for classifications: %s", data.ClassificationData.m.count())





log.info("Constructing even partitions")

for nmodes in ctpy.DIMENSION_PARTITIONS:
    boundaries = cg.dmb.build_even_dimension(nmodes)
    data.storeClassificationModeDefinition(ctpy.MODETYPE_EVEN,ctpy.MAXALLELES,nmodes,boundaries)


log.info("Constructing random partitions: %s replicates per partition size", ctpy.NUM_REPLICATES_FOR_RANDOM_DIMENSION_MODES)


for nmodes in ctpy.DIMENSION_PARTITIONS:
    for i in range(0, ctpy.NUM_REPLICATES_FOR_RANDOM_DIMENSION_MODES):
        boundaries = cg.dmb.build_random_dimension(nmodes)
        data.storeClassificationModeDefinition(ctpy.MODETYPE_RANDOM, ctpy.MAXALLELES, nmodes, boundaries)


log.info("Constructing classifications for even dimensions")

for dim in ctpy.DIMENSIONS_STUDIED:
    log.debug("constructing classifications with even for dimensionality: %s", dim)
    for nmodes in ctpy.DIMENSION_PARTITIONS:
        #log.debug("constructing classifications for num_modes: %s", nmodes)
        query = dict(num_modes=nmodes, mode_type=ctpy.MODETYPE_EVEN)
        dimension_record = data.ClassificationModeDefinitions.m.find(query).one()
        dimensions = []
        # each of the classification dimensions uses the same partition in this case
        for i in range(0, dim):
            dimensions.append(dimension_record["_id"])

        #log.debug("classification modemap: %s", dimensions)
        data.storeClassificationData(ctpy.MODETYPE_EVEN,ctpy.MAXALLELES,dim,dimensions)


log.info("Constructing classifications for random dimensions")

for dim in ctpy.DIMENSIONS_STUDIED:
    log.debug("constructing classifications for random with dimensionality: %s", dim)
    for nmodes in ctpy.DIMENSION_PARTITIONS:
        for j in range(0, ctpy.NUM_REPLICATES_FOR_RANDOM_DIMENSION_MODES):
            #log.debug("constructing classifications for num_modes: %s", nmodes)
            query = dict(num_modes=nmodes, mode_type=ctpy.MODETYPE_RANDOM)
            dimension_list = data.ClassificationModeDefinitions.m.find(query).all()
            #log.debug("Num_mode: %s Num defns %s ", nmodes, len(dimension_list))
            dimensions = []
            for i in range(0, dim):
                rand_dimension = random.choice(dimension_list)
                dimensions.append(rand_dimension["_id"])
                #log.debug("classification modemap: %s", dimensions)
            data.storeClassificationData(ctpy.MODETYPE_RANDOM,ctpy.MAXALLELES,dim,dimensions)


log.info("Building %s classifications", sc.compute_total_classifications_across_dimensionality())

count = data.ClassificationData.m.count()
log.info("Constructed %s classifications and stored in database", count)


log.info("CONSTRUCT CLASSIFICATIONS - Completed")
