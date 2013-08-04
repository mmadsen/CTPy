# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

from __future__ import print_function
import simuOpt, sys
simuOpt.setOptions(alleleType='long',optimized=False,quiet=True)
import simuPOP as sim
import uuid
import ctpy.data as data
import ctpy.utils as utils
import ctpy.math as cpm
import ctpy
import ming
import itertools
import logging as log


"""
This program simulates the Wright-Fisher model of genetic drift with infinite-alleles mutation in a single
population, and counts the number of alleles present in the population and in samples of specified size.

This process is performed for each combination of key model parameters, and the results are saved to MongoDB.

"""

log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

config = data.getMingConfiguration()
ming.configure(**config)

sim_id = uuid.uuid4().urn


# parameters intersected to form sample space
# mutationrates = [0.0001,0.0002,0.0005,0.00075,0.001,0.002,0.005,0.0075,0.01]
# samplesizes = [10,20,30,50,75,100,250,500]
# populationsizes = [500,1000,2000,5000,10000,25000,50000]

mutationrates = ctpy.INNOVATION_RATES_STUDIED
populationsizes = ctpy.POPULATION_SIZES_STUDIED


state_space = [
    mutationrates,
    populationsizes
]


# other parameters
sample_size = max(ctpy.SAMPLE_SIZES_STUDIED)
replications_per_paramset = ctpy.REPLICATIONS_PER_PARAM_SET
sampling_interval = ctpy.SAMPLING_INTERVAL
sim_length = ctpy.SIMULATION_LENGTH_AFTER_STATIONARITY
numloci = max(ctpy.DIMENSIONS_STUDIED)
gen_logging_interval = sim_length / 5
numalleles = ctpy.INITIAL_TRAIT_NUMBER




initial_distribution = utils.constructUniformAllelicDistribution(numalleles)
log.info("Initial allelic distribution: %s", initial_distribution)



for param_combination in itertools.product(*state_space):
    sim_id = uuid.uuid4().urn
    log.info("Beginning run: %s params: %s", sim_id, param_combination)
    mut = param_combination[0]
    popsize = param_combination[1]

    data.storeSimulationData(
        popsize,mut,sim_id,sample_size,replications_per_paramset,numloci,__file__,numalleles,ctpy.MAXALLELES)

    time_start_stats = cpm.expectedIAQuasiStationarityTimeHaploid(popsize,mut)
    log.info("...Starting data collection at generation: %s", time_start_stats)

    totalSimulationLength = time_start_stats + sim_length
    log.info("...Simulation will sample %s generations after stationarity", sim_length)

    pop = sim.Population(size=popsize, ploidy=1, loci=numloci)
    simu = sim.Simulator(pop, rep=replications_per_paramset)

    simu.evolve(
        initOps = sim.InitGenotype(freq=initial_distribution),
        preOps = [
            sim.PyOperator(func=utils.logGenerationCount, param=(), step=gen_logging_interval, reps=0),
        ],
        matingScheme = sim.RandomSelection(),
        postOps = [sim.KAlleleMutator(k=ctpy.MAXALLELES, rates=mut),
                    sim.PyOperator(func=data.sampleNumAlleles, param=(sample_size, mut, popsize,sim_id,numloci), step=sampling_interval,begin=time_start_stats),
                    sim.PyOperator(func=data.sampleTraitCounts, param=(sample_size, mut, popsize,sim_id,numloci), step=sampling_interval,begin=time_start_stats),
                    sim.PyOperator(func=data.censusTraitCounts, param=(mut, popsize,sim_id,numloci), step=sampling_interval,begin=time_start_stats),
                    sim.PyOperator(func=data.censusNumAlleles, param=(mut, popsize,sim_id,numloci), step=sampling_interval,begin=time_start_stats),
                    sim.PyOperator(func=data.sampleIndividuals, param=(sample_size, mut, popsize, sim_id,numloci), step=sampling_interval, begin=time_start_stats),
               ],
        gen = totalSimulationLength,
    )
    log.info("End run %s at generation %s", sim_id, simu.population(0).dvars().gen)