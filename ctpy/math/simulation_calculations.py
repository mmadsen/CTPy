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


def compute_total_simulation_runs():
    """
    The number of simulation runs (i.e., execution runs) is the product of the number
    of simulation parameter combinations and the number of network realizations against
    which we want to test.  Note that each execution run can generate multiple independent
    replicates of those parameters in simuPOP, so this is NOT the number of independent data
    sample streams.

    :return: number of total simulation execution runs
    """
    return compute_sim_param_combinations() * compute_total_network_realizations()

def compute_total_simulation_replicates():
    """
    The number of simulation replicates is the number of simulation execution runs,
    times the number of replications we ask simuPOP to do for every parameter combination
    and network realization (i.e., configuration).

    :return: number of total simulation replicates across all parameter and network combinations
    """
    return compute_total_simulation_runs() * ctpy.REPLICATIONS_PER_PARAM_SET

