# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the Apache Public License 2.0
#
# This module contains classes and functions for applying paradigmatic classifications
# to the trait spaces of CTPy/simuPOP simulations.
#

import ctpy.data as data
from bson.objectid import ObjectId
import ming
import logging as log


class ClassIdentifier:
    def __init__(self, classification):
        self.classification = classification
        self.class_id = classification["_id"]
        self.dimensionality = classification["dimensions"]
        self.coarseness = classification["mean_coarseness"]
        self.class_type = classification["classification_type"]
        log.debug("initializing ClassIdentifier for classification %s", self.class_id)



