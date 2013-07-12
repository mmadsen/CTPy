# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/

import logging




from richness_sample import sampleNumAlleles
from trait_count_sample import sampleTraitCounts
from individual_sample import sampleIndividuals
from simulation_data import storeSimulationData
from trait_lifetime import TraitLifetimeCacheIAModels
from trait_count_population import censusTraitCounts



# When a new module is added for sampling, the module's filename should be added to the module list below,
# and the module must support a _get_dataobj_id() method which returns the string used in the Ming ORM
# configuration for MongoDB.  This is defined in each module, and then used in the declarative definition
# of the data object being stored.  Ming configuration is then automatic so that simulation simulations need
# include only two lines which are fully generic.

modules = [individual_sample, trait_count_population, trait_count_sample, richness_sample, simulation_data, trait_lifetime]


def getMingConfiguration():
    config = {}
    urlstring = 'mongodb://localhost:27017/sim_raw_samples'
    for module in modules:
        key = ''
        key += 'ming.'
        key += module._get_dataobj_id()
        key += '.uri'
        config[key] = urlstring
    logging.debug(config)
    return config

__author__ = 'mark'
