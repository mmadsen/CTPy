# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/
"""
.. module:: individual_sample_classified
    :platform: Unix, Windows
    :synopsis: Data object for storing a sample of N individuals (with genotype identified to a class) in MongoDB, via the Ming ORM.

.. moduleauthor:: Mark E. Madsen <mark@madsenlab.org>

"""

import logging
from ming import Session, Field, schema
from ming.declarative import Document
import simuPOP as sim
from simuPOP.sampling import drawRandomSample
import pprint as pp

def _get_dataobj_id():
    """
        Returns the short handle used for this data object in Ming configuration
    """
    return 'individuals_classified'




def storeIndividualSampleClassified(generation, replication, ssize, popsize, mutation, sim_id, sample_list):
    IndividualSampleClassified(dict(
        simulation_time=generation,
        replication=replication,
        sample_size=ssize,
        population_size=popsize,
        mutation_rate=mutation,
        simulation_run_id=sim_id,
        sample=sample_list
    )).m.insert()
    return True




class IndividualSampleClassified(Document):

    class __mongometa__:
        session = Session.by_name(_get_dataobj_id())
        name = 'individual_samples_classified'
        _id = Field(schema.ObjectId)
        simulation_time = Field(int)
        replication = Field(int)
        sample_size = Field(int)
        population_size = Field(int)
        mutation_rate = Field(float)
        simulation_run_id = Field(str)
        # a sample is a list of dicts, where each dict has an individual ID and a list of ints as a value
        sample = Field([
            dict(id=int, classid=int),
        ])