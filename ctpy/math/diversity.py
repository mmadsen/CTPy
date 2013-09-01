# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the Apache Public License 2.0
#
# This module contains classes and functions for applying paradigmatic classifications
# to the trait spaces of CTPy/simuPOP simulations.
#

import logging as logger
from math import log



def diversity_shannon_entropy(freq_list):
    k = len(freq_list)
    sw = 0.0
    for i in range(0, k):
        sw += freq_list[i] * log(freq_list[i])
    return sw * -1.0

def diversity_iqv(freq_list, num_classes_possible):
    pass

def diversity_neiman_tf(freq_list, num_classes_possible):
    pass
