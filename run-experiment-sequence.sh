#!/bin/sh

experiment=$1
conf=$2
echo "Running sequence of CTPy scripts for experiment $experiment with config: $conf"

python admin/initialize_experiment.py --experiment $experiment --debug 0
python simulations/neutral-kn-sweep.py --experiment $experiment --configuration $conf --debug 0 >& simulation.log
python analytics/subsample_individual_samples.py --experiment $experiment --configuration $conf --debug 0  >& subsampling.log
python analytics/classify_individual_samples.py  --experiment $experiment --configuration $conf --debug 0  >& classification.log
python analytics/calculate_persimrun_statistics.py  --experiment $experiment --configuration $conf --debug 0  >& postclass-stats.log




