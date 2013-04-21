# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/
import logging
from ming import Session, Field, schema
from ming.declarative import Document
import simuPOP as sim
from simuPOP.sampling import drawRandomSample

__author__ = 'mark'

def _get_dataobj_id():
    return 'simulations'



def storeSimulationData(popsize,mutation,sim_id,ssize,replicates,num_loci):
    SimulationRun(dict(
        replicates=replicates,
        population_size=popsize,
        mutation_rate=mutation,
        simulation_run_id=sim_id,
        sample_size=ssize,
        num_loci=num_loci
    )).m.insert()
    return True





class SimulationRun(Document):

    class __mongometa__:
        session = Session.by_name(_get_dataobj_id())
        name = 'simulation_runs'

    _id = Field(schema.ObjectId)
    replicates = Field(int)
    num_loci = Field(int)
    sample_size = Field(int)
    population_size = Field(int)
    mutation_rate = Field(float)
    simulation_run_id = Field(str)

