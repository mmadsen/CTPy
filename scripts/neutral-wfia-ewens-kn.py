#!/opt/local/bin/python2.7

import simuOpt, os, sys, time
from pprint import pprint
simuOpt.setOptions(alleleType='long',optimized=False,quiet=True)
import simuPOP as sim
from simuPOP.sampling import drawRandomSample
from simuPOP.utils import *
from scipy import stats

sampleAlleleNumbers = []


def sampleEwensNumAlleles(pop, param):
    (ssize) = param
    sample = drawRandomSample(pop, sizes=ssize)
    sim.stat(sample, alleleFreq=0)
    numAlleles = len(sample.dvars().alleleFreq[0].values())
    sampleAlleleNumbers.append(numAlleles)
    print '%d' % numAlleles
    return True

stepsize = 100
length = 10000
samplesize = 30
beginCollectingData = (3 * stepsize)

pop = sim.Population(size=2000, ploidy=1, loci=1)

pop.evolve(
	initOps = sim.InitGenotype(freq=[0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]),
	matingScheme = sim.RandomSelection(),
	postOps = [sim.KAlleleMutator(k=100000000, rates=0.005),
		sim.Stat(alleleFreq=0, step=stepsize,begin=beginCollectingData),
		sim.PyEval(r"'%d, ' % gen", step=stepsize,begin=beginCollectingData),
		#sim.PyEval(r"', '.join(map(str,alleleFreq[0].values()))", step=stepsize),
        sim.PyEval(r"'%d, ' % len(alleleFreq[0].values())", step=stepsize,begin=beginCollectingData),
        sim.PyOperator(func=sampleEwensNumAlleles, param=(samplesize), step=stepsize,begin=beginCollectingData),
		],	
	gen = length,
)



mean = sum(sampleAlleleNumbers) / float(len(sampleAlleleNumbers))

print "mean number of alleles in sample of size %d: %.3f" % (samplesize, mean)


#print "Evolved generations: %d\n" % pop.dvars().gen
#print "Final Allele Frequencies: \n"
#sim.Stat(pop, alleleFreq=0)
#print ', '.join(map(str,pop.dvars().alleleFreq[0].values()))
#print "\n"





