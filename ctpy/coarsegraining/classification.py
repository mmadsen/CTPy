# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the Apache Public License 2.0
#
# This module contains classes and functions for applying paradigmatic classifications
# to the trait spaces of CTPy/simuPOP simulations.
#

import ctpy.data as data
from bson.objectid import ObjectId
import ming
import logging as log
from collections import defaultdict


class ClassIdentifier:
    # speed things up by caching mode definitions so we hit the DB a minimal number of times
    mode_definition_cache = dict()
    classification_dimension_cache = dict()

    def __init__(self, simconfig, classification, save_identified_indiv=True):
        self.simconfig = simconfig
        self.classification = classification
        self.class_id = classification["_id"]
        self.dimensionality = classification["dimensions"]
        self.coarseness = classification["mean_coarseness"]
        self.class_type = classification["classification_type"]
        self.save_indiv = save_identified_indiv
        log.debug("initializing ClassIdentifier for classification %s", self.class_id)
        log.debug(">> Saving identified individuals, in addition to stats? %s", self.save_indiv)


    def identify_individual_samples(self):
        """
        Identify the individuals sampled from each generation of a simulation run to the appropriate class from the focal classification.

        Each "sample" is a record from one generation of one replication of one
        simulation run, at a given sample size and dimensionality.  Within each
        sample record is a list of sampled individual genotypes.  This list is
        what we iterate over to identify via the classification, and then we
        calculate various stats, and store the resulting stats.  If the flag for
        saving raw individuals (after classification identification) is set, we
        also store the list of individuals and the classes to which their genotypes identify.

        :return: None
        """

        records = self._get_individual_cursor_for_dimensionality(self.dimensionality)

        for s in records:
            classified_indiv = []
            mode_counts_by_dimension = {}
            class_richness = 0

            # these are caches, to be used in other methods
            global mode_counts_by_dimension, class_richness


            for indiv in s.sample:
                ident_class = self._identify_genotype_to_class_for_classification(indiv.genotype)
                ident_indiv = dict(id=indiv.id,classid=ident_class)
                classified_indiv.append(ident_indiv)

                class_richness += 1




                if self.save_indiv:
                    data.storeIndividualSampleClassified(s.simulation_time,ObjectId(self.class_id),self.class_type,self.dimensionality,
                                                        self.coarseness,s.replication,s.sample_size,s.population_size,
                                                        s.mutation_rate, s.simulation_run_id, classified_indiv)





    # private analytic methods








    # private methods
    def _get_individual_cursor_for_dimensionality(self, dimensionality):
        sample_cursor = data.IndividualSampleFullDataset.m.find(dict(dimensionality=dimensionality))
        return sample_cursor


    def _get_and_cache_mode_definition(self, mode_id):
        if mode_id in self.mode_definition_cache:
            return self.mode_definition_cache[mode_id]
        else:
            mode_defn = data.ClassificationModeDefinitions.m.find(dict(_id=mode_id)).one()
            self.mode_definition_cache[mode_id] = mode_defn["boundary_map"]
            return mode_defn["boundary_map"]


    def _get_and_cache_dimensions_for_classification(self, class_id):
        if class_id in self.classification_dimension_cache:
            return self.classification_dimension_cache[class_id]
        else:
            classification = data.ClassificationData.m.find(dict(_id=class_id)).one()
            dimension_list = classification["modes_for_dimensions"]
            self.classification_dimension_cache[class_id] = dimension_list
            return dimension_list


    def _identify_genotype_to_class_for_classification(self, genotype):
        """

        :param genotype:
        :return:
        """
        mode_dimension_id_list = self.classification["modes_for_dimensions"]

        identified_modes = []

        for dim_num in range(0, self.dimensionality):

            # initialize a cache
            mode_counts_by_dimension[dim_num] = defaultdict(int)

            dimension_id = mode_dimension_id_list[dim_num]
            mode_boundaries = self._get_and_cache_mode_definition(dimension_id)
            trait_for_dim = genotype[dim_num]

            # increment the cached trait count for stats
            mode_counts_by_dimension[dim_num][trait_for_dim] += 1

            #log.debug("mode_boundaries: %s", mode_boundaries)

            for mode_num in range(0, self.coarseness):
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