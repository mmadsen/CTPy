"""
ctpy.strategies.conformism contains a variety of methods for implementing a 'conformist'
strategy for cultural transmission.  Each is implemented as a simuPOP PyParentsChooser
operator, which can then be used to define a custom mating scheme.  This allows one to
use the standard offspring generators to form the next generation, across subpopulations.

Some of the strategies are conditional, and thus have parameters that need to be set.  An
example would be the standard Bentley/Mesoudi/Lycett implementation of conformism, in which
with probability p, we choose the most frequent trait in the population (or subpopulation),
and with probability 1-p, we select a parent randomly.

"""

import simuPOP as sim

