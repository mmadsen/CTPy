# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/

import logging as log
import ctpy
import ctpy.math.simulation_calculations as sc

log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')


log.info("Number of parameter combinations: %s", sc.compute_sim_param_combinations())
log.info("Number of network param combinations: %s", sc.compute_network_param_combinations())
log.info("Number of network realizations: %s", sc.compute_total_network_realizations())
log.info("Number of sim execution runs: %s", sc.compute_total_simulation_runs())
log.info("Number of sim replications: %s", sc.compute_total_simulation_replicates())


