# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the Apache Public License 2.0
#
# This module contains classes and functions for applying paradigmatic classifications
# to the trait spaces of CTPy/simuPOP simulations.
#

import ctpy.data as data
import ctpy.math as m
from bson.objectid import ObjectId
import logging as log
from collections import defaultdict
import numpy as np


class ClassificationStatsPerSimrun:


    def __init__(self, simconfig):
        self.simconfig = simconfig
        self.simrun_param_cache = None
        self.param_cached = False


    def process_simulation_run(self, simrun_id):
        """
        Process the individual samples for a single simulation run, calculating any statistics that
        require aggregation over the simulation run, saving the results to the database.  This requires
        that we process each "replication" separately, so that we do not mix them together.

        :return:
        """
        #log.debug("Starting analysis of simulation run %s", simrun_id)

        for replication in range(0,self.simconfig.REPLICATIONS_PER_PARAM_SET):
            records = self._get_samples_for_simulation_run(simrun_id, replication)
            if len(records) < 1:
                log.info("No samples in the database for simulation run: %s", simrun_id)
                return
            else:
                log.info("Samples found for simulation run: %s", simrun_id)



            class_time_cache = {}

            # classification info


            for s in records:
                #log.debug("starting analysis of record")
                #log.debug("record: %s", s)

                # Only do this once - keep one of the records around so we can snag parameters from it later,
                # outside the processing loop
                if self.param_cached is False:
                    self.simrun_param_cache = s
                    self.param_cached = True



                gen = s.simulation_time

                for indiv in s.sample:
                    class_id = indiv.classid

                    # if we find an instance of the class showing up earlier than the cached time, record the earlier time
                    if class_id not in class_time_cache:
                        class_time_cache[class_id] = gen
                    else:
                        if class_time_cache[class_id] > gen:
                            class_time_cache[class_id] = gen

            # the cache now contains the earliest time of appearance of all classes in the simulation run
            #log.debug("cache: %s", class_time_cache)
            class_time_appeared = [dict(classid=k,time=v) for k,v in class_time_cache.items()]
            #log.debug("%s", class_time_appeared)

            # calculate other stats...
            stats = self._innovation_interval_stats(class_time_cache)


            # save the results
            s = self.simrun_param_cache
            data.storePerSimrunStatsPostclassification(s.classification_id,s.classification_type,s.classification_dim,
                                                       s.classification_coarseness,s.replication,s.sample_size,
                                                       s.population_size,s.mutation_rate,s.simulation_run_id,class_time_appeared,
                                                       stats[0],stats[1])





    def _get_samples_for_simulation_run(self, simrun_id, replication):
        """

        :return:
        """
        return data.IndividualSampleClassified.m.find(dict(simulation_run_id=simrun_id,replication=replication))


    def _innovation_interval_stats(self,cache):
        """
        Takes a dict of class_id and generation of first appearance, and calculates the
        intervals between class appearances
        :return:  tuple of mean, sd
        """
        sorted_times = np.array(sorted(cache.values()))
        #log.debug("sorted times: %s", sorted_times)
        intervals = np.diff(sorted_times)
        #log.debug("intervals: %s", intervals)
        mean = np.mean(intervals)
        # ddof = 1 is required to give the standard statistical definition, with n-1 in the denominator
        sd = np.std(intervals, ddof=1)
        #log.debug("mean: %s  sd: %s", mean, sd)
        return (mean,sd)




class ClassificationStatsPerSample:
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
        self.classification_size = self._calc_num_classes()

        #log.debug("initializing ClassIdentifier for classification %s", self.class_id)
        #log.debug("    Saving identified individuals, in addition to stats? %s", self.save_indiv)


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
        log.info("Starting identification of individuals to classification %s", self.class_id)
        records = self._get_individual_cursor_for_dimensionality(self.dimensionality)

        #log.debug("record length: %s", len(records))

        for s in records:
            log.debug("Starting analysis of record")
            classified_indiv = []
            mode_counts_by_dimension = {}
            class_counts = defaultdict(int)


            for dim_num in range(0, self.dimensionality):
                # initialize a cache
                mode_counts_by_dimension[dim_num] = defaultdict(int)

            # these are caches, to be used in other methods
            global mode_counts_by_dimension, class_counts


            for indiv in s.sample:
                ident_class = self._identify_genotype_to_class(indiv.genotype)
                ident_indiv = dict(id=indiv.id,classid=ident_class)
                #log.debug("identified to class: %s", ident_class)
                classified_indiv.append(ident_indiv)

                class_counts[ident_class] += 1



            class_freq = [float(count)/float(s.sample_size) for class_id, count in class_counts.items() ]
            shannon_entropy = m.diversity_shannon_entropy(class_freq)
            class_iqv = m.diversity_iqv(class_freq)

            #log.debug("class freq: %s  shannon entropy: %s   iqv: %s", class_freq, shannon_entropy, class_iqv)
            stats = self._calc_postclassification_stats(s)
            #log.debug("class richness %s", len(class_counts))
            data.storePerGenerationStatsPostclassification(s.simulation_time,ObjectId(self.class_id),self.class_type,self.dimensionality,
                                                        self.coarseness,self.classification_size,s.replication,s.sample_size,s.population_size,s.mutation_rate,
                                                        s.simulation_run_id,stats["mode_richness_list"],stats["class_richness"],
                                                        stats["mode_iqv"],stats["mode_entropy"],class_iqv,shannon_entropy,stats["design_space_occupation"],None)

            if self.save_indiv:
                    data.storeIndividualSampleClassified(s.simulation_time,ObjectId(self.class_id),self.class_type,self.dimensionality,
                                                        self.coarseness,s.replication,s.sample_size,s.population_size,
                                                        s.mutation_rate, s.simulation_run_id, classified_indiv)





    # private analytic methods


    def _calc_postclassification_stats(self,s):
        mode_richness_list = []
        mode_evenness_iqv_list = []
        mode_evenness_entropy_list = []

        for dim, dim_dict in sorted(mode_counts_by_dimension.items()):
            mode_richness_list.append(len(dim_dict))
            mode_freq = [float(count)/float(s.sample_size) for dim, count in dim_dict.items()]
            mode_evenness_iqv_list.append(m.diversity_iqv(mode_freq))
            mode_evenness_entropy_list.append(m.diversity_shannon_entropy(mode_freq))

        log.debug("mode_richness_list %s", mode_richness_list )
        results = {}
        results["mode_richness_list"] = mode_richness_list
        results["class_richness"] = len(class_counts)
        results["design_space_occupation"] = float(len(class_counts)) / float(self.classification_size)
        results["mode_iqv"] = mode_evenness_iqv_list
        results["mode_entropy"] = mode_evenness_entropy_list

        return results

    def _calc_num_classes(self):
        # given that each dimension has the same coarseness, of course....
        return self.coarseness ** self.dimensionality



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


    def _identify_genotype_to_class(self, genotype):
        """

        :param genotype:
        :return:
        """
        mode_dimension_id_list = self.classification["modes_for_dimensions"]

        identified_modes = []

        for dim_num in range(0, self.dimensionality):
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