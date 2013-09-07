# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/

import unittest
import ctpy.coarsegraining as cg
import ctpy.utils as utils


class TestInnovationIntervalStats(unittest.TestCase):

    def setUp(self):
        self.config = utils.CTPyConfiguration(None)
        self.test_data = {
            '0-1-0' : 2500,
            '0-0-0' : 1000,
            '0-0-1' : 1500,
            '1-0-0' : 3500,
            '1-1-0' : 500
        }

        self.expected_intervals = [500,500,1000,1000]
        self.expected_mean_interval = 750.00
        self.expected_sd_interval = 288.6751
        self.epsilon = 0.01
        simrun_stats = cg.ClassificationStatsPerSimrun(self.config)

        self.stats = simrun_stats._innovation_interval_stats(self.test_data)


    def test_mean(self):
        self.assertAlmostEqual(self.expected_mean_interval, self.stats[0], delta=self.epsilon)

    def test_sd(self):
        self.assertAlmostEqual(self.expected_sd_interval, self.stats[1], delta=self.epsilon)



if __name__ == "__main__":
    unittest.main()
