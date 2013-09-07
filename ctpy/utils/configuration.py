# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/

import json

class CTPyConfiguration:
    MODETYPE_EVEN = str("EVEN")
    MODETYPE_RANDOM = str('RANDOM')

    ### Research-level constants

    MAXALLELES = 1000000000
    """
    simuPOP does infinite-allele models by giving a really large number to the KAllelesMutator,
    and ensuring that the combination of popsize * mutationrate * simlength doesn't exceed MAXALLELES
    This value is thus very important for defining classifications since it defines an integer-valued
    trait space.
    """

    NUM_REPLICATES_FOR_RANDOM_DIMENSION_MODES = 10
    """
    When creating random dimensions for classification, we want this many random choices
    of mode boundaries for each choice of mode count (e.g., 2 modes per dimension, 3 modes...)
    """

    DIMENSION_PARTITIONS = [2,3,4,8,16,32]
    """
    Classifications with 32 modes per dimension are rare in archaeological practice
    when classes are discrete/nominal categories, but we want to see scaling of
    observables, and we can imagine cases with random dimensions where we might
    have an ability to chop things into chunks but not understand how those map to underlying
    variation...
    """

    DIMENSIONS_STUDIED = [2,3,4,6,8]
    """
    We construct classifications by intersecting dimensions
    In the current implementation, we study classifications with
    the same number of dimensions as the underlying trait
    transmission dimensionality (num_loci).  But we need to study
    systems with differing values for num_loci, and thus classifications
    with the same number of dimensions
    """

    INNOVATION_RATES_STUDIED = [0.0001,0.00025,0.0005,0.001,0.0025,0.005,0.01,0.025]
    """
    We examine a range of innovation rates, from slow innovation rates that would imply one innovation
    every ten "generations" for a population of 1000 individuals, to rates which imply that at least
    10 individuals per generation in a population of 1000 will have a new idea.
    """

    SIMULATION_LENGTH_AFTER_STATIONARITY = 10000
    """
    We do not begin taking samples from the population until the Markov chain corresponding to the
    simulation is fully mixed (i.e., at quasi-stationary equilibrium).  That value is calculated based
    upon other simulation parameters.  The simulation continues to run for this many generations
    AFTER that stationarity time is reached.  This value should be adjusted for temporal
    aggregation studies to give you a sufficient number of samples for your longest TA duration
    window.  Making this a derived value from TA would be desirable.
    """

    TIME_AVERAGING_DURATIONS_STUDIED = [1000,500,250,125,63,32,16,8,1]
    """
    We want to be able to examine the effects of temporal aggregation AND classification, in addition
    to just classification.
    """



    INITIAL_TRAIT_NUMBER = 10
    """
    This constant sets the number of initial traits to which the population is initialized at time zero.
    Since we wait for the system to reach stationarity, this value matters only in that it slightly affects
    the difference between actual stationary mixing time, and the estimated average value.  I set it
    relatively low since the genetic approximations for mixing time usually work with a small number of
    alleles at a locus.
    """

    SAMPLING_INTERVAL = 1
    """
    Interval, in simulation ticks or generations, between samples of the population which are taken
    and stored in the database.  For testing and development, this is usually larger (e.g., 100).
    For production runs where we are not examining temporal aggregation, this value can also be
    larger. When examining temporal aggregation, we'll likely set this value to 1.
    """

    REPLICATIONS_PER_PARAM_SET = 10
    """
    For each combination of simulation parameters, CTPy and simuPOP will run this many replicate
    populations, saving samples identically for each, but initializing each replicate with a
    different population and random seed.
    """

    SAMPLE_SIZES_STUDIED = [25,50,100,200]
    """
    At each sampling interval, we take samples of the population and either calculate a statistic,
    or store the actual "genotype" values of sampled individuals in the database.  We want to do that
    for a number of different sample sizes, to determine how the various coarse-graining effects
    vary by sample size AND the underlying model.
    """

    POPULATION_SIZES_STUDIED = [500,1000,2500,5000]
    """
    In most of the CT models we study, the absolute amount of variation we might expect to see is
    partially a function of the number of individuals doing the transmitting.  This is *total* population
    size, either for a single population, or the metapopulation as a whole in a spatial model.
    """

    DEME_NUMBERS_STUDIED = [32]
    """
    For metapopulation models, we want to examine different configurations, but that is
    better accomplished via demic migration matrices.  We just need enough demes to make the
    connection model differences interesting.
    """

    NUMBER_RANDOM_MIGRATION_MATRICES_STUDIED = 10
    """
    This is the number of randomly generated migration matrices (i.e., weighted networks) per
    rewiring level and clustering coefficient we want to study
    """

    DENSITY_SMALL_WORLD_LINKS_STUDIED = [0.0,0.1,0.25,0.5,0.75]
    """
    This is the set of density levels for small world links we'll study.
    TODO:  needs tuning, look at Watts and look at node size and see what will actually work
    """

    CLUSTERING_COEFFICIENTS_STUDIED = [0.0,0.1,0.25,0.5,0.75]
    """
    This is the set of clustering coefficients for metapopulation networks we'll study.
    TODO:  needs tuning, look at how we'll generate networks with this amount of clustering first.
    """

    NUM_SAMPLES_ANALYZED_PER_FINAL_SAMPLE_PATH = 1
    """
    Each simulation parameter combination is analyzed with different sample sizes, dimensionality,
    classifications, and levels of time averaging.  At the maximum level of TA (1000?), with 10K
    raw steps in the simulation post-stationarity, we'll end up wtih 10 samples of the coarsest duration.
    We'll want to have the same number of samples at finer durations as well, even though we could have
    1250 samples of duration 8, or 10K samples of duration 1.

    This value ideally is *calculated* but I have to declare it and set a value here....
    """

    def __init__(self, config_file):
        # if we don't give a configuration file on the command line, then we
        # just return a Configuration object, which has the default values specified above.
        if config_file is None:
            return

        # otherwise, we load the config file and override the default values with anything in
        # the config file
        try:
            json_data = open(config_file)
            self.config = json.load(json_data)
        except ValueError:
            print "Problem parsing json configuration file - probably malformed syntax"
            exit(1)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            exit(1)

        # we succeeded in loading the configuration, now override the default values of variables
        # given the contents of the configuration file
        for variable,value in self.config.iteritems():
            setattr(self, variable, value)

        self._calc_derived_values()

        # now finalize any calculated or derived values


    def __repr__(self):
        attrs = vars(self)
        rep = '\n'.join("%s: %s" % item for item in attrs.items() if item[0] != "config")
        return rep

    def _calc_derived_values(self):
        """
        Each simulation parameter combination is analyzed with different sample sizes, dimensionality,
        classifications, and levels of time averaging.  At the maximum level of TA (1000?), with 10K
        raw steps in the simulation post-stationarity, we'll end up wtih 10 samples of the coarsest duration.
        We'll want to have the same number of samples at finer durations as well, even though we could have
        1250 samples of duration 8, or 10K samples of duration 1.
        """
        self.NUM_SAMPLES_ANALYZED_PER_FINAL_SAMPLE_PATH = int(self.SIMULATION_LENGTH_AFTER_STATIONARITY / self.SAMPLING_INTERVAL)
