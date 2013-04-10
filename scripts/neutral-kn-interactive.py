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


"""
This program simulates the Wright-Fisher model of genetic drift with infinite-alleles mutation in a single
population, and counts the number of alleles present in the population and in samples of specified size
"""



config = {'ming.richness.uri': 'mongodb://localhost:27017/richness_samples'}
ming.configure(**config)

sim_id = uuid.uuid4().urn

options = [
    {
        'name':'popsize',
        'default':1000,
        'label':'Population Size',
        'type': 'integer',
        'validator': 'popsize > 0',
    },
    {
        'name':'stepsize',
        'default':100,
        'label':'Interval Between Data Samples',
        'type': 'integer',
        'validator': 'stepsize > 0',
    },
    {
        'name':'length',
        'default':10000,
        'label':'Length of simulation (in generations)',
        'type': 'integer',
        'validator': 'length > 0',
    },
    {
        'name':'replications',
        'default':5,
        'label':'Number of populations to simulate in parallel',
        'type': 'integer',
        'validator': 'replications > 0',
    },
    {
        'name':'samplesize',
        'default':30,
        'label':'Size of sample to take each generation for allele counting',
        'type': 'integer',
        'validator': 'samplesize > 0',
    },
    {
        'name':'mutationrate',
        'default':0.001,
        'label':'Rate of individual innovations/mutations per generation',
        'type': 'number',
        'validator': 'mutationrate > 0.0',
    },
    {
        'name':'numloci',
        'default' : 2,
        'label' : 'Number of loci to model',
        'type' : 'integer',
        'validator' : 'numloci > 0',
    }

]



# get all parameters
pars = simuOpt.Params(options, doc='This program simulates the Wright-Fisher model of genetic drift with infinite-alleles mutation in a single population, and counts the number of alleles present in the population and in samples of specified size')
# cancelled
if not pars.getParam():
    sys.exit(1)


beginCollectingData = (3 * pars.stepsize)


pop = sim.Population(size=pars.popsize, ploidy=1, loci=pars.numloci)
simu = sim.Simulator(pop, rep=pars.replications)

simu.evolve(
	initOps = sim.InitGenotype(freq=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]),
	matingScheme = sim.RandomSelection(),
	postOps = [sim.KAlleleMutator(k=100000000, rates=pars.mutationrate),
		sim.Stat(alleleFreq=0, step=pars.stepsize,begin=beginCollectingData),
		sim.PyEval(r"'%d, ' % gen", step=pars.stepsize,begin=beginCollectingData,reps=0),
        sim.PyOperator(func=sampling.sampleNumAlleles, param=(pars.samplesize, pars.mutationrate, pars.popsize,sim_id,pars.numloci), step=pars.stepsize,begin=beginCollectingData),
        sim.PyOutput('\n', reps=-1, step = pars.stepsize, begin=beginCollectingData),
		],	
	gen = pars.length,
)





