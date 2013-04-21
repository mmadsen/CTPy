"""
TraitCountSample is a declarative document schema for MongoDB storage of trait count samples, using
the Ming ORM library.


"""

from ming import Session, Field, schema
from ming.declarative import Document
import simuPOP as sim
from simuPOP.sampling import drawRandomSample
from pprint import pprint


# locus default sim.ALL_AVAIL
def sampleTraitCounts(pop, param):
    (ssize, mutation, popsize, sim_id,numloci) = param
    popID = pop.dvars().rep
    gen = pop.dvars().gen
    sample = drawRandomSample(pop, sizes=ssize)
    sim.stat(sample, alleleFreq=sim.ALL_AVAIL)
    for locus in range(numloci):
        alleleMap = sample.dvars().alleleNum[locus]
        for allele,count in alleleMap.iteritems():
            _storeTraitCountSample(popID, ssize, locus, gen, mutation, popsize, sim_id, allele, count)
    return True


def _storeTraitCountSample(popID, ssize, locus, generation, mutation, popsize, sim_id, allele, count):
    TraitCountSample(dict(
        simulation_time=generation,
        replication=popID,
        locus=locus,
        sample_size=ssize,
        population_size=popsize,
        mutation_rate=mutation,
        simulation_run_id=sim_id,
        allele=allele,
        count=count
    )).m.insert()
    return True



CountMap = dict(allele=int, count=float)

class TraitCountSample(Document):

    class __mongometa__:
        session = Session.by_name('traitcounts')
        name = 'trait_count_sample'

    _id = Field(schema.ObjectId)
    simulation_time = Field(int)
    replication = Field(int)
    locus = Field(int)
    sample_size = Field(int)
    population_size = Field(int)
    mutation_rate = Field(float)
    simulation_run_id = Field(str)
    allele = Field(int)
    count = Field(float)
