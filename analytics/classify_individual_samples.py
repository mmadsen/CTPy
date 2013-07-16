# Copyright (c) 2013  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

#
#
#
#

import ctpy.data as data
import ctpy.coarsegraining as cg
import ming
import logging
import pprint as pp

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

config = data.getMingConfiguration()
ming.configure(**config)

