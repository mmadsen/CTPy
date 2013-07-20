# Copyright (c) 2013  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

#
#
#
#

import ctpy.data as data
import ctpy.coarsegraining as cg
import ming
import logging
import pprint as pp

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

config = data.getMingConfiguration()
ming.configure(**config)

simrun_param_cache = dict()
simrun_dimension_cache = dict()


def identify_genotype_to_class(genotype, sim_param):
    sim_id = sim_param["simid"]
    numloci = sim_param["numloci"]
    dimensions = simrun_dimension_cache[sim_id]

    identified_modes = []

    for dim_num in range(0, numloci):
        allele = genotype[dim_num]
        modes = dimensions[dim_num].keys()
        for mode in modes:
            lower = dimensions[dim_num][mode]["lower"]
            upper = dimensions[dim_num][mode]["upper"]
            if lower <= allele < upper:
                identified_modes.append(mode)
                break

    # at the end of looping through the dimensions, we ought to have an ordered list of
    # which modes the alleles each identified to given the mode boundaries
    return '-'.join([`num` for num in identified_modes])



# This function is temporary - will be factored out into a set of objects which produce
# the mode boundaries for a given classification.  So that the main script can just get a list
# of classifications to use, and then use all of this logic as-is, perhaps in parallel.

# TODO:  Module which produces random mode boundaries from TF, given a specific number of modes
# TODO:  Module which produces even mode boundaries, given a specific number of modes
# TODO:  Modules should use unit interval partitions, and then chop maxalleles with it.

def map_partition_to_boundaries(maxalleles,numdimensions):
    dimensions = {}

    # to start, we partition into quarters for each locus (dimension)
    num_modes = 4
    mode_width = maxalleles / 4.0

    for dimension in range(0, numdimensions):
        mode_boundaries_dict = {}
        lower_val = 0.0
        upper_val = 0.0
        for mode in range(0,num_modes):
            upper_val += mode_width
            mode_boundaries_dict[mode] = dict(lower=lower_val, upper=upper_val)
            lower_val = upper_val
            dimensions[dimension] = mode_boundaries_dict
    return dimensions




def construct_dimension_boundaries(sim_id, sim_param):
    if sim_id not in simrun_dimension_cache:
        simrun_dimension_cache[sim_id] = map_partition_to_boundaries(sim_param["maxalleles"], sim_param["numloci"])

def lookup_sim_run_parameters(sim_id):
    sim_param = dict()
    if sim_id in simrun_param_cache:
       return simrun_param_cache[sim_id]
    else:
        query = dict(simulation_run_id=sim_id)
        simrun_record = data.SimulationRun.m.find(query).one()
        sim_param["numloci"] = simrun_record.num_loci
        sim_param["maxalleles"] = simrun_record.max_alleles
        sim_param["simid"] = sim_id

        logging.debug("sim run %s: numloci: %s  maxalleles: %s", sim_id, sim_param["numloci"], sim_param["maxalleles"])
        simrun_param_cache[sim_id] = sim_param

        return sim_param



#### main program ####


samples = data.IndividualSample.m.find().all()

for s in samples:
    classified_list = []
    sim_time = s["simulation_time"]
    replication = s["replication"]
    ssize = s["sample_size"]
    popsize = s["population_size"]
    mut = s["mutation_rate"]
    simid = s["simulation_run_id"]

    # for the sim run, get numloci and maxalleles
    sim_param = lookup_sim_run_parameters(simid)

    # if we need to, construct dimension boundaries for this sim run and cache
    construct_dimension_boundaries(simid,sim_param)


    for sample in s.sample:
        identified_class = identify_genotype_to_class(sample.genotype,sim_param)
        indiv = dict(id=sample.id,classid=identified_class)
        classified_list.append(indiv)

    data.storeIndividualSampleClassified(sim_time,replication,ssize,popsize,mut,simid,classified_list)

pp.pprint(simrun_dimension_cache)



cg.dmb.build_random_partitions_all_dimensions(6,sim_param)




# TODO:  Are classifications data in the database, or code modules with names we refer to?


