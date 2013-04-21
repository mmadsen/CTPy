# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/

# this module exists so that we can do logging functions which are usable as PyOperators in simuPOP.


import logging

__author__ = 'mark'


def logGenerationCount(pop, param):
        gen = pop.dvars().gen
        logging.info("Generation: %s", gen)
        return True

