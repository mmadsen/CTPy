# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/


import unittest
import ctpy.math as cpm
import pprint as pp
import math

class MathTest(unittest.TestCase):

    def test_expectedTimeStationarityHaploid(self):
        popsize = 1000
        mutation = 0.001
        theta = 2.0 * popsize * mutation

        val = (9.2 * popsize) / (theta + 1.0)
        expected = int(math.ceil(val / 1000)) * 1000
        print "expected stationary time: %s" % expected
        obs = cpm.expectedIAQuasiStationarityTimeHaploid(popsize,mutation)
        print "observed stationary time: %s" % obs
        self.assertEqual(expected,obs)

if __name__ == "__main__":
    unittest.main()
