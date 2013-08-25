#!/usr/bin/env python
# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/


import itertools
import logging as log
import ctpy.utils as utils

log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s')

sargs = utils.ScriptArgs()
if sargs.debug:
    log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
else:
    log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s')

simconfig = utils.CTPyConfiguration(sargs.configuration)
mutationrates = simconfig.INNOVATION_RATES_STUDIED
populationsizes = simconfig.POPULATION_SIZES_STUDIED

state_space = [
    mutationrates,
    populationsizes
]

print "popsize\tmutation\ttheta"
for param_combination in itertools.product(*state_space):
    mut = param_combination[0]
    popsize = param_combination[1]

    theta = 2 * mut * popsize
    log.info("%d\t%f\t%f", popsize, mut, theta)



