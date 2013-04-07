# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/

from __future__ import print_function
import simuOpt, os, sys, time
from pprint import pprint
simuOpt.setOptions(alleleType='long',optimized=False,quiet=True)
import simuPOP as sim
from simuPOP.sampling import drawRandomSample
from simuPOP.utils import *
from scipy import stats
import pandas as pd
import numpy as np
from pandas import DataFrame

"""
This program simulates the Wright-Fisher model of genetic drift with infinite-alleles mutation in a single
population, and counts the number of alleles present in the population and in samples of specified size
"""


replicatesAlleleNumber = {}

def sampleEwensNumAlleles(pop, param):
    (ssize) = param
    popID = pop.dvars().rep
    sample = drawRandomSample(pop, sizes=ssize)
    sim.stat(sample, alleleFreq=0)
    numAlleles = len(sample.dvars().alleleFreq[0].values())
    replicatesAlleleNumber[popID].append(numAlleles)
    print('%d' % numAlleles, end=', ')
    return True

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
        'type': 'numbers',
        'validator': 'mutationrate > 0.0',
    }

]







############# main program flow ####################


# get all parameters
pars = simuOpt.Params(options, doc='This program simulates the Wright-Fisher model of genetic drift with infinite-alleles mutation in a single population, and counts the number of alleles present in the population and in samples of specified size')
# cancelled
if not pars.getParam():
    sys.exit(1)


beginCollectingData = (3 * pars.stepsize)
for i in range(pars.replications):
    replicatesAlleleNumber[i] = []


pop = sim.Population(size=pars.popsize, ploidy=1, loci=1)
simu = sim.Simulator(pop, rep=pars.replications)

simu.evolve(
	initOps = sim.InitGenotype(freq=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]),
	matingScheme = sim.RandomSelection(),
	postOps = [sim.KAlleleMutator(k=100000000, rates=pars.mutationrate),
		sim.Stat(alleleFreq=0, step=pars.stepsize,begin=beginCollectingData),
		sim.PyEval(r"'%d, ' % gen", step=pars.stepsize,begin=beginCollectingData,reps=0),
		#sim.PyEval(r"', '.join(map(str,alleleFreq[0].values()))", step=stepsize),
        #sim.PyEval(r"'%d, ' % len(alleleFreq[0].values())", step=pars.stepsize,begin=beginCollectingData),
        sim.PyOperator(func=sampleEwensNumAlleles, param=(pars.samplesize), step=pars.stepsize,begin=beginCollectingData),
        sim.PyOutput('\n', reps=-1, step = pars.stepsize, begin=beginCollectingData),
		],	
	gen = pars.length,
)

# at this point, replicatesAlleleNumber is a dict containing a number of arrays, each for a replicate
# the pandas DataFrame can use that directly in a constructor.

df = DataFrame(replicatesAlleleNumber)
df.index.name = 'Generation'
df.columns.name = 'Population'

print(df.describe(),end='\n')











