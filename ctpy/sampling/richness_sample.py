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