# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/

"""
.. module:: simulation_calculations
    :platform: Unix, Windows
    :synopsis: Functions to help calculate metrics for planning and executing CTPy simulations.

.. moduleauthor:: Mark E. Madsen <mark@madsenlab.org>

"""

import ctpy

########## Common Values #############

def compute_sim_param_combinations():
    """
    The number of simulation parameter combinations can probably be reduced to the
    Cartesian product of innovation rates and overall population sizes.  The number
    of trait dimensions can -- IF simuPOP evolves each locus independently in terms of
    mutations -- be a post-processing step.  All "raw" simulation runs would occur with
    the highest number of dimensions studied (say, 8), and then to study a smaller number of
    dimensions (say, 2), we'd simply extract two dimensions from the raw dataset.

    :return: number of simuPOP parameter combinations to test
    """
    innov_param = len(ctpy.INNOVATION_RATES_STUDIED)
    pop_param = len(ctpy.POPULATION_SIZES_STUDIED)
    return innov_param * pop_param



######### Classification Combinations #############

def compute_even_dimension_classifications():
    """
    For each dimensionality, we will have one classification per level of mode
    partitioning (i.e., a classification which chops dimensions into 2 modes, one
    which chops dimensions into 4 modes, etc).
    TODO:  We might also want classifications which are even, but different levels of partitioning for different dimensions...?
    :return: number of classifications with even dimensions
    """
    return len(ctpy.DIMENSION_PARTITIONS)

def compute_random_dimension_classifications():
    """
    For each dimensionality, we have R classifications per level of mode partitioning M.  For each
    of the R classifications, the M modes have random boundaries chosen uniformly.
    TODO:  We might want classifications which have different levels of M per dimension, but random mode boundaries....?
    :return: number of classifications with M mode partitions, given R randomly generated partitions per value of M
    """
    return ctpy.NUM_REPLICATES_FOR_RANDOM_DIMENSION_MODES * len(ctpy.DIMENSION_PARTITIONS)

def compute_total_classifications():
    """
    Since dimensionality is a property of subsampling the simulation output into separate
    data samples, any given data sample stream has a specific dimensionality (and other
    configuration parameters).  We want, then, to identify the sample stream through each
    of the even and random classifications we pre-define.
    :return: number of total even and random classifications
    """
    return compute_even_dimension_classifications() + compute_random_dimension_classifications()



######### Single Population Models (Simple Models) ############

def compute_total_simulation_runs_simple():
    """
    For single population models, the number of simulation runs is just the number
    of simulation parameter combinations, so this is a pass through.
    :return: number of simulation runs for a single population model
    """
    return compute_sim_param_combinations()


def compute_total_simulation_replicates_simple():
    """
    For single population models, the number of simulation replicates is just the number of
    simulation parameter combinations times the number of simuPOP replicates.
    :return: number of simulation replicates for a single population model
    """
    return compute_total_simulation_runs_simple() * ctpy.REPLICATIONS_PER_PARAM_SET

def compute_total_sample_size_replicates_simple():
    """
    For each simulation replicate in each run, we're also taking a variety of sample sizes of
    individuals for recording aggregate statistics and capturing genotypes for classification.
    This increases the total number of sample "streams" by a factor.
    :return: number of simulation replicates for each sample size factor
    """
    return compute_total_simulation_replicates_simple() * len(ctpy.SAMPLE_SIZES_STUDIED)

def compute_total_replicates_ssize_dimensionality():
    """
    From the raw sim runs, we also study different dimensionality by subsampling.  This leads
    to genotype and statistics which are distinct for each level of dimensionality, at each
    sample size, FOR each combination of simulation parameters, by the number of replicates at
    each sim param combination...

    :return: number of replicates at each dimensionality and sample size and param combo, given replication level
    """
    return compute_total_sample_size_replicates_simple() * len(ctpy.DIMENSIONS_STUDIED)


