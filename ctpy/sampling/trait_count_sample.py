"""
TraitCountSample is a declarative document schema for MongoDB storage of trait count samples, using
the Ming ORM library.


"""

from ming import Session, Field, schema
from ming.declarative import Document
import simuPOP as sim
from simuPOP.sampling import drawRandomSample


# locus default sim.ALL_AVAIL
def sampleTraitCounts(pop, param):
    (ssize, mutation, popsize, sim_id,numloci) = param
    popID = pop.dvars().rep
    gen = pop.dvars().gen
    sample = drawRandomSample(pop, size=ssize)
    sim.stat(sample, alleleNum=sim.ALL_AVAIL)
    for locus in range(numloci):
        _storeTraitCountSample(popID, ssize, locus, gen, mutation, popsize, sim_id, sample.dvars().alleleNum[locus].values())
    return True


def _storeTraitCountSample(popID, ssize, locus, generation, mutation, popsize, sim_id, count_list):
    TraitCountSample(dict(
        # fields
    )).m.insert()
    return True






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
    # something for the array of trait counts
