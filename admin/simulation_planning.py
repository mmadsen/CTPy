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

log.info("========== SINGLE POPULATION MODELS ==============")
log.info("Number of sim execution runs: %s", sc.compute_total_simulation_runs_simple())
log.info("Number of sim replications: %s", sc.compute_total_simulation_replicates_simple())
log.info("Number of replications (repl x ssize x simparam): %s", sc.compute_total_sample_size_replicates_simple())
log.info("Number of replications (repl x dimensionality x ssize x simparam): %s", sc.compute_total_replicates_ssize_dimensionality())
log.info("Total number of classifications: %s", sc.compute_total_classifications())
log.info("Total sample paths (repl x dimensionality x ssize x classification x simparams): %s",sc.compute_total_replicates_ssize_dimensionality_classifications())
log.info("Total sample paths (repl x dim x ssize x class x simparams x taduration): %s", sc.compute_total_sample_paths_ssize_dim_class_taduration())
log.info("Number of samples per sample path per TA duration: %s", ctpy.NUM_SAMPLES_ANALYZED_PER_FINAL_SAMPLE_PATH)
log.info("    ")
log.info("TOTAL NUMBER OF FINAL SAMPLES FOR EACH SIMPLE MODEL: %s", sc.compute_total_number_samples_simple_models() )
log.info("======= END SINGLE POPULATION MODELS ======")
log.info("    ")
log.info("============= METAPOPULATION MODELS ===========")
log.info("Number of network param combinations: %s", sc.compute_network_param_combinations())
log.info("Number of network realizations: %s", sc.compute_total_network_realizations())
log.info("Number of sim execution runs for metapopulation models: %s", sc.compute_total_simulation_runs_metapopulation())
log.info("Number of sim replications for metapopulation models: %s", sc.compute_total_simulation_replicates_metapopulation())


log.info("=========== END METAPOPULATION MODELS ===========")

