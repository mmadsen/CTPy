# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public License 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/


import unittest
import ctpy.coarsegraining as cg
import pprint as pp
import logging as log

class DimensionModeCreationTest(unittest.TestCase):

    def test_random_creation(self):
        sim_param = {}
        sim_param["numloci"] = 3
        sim_param["maxalleles"] = 100000

        result_dict = cg.dmb.build_random_partitions_all_dimensions(4, sim_param)

if __name__ == "__main__":
    unittest.main()

