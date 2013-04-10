"""
RichnessSample is a declarative document schema for MongoDB storage of trait richness samples, using
the Ming ORM library.

Aggregation framework query for calculating the mean richness for combinations of
population size, mutation rate, and sample size, for comparison with formulas
derived from Ewens sampling theory.

db.richness_sample.aggregate(
	{ '$project' : {
		'population_size' : 1,
		'richness' : 1,
		'mutation_rate' : 1,
		'sample_size' : 1
	}},
	{
		'$group' : {
			'_id': { population: '$population_size', mutation_rate : '$mutation_rate', sample_size: '$sample_size'},
			'mean_richness' : { '$avg' : '$richness'},
		}
	})

"""



from ming import Session, Field, schema
from ming.declarative import Document
import simuPOP as sim
from simuPOP.sampling import drawRandomSample

def sampleNumAlleles(pop, param):
    (ssize, mutation, popsize,sim_id,numloci) = param
    popID = pop.dvars().rep
    gen = pop.dvars().gen
    sample = drawRandomSample(pop, sizes=ssize)
    sim.stat(sample, alleleFreq=sim.ALL_AVAIL)
    for locus in range(numloci):
        numAlleles = len(sample.dvars().alleleFreq[locus].values())
        _storeRichnessSample(popID,ssize,numAlleles,locus,gen,mutation,popsize,sim_id)
    return True


def _storeRichnessSample(popID, ssize, richness, locus, generation,mutation,popsize,sim_id):
    RichnessSample(dict(
        simulation_time=generation,
        replication=popID,
        locus=locus,
        richness=richness,
        sample_size=ssize,
        population_size=popsize,
        mutation_rate=mutation,
        simulation_run_id=sim_id
    )).m.insert()
    return True




class RichnessSample(Document):

    class __mongometa__:
        session = Session.by_name('richness')
        name = 'richness_sample'

    _id = Field(schema.ObjectId)
    simulation_time = Field(int)
    replication = Field(int)
    locus = Field(int)
    richness = Field(int)
    sample_size = Field(int)
    population_size = Field(int)
    mutation_rate = Field(float)
    simulation_run_id = Field(str)