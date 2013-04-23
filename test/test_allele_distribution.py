# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/

import unittest
from ctpy import utils
import pprint as pp

class AlleleDistributionTest(unittest.TestCase):

    def test_uniform_10alleles(self):
        expected_10 = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]
        obs_10 = utils.constructUniformAllelicDistribution(10)
        self.assertEqual(expected_10, obs_10, "wrong array of allele frequencies")

    def test_uniform_5alleles(self):
        expected_5 = [0.2, 0.2, 0.2, 0.2, 0.2]
        obs_5 = utils.constructUniformAllelicDistribution(5)
        self.assertEqual(expected_5, obs_5, "wrong array of allele frequencies")

    def test_uniform_3alleles(self):
        expected_3 = [.33333333333333337, .33333333333333337, .33333333333333337]
        obs_3 = utils.constructUniformAllelicDistribution(3)
        self.assertEquals(expected_3, obs_3)


if __name__ == "__main__":
    unittest.main()


