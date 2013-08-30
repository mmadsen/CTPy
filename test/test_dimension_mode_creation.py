# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public License 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/


import unittest
import ctpy.coarsegraining as cg
import ctpy.utils as utils
import pprint as pp
import logging as log

class DimensionModeCreationTest(unittest.TestCase):

    def setUp(self):
        self.config = utils.CTPyConfiguration(None)

    def test_random_creation(self):

        result_dict = cg.dmb.build_random_dimension(self.config,4)


if __name__ == "__main__":
    unittest.main()

