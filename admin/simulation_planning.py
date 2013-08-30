#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

import logging as log
import ctpy.math.simulation_calculations as calc
import ctpy.utils as utils

simconfig = utils.CTPyConfiguration(None)

sc = calc.SimulationCalculations(simconfig)

log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

log.info("========== SINGLE POPULATION MODELS ==============")
log.info("Number of sim execution runs: %s", sc.compute_total_simulation_runs_simple())
log.info("Number of sim replications: %s", sc.compute_total_simulation_replicates_simple())
log.info("Number of replications (repl x ssize x simparam): %s", sc.compute_total_sample_size_replicates_simple())
log.info("Number of replications (repl x dimensionality x ssize x simparam): %s", sc.compute_total_replicates_ssize_dimensionality())
log.info("Total number of classifications: %s", sc.compute_total_classifications())
log.info("Total sample paths (repl x dimensionality x ssize x classification x simparams): %s","{:,}".format(sc.compute_total_replicates_ssize_dimensionality_classifications()))
log.info("Total sample paths (repl x dim x ssize x class x simparams x taduration): %s", "{:,}".format(sc.compute_total_sample_paths_ssize_dim_class_taduration()))
log.info("Number of samples per sample path per TA duration: %s", simconfig.NUM_SAMPLES_ANALYZED_PER_FINAL_SAMPLE_PATH)
log.info("    ")
log.info("TOTAL NUMBER OF FINAL SAMPLES FOR EACH SIMPLE MODEL WITH TA: %s", "{:,}".format(sc.compute_total_number_samples_simple_models()))
log.info("TOTAL NUMBER OF FINAL SAMPLES FOR EACH SIMPLE MODEL NO TA: %s","{:,}".format(sc.compute_total_number_samples_notimeavg_simple_models()))

log.info("======= END SINGLE POPULATION MODELS ======")
log.info("    ")
log.info("============= METAPOPULATION MODELS ===========")
log.info("Number of network param combinations: %s", sc.compute_network_param_combinations())
log.info("Number of network realizations: %s", sc.compute_total_network_realizations())
log.info("Number of sim execution runs for metapopulation models: %s", sc.compute_total_simulation_runs_metapopulation())
log.info("Number of sim replications for metapopulation models: %s", sc.compute_total_simulation_replicates_metapopulation())

log.info("----ANALYSIS OF METAPOP MODELS IS INCOMPLETE---------")

log.info("=========== END METAPOPULATION MODELS ===========")

