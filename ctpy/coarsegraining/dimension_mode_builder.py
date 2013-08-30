# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the Apache Public License 2.0

# Each function in this file returns a dict with dimensions as keys,
# and a dict of modes as values.  Each mode dict has two keys,
# "upper" and "lower" values.  These values are interpreted
# strictly as [lower, upper), so "adjacent" modes must have
# identical upper (and thus lower) values.
#
# In other words, a dimension looks like this:
#
# 1: {0: {'lower': 0.0,
#         'upper': 250000000.0},
#     1: {'lower': 250000000.0,
#         'upper': 500000000.0},
#     2: {'lower': 500000000.0,
#         'upper': 750000000.0},
#     3: {'lower': 750000000.0,
#         'upper': 1000000000.0}}
#

import random
import pprint as pp
import logging as log
import ctpy

log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')


def build_even_dimension(simconfig, num_modes):
    mode_boundaries = []
    mode_width = float(simconfig.MAXALLELES) / float(num_modes)
    lower_val = 0.0
    upper_val = 0.0
    for mode in range(0, num_modes):
        upper_val += mode_width
        mode_boundaries.append(dict(lower=lower_val, upper=upper_val))
        lower_val = upper_val
    log.debug("boundaries: %s", mode_boundaries)
    return mode_boundaries


def build_random_dimension(simconfig, num_modes):
    iboundaries = []
    mode_boundaries = []
    num_internal_boundaries = num_modes - 1
    for i in range(0, num_internal_boundaries):
        random_variate = random.random()
        iboundaries.append(random_variate)

    # add the final upper boundary
    iboundaries.append(1.0)

    lower_val = 0.0
    upper_val = 0.0
    iboundaries.sort()

    for mode in range(0, num_modes):
        lower_val = lower_val * simconfig.MAXALLELES
        upper_val = iboundaries[mode] * simconfig.MAXALLELES
        mode_boundaries.append(dict(lower=lower_val, upper=upper_val))
        lower_val = iboundaries[mode]

    log.debug("boundaries: %s", mode_boundaries)
    return mode_boundaries



# # TODO:  needs to deal with cases where maxalleles % num_modes leaves a remainder...
#
#
# def build_even_partitions_all_dimensions(num_modes, sim_param):
#     """
#
#
#     :param num_modes:
#     :param sim_param:
#     :return:
#     """
#     dimensions = {}
#
#     # to start, we partition into quarters for each locus (dimension)
#     mode_width = sim_param["maxalleles"] / num_modes
#
#     for dimension in range(0, sim_param["numloci"]):
#         mode_boundaries_dict = {}
#         lower_val = 0.0
#         upper_val = 0.0
#         for mode in range(0,num_modes):
#             upper_val += mode_width
#             mode_boundaries_dict[mode] = dict(lower=lower_val, upper=upper_val)
#             lower_val = upper_val
#             dimensions[dimension] = mode_boundaries_dict
#     return dimensions
#
#
# def build_random_partitions_all_dimensions(num_modes, sim_param):
#     """
#     For k desired modes, generate random mode boundaries within maxalleles.
#     Algorithm generates k-1 "internal" boundaries on the unit interval [0,1]
#     and then scales maxalleles by the unit interval partitions.  Upper
#     and lower internal boundaries are equivalent, since they will be
#     interpreted with open/closed interval semantics.
#
#
#     :param num_modes:
#     :param sim_param:
#     :return: dict of dimension-specific dicts, within each of which a mode maps to a dict of upper and lower boundaries
#     """
#     dimensions = {}
#     num_internal_boundaries = num_modes - 1
#
#     for dimension in range(0, sim_param["numloci"]):
#         tempboundary = list()
#         mode_boundaries_dict = {}
#         maxalleles = sim_param["maxalleles"]
#
#         for i in range(0, num_internal_boundaries):
#             random_variate = random.random()
#             tempboundary.append(random_variate)
#
#         # add the final upper boundary
#         tempboundary.append(1.0)
#
#         lower_val = 0.0
#         upper_val = 0.0
#         tempboundary.sort()
#
#         for mode in range(0, num_modes):
#             lower_val = int(lower_val * maxalleles)
#             upper_val = int(tempboundary[mode] * maxalleles)
#             mode_boundaries_dict[mode] = dict(lower=lower_val, upper=upper_val)
#             lower_val = tempboundary[mode]
#
#         dimensions[dimension] = mode_boundaries_dict
#         # TODO:  missing logic for scaling to maxalleles, need to debug this first...
#     return dimensions
#
#
# if __name__ == "__main__":
#     sim_param = {}
#     sim_param["numloci"] = 3
#     sim_param["maxalleles"] = 100000000
#
#
#     print "Testing random partitions for 3 dimensions, 4 modes"
#     result_dict = build_random_partitions_all_dimensions(4, sim_param)
#     pp.pprint(result_dict)
#
#     print "Testing even partitions for 3 dimensions, 4 modes"
#     result_dict = build_even_partitions_all_dimensions(4, sim_param)
#     pp.pprint(result_dict)