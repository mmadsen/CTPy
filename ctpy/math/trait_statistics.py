# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the Apache Public License 2.0
#
# This module contains classes and functions for applying paradigmatic classifications
# to the trait spaces of CTPy/simuPOP simulations.
#

import ctpy.data as data
from bson.objectid import ObjectId
import logging as log
from collections import defaultdict
import numpy as np
from diversity import diversity_iqv, diversity_shannon_entropy
import itertools


class TraitStatisticsPerSample:

    def __init__(self, simconfig, sample):
        self.simconfig = simconfig
        self.sample = sample



    def process_trait_statistics(self):
        """
        Given a sample in the fulldataset, we want to calculate the following:
        trait richness
        per locus for sample, mean trait richness per generation for sample,
        shannon entropy and iqv per locus for sample,
        mean shannon entropy and iqv per generation for sample.

        These statistics are saved to the database with sim run ID, replication, sample size,
        mutation rate, simulation time, and population size as keys.  With these keys,
        we can match them up to their post-classification counterparts.

        :return: no return value
        """
        s = self.sample
        log.debug("Starting analysis of sample")
        entropy_by_locus = []
        iqv_by_locus = []
        richness_by_locus = []
        trait_counts = {}

        # initialization
        for locus in range(0, s.dimensionality):
            trait_counts[locus] = defaultdict(int)

        # go through individuals in a single pass, counting all loci
        # we do this manually, because using numpy.bincount yields an array with zeros
        # for any slot which has no entries, which is a giant space given MAXALLELE
        for indiv in s.sample:
            for locus_num in range(0, s.dimensionality):
                trait_counts[locus_num][indiv.genotype[locus_num]] += 1

        log.debug("%s", trait_counts)

        for locus in range(0, s.dimensionality):
            richness_by_locus.append(len(trait_counts[locus]))
            trait_freq = [float(count)/float(s.sample_size) for trait_id, count in trait_counts[locus].items() ]
            entropy_by_locus.append(diversity_shannon_entropy(trait_freq))
            iqv_by_locus.append(diversity_iqv(trait_freq))


        mean_entropy = np.mean(np.array(entropy_by_locus))
        mean_iqv = np.mean(np.array(iqv_by_locus))
        mean_richness = np.mean(np.array(richness_by_locus))

        # store the result
        data.storePerGenerationStatsTraits(s.simulation_time,s.replication,s.sample_size,s.population_size,
                                           s.mutation_rate,s.dimensionality, s.simulation_run_id,mean_richness,mean_entropy,mean_iqv,
                                           richness_by_locus,entropy_by_locus,iqv_by_locus)