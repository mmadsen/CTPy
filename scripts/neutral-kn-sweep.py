# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

from __future__ import print_function
import simuOpt, sys
simuOpt.setOptions(alleleType='long',optimized=False,quiet=True)
import simuPOP as sim
import uuid
import ctpy.sampling as sampling
import ming
import itertools


"""
This program simulates the Wright-Fisher model of genetic drift with infinite-alleles mutation in a single
population, and counts the number of alleles present in the population and in samples of specified size.

This process is performed for each combination of key model parameters, and the results are saved to MongoDB.

"""

config = {'ming.richness.uri': 'mongodb://localhost:27017/richness_samples'}
ming.configure(**config)


# parameters intersected to form sample space
# mutationrates = [0.0001,0.0002,0.0005,0.00075,0.001,0.002,0.005,0.0075,0.01]
# samplesizes = [10,20,30,50,75,100,250,500]
# populationsizes = [500,1000,2000,5000,10000,25000,50000]

mutationrates = [0.0001,0.00075,0.001,0.01]
samplesizes = [10,50,250]
populationsizes = [500,1000,10000,20000]


state_space = [
    mutationrates,
    samplesizes,
    populationsizes
]


# other parameters
replications_per_paramset = 10
sampling_interval = 50
sim_length = 11000
time_start_stats = 1000
debug_output_interval = 5000
numloci = 1


for param_combination in itertools.product(*state_space):
    print(param_combination,end='\n')
    mut = param_combination[0]
    ssize = param_combination[1]
    popsize = param_combination[2]
    sim_id = uuid.uuid4().urn

    pop = sim.Population(size=popsize, ploidy=1, loci=numloci)
    simu = sim.Simulator(pop, rep=replications_per_paramset)

    simu.evolve(
        initOps = sim.InitGenotype(freq=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]),
        matingScheme = sim.RandomSelection(),
        postOps = [sim.KAlleleMutator(k=100000000, rates=mut),
               sim.Stat(alleleFreq=0, step=sampling_interval,begin=time_start_stats),
               #sim.PyEval(r"'%d, ' % gen", step=debug_output_interval,begin=time_start_stats,reps=0),
               sim.PyOperator(func=sampling.sampleNumAlleles, param=(ssize, mut, popsize, sim_id,numloci), step=sampling_interval,begin=time_start_stats),
               #sim.PyOutput('\n', reps=-1, step = debug_output_interval, begin=time_start_stats),
               ],
        gen = sim_length,
    )