# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

from __future__ import print_function
import simuOpt, sys
simuOpt.setOptions(alleleType='long',optimized=False,quiet=True)
import simuPOP as sim
import uuid
import ctpy.sampling as sampling
import ctpy.utils as utils
import ctpy.math as cpm
import ming
import logging
import pprint as pp


"""
This program simulates the Wright-Fisher model of genetic drift with infinite-alleles mutation in a single
population, and counts the number of alleles present in the population and in samples of specified size
"""


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

config = sampling.getMingConfiguration()
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
        'label':'Length of simulation sample (in generations) after stationarity reached',
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
    },
    {
        'name' : 'numalleles',
        'default' : 10,
        'label' : 'Number of initial alleles in population',
        'type' : 'integer',
        'validator' : 'numalleles > 0'
    }

]



# get all parameters
pars = simuOpt.Params(options, doc='This program simulates the Wright-Fisher model of genetic drift with infinite-alleles mutation in a single population, and counts the number of alleles present in the population and in samples of specified size')
# cancelled
if not pars.getParam():
    sys.exit(1)





logging.info("Beginning simulation run: %s", sim_id)


beginCollectingData = cpm.expectedIAQuasiStationarityTimeHaploid(pars.popsize,pars.mutationrate)
logging.info("Starting data collection at generation: %s", beginCollectingData)

totalSimulationLength = beginCollectingData + pars.length
logging.info("Simulation will sample %s generations after stationarity", pars.length)




sampling.storeSimulationData(pars.popsize,pars.mutationrate,sim_id,pars.samplesize,pars.replications,pars.numloci,__file__,pars.numalleles)

initial_distribution = utils.constructUniformAllelicDistribution(pars.numalleles)
logging.info("Initial allelic distribution: %s", initial_distribution)

pop = sim.Population(size=pars.popsize, ploidy=1, loci=pars.numloci)
simu = sim.Simulator(pop, rep=pars.replications)

simu.evolve(
	initOps = sim.InitGenotype(freq=initial_distribution),
    preOps = [
        sim.PyOperator(func=utils.logGenerationCount, param=(), step=1000, reps=0),
    ],
	matingScheme = sim.RandomSelection(),
	postOps = [sim.KAlleleMutator(k=100000000, rates=pars.mutationrate, loci=sim.ALL_AVAIL),
        sim.PyOperator(func=sampling.sampleNumAlleles, param=(pars.samplesize, pars.mutationrate, pars.popsize,sim_id,pars.numloci), step=pars.stepsize,begin=beginCollectingData),
        sim.PyOperator(func=sampling.sampleTraitCounts, param=(pars.samplesize, pars.mutationrate, pars.popsize,sim_id,pars.numloci), step=pars.stepsize,begin=beginCollectingData),
        sim.PyOperator(func=sampling.censusTraitCounts, param=(pars.mutationrate, pars.popsize,sim_id,pars.numloci), step=pars.stepsize,begin=beginCollectingData),
        sim.PyOperator(func=sampling.sampleIndividuals, param=(pars.samplesize, pars.mutationrate, pars.popsize, sim_id), step=pars.stepsize, begin=beginCollectingData),
		],	
	gen = totalSimulationLength,
)

logging.info("Ending simulation run at generation %s", simu.population(0).dvars().gen)


