# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/

import unittest
import ctpy.utils as utils
import os
import tempfile

class ConfigurationTest(unittest.TestCase):
    filename = "test"

    def setUp(self):
        self.tf = tempfile.NamedTemporaryFile(dir="/tmp", delete=False)
        self.tf.write("""
        {
    "MODETYPE_EVEN" : "EVEN",
    "MODETYPE_RANDOM" : "RANDOM",
    "MAXALLELES" : 100,
    "NUM_REPLICATES_FOR_RANDOM_DIMENSION_MODES" : 10,
    "DIMENSION_PARTITIONS" : [2,3,4,8,16,32],
    "DIMENSIONS_STUDIED" : [2,3,4,6,8],
    "INNOVATION_RATES_STUDIED" : [0.0001,0.00025,0.0005,0.001,0.0025,0.005,0.01,0.025],
    "SIMULATION_LENGTH_AFTER_STATIONARITY" : 10000,
    "TIME_AVERAGING_DURATIONS_STUDIED" : [1000,500,250,125,63,32,16,8,1],
    "NUM_SAMPLES_ANALYZED_PER_FINAL_SAMPLE_PATH" : 10,
    "INITIAL_TRAIT_NUMBER" : 10,
    "SAMPLING_INTERVAL" : 1,
    "REPLICATIONS_PER_PARAM_SET" : 1000,
    "SAMPLE_SIZES_STUDIED" : [25,50,100,200],
    "POPULATION_SIZES_STUDIED" : [500,1000,2500,5000],
    "DEME_NUMBERS_STUDIED" : [32],
    "NUMBER_RANDOM_MIGRATION_MATRICES_STUDIED" : 10,
    "DENSITY_SMALL_WORLD_LINKS_STUDIED" : [0.0,0.1,0.25,0.5,0.75],
    "CLUSTERING_COEFFICIENTS_STUDIED" : [0.0,0.1,0.25,0.5,0.75]
}
        """)
        self.tf.flush()

    def tearDown(self):
        os.remove(self.tf.name)


    def test_configuration(self):


        print "tempfile: %s" % self.tf.name

        config = utils.CTPyConfiguration(self.tf.name)
        print "configured MAXALLELES: %s" % config.MAXALLELES
        self.assertEqual(100, config.MAXALLELES, "Config file value does not match")



    def test_latex_output(self):

        config = utils.CTPyConfiguration(self.tf.name)
        table = config.to_latex_table("test")

        print table

    def test_pandoc_output(self):

        config = utils.CTPyConfiguration(self.tf.name)
        table = config.to_pandoc_table("test")

        print table

if __name__ == "__main__":
    unittest.main()
