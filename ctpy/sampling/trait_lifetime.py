# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/
"""
.. module:: trait_lifetime
    :platform: Unix, Windows
    :synopsis: Classes and data objects for tracking the lifetime of alleles/traits, and storing this in the database.

.. moduleauthor:: Mark E. Madsen <mark@madsenlab.org>

Trait (allele) lifetimes

"""

import logging
from ming import Session, Field, schema
from ming.declarative import Document
import simuPOP as sim


def _get_dataobj_id():
    """
        Returns the short handle used for this data object in Ming configuration
    """
    return 'traitlifetime'



class TraitLifetimeCache:
    """
    Caches the starting generation of each newly mutated allele.  Constructor takes as
     argument the number of loci and initial alleles, since these begin their lifetime at gen 0.
    """
    def __init__(self, numloci, numalleles):
        cache = {}
        for locus in range(numloci):
            cache[locus] = {}
            for n in range(numalleles):
                cache[locus][n] = 0

    def cacheNewAllele(self, pop, locus, ):
        """Given a simuPOP population, checks for newly mutated alleles and records
            the generation of their first occurrence.  Intended to be used as a
            PyOperator in postOps for evolve()
        """

        return True




class TraitLifetimeRecord(Document):

    class __mongometa__:
        session = Session.by_name(_get_dataobj_id())
        name = 'trait_lifetime'

    _id = Field(schema.ObjectId)
    replication = Field(int)
    locus = Field(int)
    population_size = Field(int)
    mutation_rate = Field(float)
    simulation_run_id = Field(str)
    allele = Field(int)
    lifetime = Field(int)