def compute_total_replicates_ssize_dimensionality_classifications():
    """
    If we identify every replicate (given level of dimensionality, sample size, and combination
    of simulation parameters) with every even and random classification applicable to the given
    level of dimensionality, we end up with this many separate data stream samples.
    :return: number of data sample streams given classification, dimensionality, ssize, sim params
    """
    return compute_total_replicates_ssize_dimensionality() * compute_total_classifications()


def compute_total_sample_paths_ssize_dim_class_taduration():
    """
    If we aggregate raw sample paths at a variety of durations, and classify the results in
    addition to the raw unaggregated samples paths, this is the number of total sample paths
    that results.
    :return: number of data sample streams given class, dim, ssize, simparam, taduration
    """
    return compute_total_replicates_ssize_dimensionality_classifications() * len(ctpy.TIME_AVERAGING_DURATIONS_STUDIED)


def compute_total_number_samples_simple_models():
    """
    The total number of "samples" (sets of observations at a given level of ssize, dim, class,
    TA duration, simparams, replicated N times).
    :return: number of sets of distinct observations including replication at each "combination" of treatments
    """
    return ctpy.NUM_SAMPLES_ANALYZED_PER_FINAL_SAMPLE_PATH * compute_total_sample_paths_ssize_dim_class_taduration()


def compute_total_number_samples_notimeavg_simple_models():
    """
    For analyses with just raw samples, and no time averaging, this is the number of "samples"
    (sets of observations at a given level of ssize, dim, class, simparams, replicated N times).
    :return: number of sets of distinct observations including replication at each "combination" of treatments, without any time averaging
    """
    return compute_total_replicates_ssize_dimensionality_classifications() * ctpy.NUM_SAMPLES_ANALYZED_PER_FINAL_SAMPLE_PATH



################# metapopulation models #####################


def compute_network_param_combinations():
    """
    The number of network model parameter combinations is important because for each
    combination, we will then test a number of random realizations, and each random
    realization will be run at all simulation parameter combinations.  This value is
    currently the product of the levels of clustering coefficient and small-world
    rewiring probability that we're testing.

    :return: number of network parameter combinations to test
    """
    density_params = len(ctpy.DENSITY_SMALL_WORLD_LINKS_STUDIED)
    clust_params = len(ctpy.CLUSTERING_COEFFICIENTS_STUDIED)
    return  density_params * clust_params

def compute_total_network_realizations():
    """
    The number of network realizations is the number of network parameter combinations times
    the number of replicates we'll study per parameter combination.

    :return: number of network realizations to test
    """
    return compute_network_param_combinations() * ctpy.NUMBER_RANDOM_MIGRATION_MATRICES_STUDIED




def compute_total_simulation_runs_metapopulation():
    """
    Applicable to metapopulation models with networks of demes.  The number of simulation runs (i.e., execution runs) is the product of the number
    of simulation parameter combinations and the number of network realizations against
    which we want to test.  Note that each execution run can generate multiple independent
    replicates of those parameters in simuPOP, so this is NOT the number of independent data
    sample streams.

    :return: number of total simulation execution runs
    """
    return compute_sim_param_combinations() * compute_total_network_realizations()

def compute_total_simulation_replicates_metapopulation():
    """
    Applicable to metapopulation models with networks of demes.  The number of simulation replicates is the number of simulation execution runs,
    times the number of replications we ask simuPOP to do for every parameter combination
    and network realization (i.e., configuration).

    :return: number of total simulation replicates across all parameter and network combinations
    """
    return compute_total_simulation_runs_metapopulation() * ctpy.REPLICATIONS_PER_PARAM_SET

def compute_replicates_ssize_dimensionality_metapop():
    """

    :return:
    """
    return compute_total_simulation_replicates_metapopulation() * len(ctpy.SAMPLE_SIZES_STUDIED) * len(ctpy.DIMENSIONS_STUDIED)

def compute_replicates_ssize_dim_classified_metapop():
    """

    :return:
    """
    return compute_replicates_ssize_dimensionality_metapop() * compute_total_classifications()

def compute_replicates_ssize_dim_classified_timeaveraged():
    """

    :return:
    """
    return compute_replicates_ssize_dim_classified_metapop() * len(ctpy.TIME_AVERAGING_DURATIONS_STUDIED)
