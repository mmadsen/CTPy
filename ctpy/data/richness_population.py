"""
.. module:: richness_population
    :platform: Unix, Windows
    :synopsis: Data object for storing a census of trait richness from a population in MongoDB, via the Ming ORM.

.. moduleauthor:: Mark E. Madsen <mark@madsenlab.org>



    Aggregation framework query for calculating the mean richness for combinations of
    population size, mutation rate, and sample size, for comparison with formulas
    derived from Ewens sampling theory.

    db.richness_population.aggregate(
        { '$project' : {
            'population_size' : 1,
            'richness' : 1,
            'mutation_rate' : 1,
            'sample_size' : 1,
                    'locus' : 1,
        }},
        {
            '$group' : {
                '_id': { population: '$population_size', mutation_rate : '$mutation_rate', sample_size: '$sample_size', locus: '$locus'},
                'mean_richness' : { '$avg' : '$richness'},
            }
        })

"""


import logging as log
from ming import Session, Field, schema
from ming.declarative import Document
import simuPOP as sim
from simuPOP.sampling import drawRandomSample

def _get_dataobj_id():
    """
        Returns the short handle used for this data object in Ming configuration
    """
    return 'richness_pop'

def _get_collection_id():
    """
    :return: returns the collection name for this data object
    """
    return 'ctpy_sim_rawdata'


def censusNumAlleles(pop, param):
    """Samples allele richness for all loci in a replicant population, and stores the richness of the sample in the database.

        Args:

            pop (Population):  simuPOP population replicate.

            params (list):  list of parameters (sample size, mutation rate, population size, simulation ID)

        Returns:

            Boolean true:  all PyOperators need to return true.

    """
    (mutation, popsize,sim_id,numloci) = param
    popID = pop.dvars().rep
    gen = pop.dvars().gen
    sim.stat(pop, alleleFreq=sim.ALL_AVAIL)
    for locus in range(numloci):
        numAlleles = len(pop.dvars().alleleFreq[locus].values())
        _storeRichnessSample(popID,numAlleles,locus,gen,mutation,popsize,sim_id)
    return True


def _storeRichnessSample(popID, richness, locus, generation,mutation,popsize,sim_id):
    RichnessSample(dict(
        simulation_time=generation,
        replication=popID,
        locus=locus,
        richness=richness,
        population_size=popsize,
        mutation_rate=mutation,
        simulation_run_id=sim_id
    )).m.insert()
    return True




class RichnessSample(Document):

    class __mongometa__:
        session = Session.by_name(_get_dataobj_id())
        name = 'richness_population'

    _id = Field(schema.ObjectId)
    simulation_time = Field(int)
    replication = Field(int)
    locus = Field(int)
    richness = Field(int)
    population_size = Field(int)
    mutation_rate = Field(float)
    simulation_run_id = Field(str)