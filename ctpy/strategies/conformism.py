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

class ConformistMatingScheme(sim.HomoMating):
    """
    A homogeneous mating scheme which implements a variety of "conformist" transmission rules.
    """

    def __init__(self, numOffspring=1, sexMode=sim.RANDOM_SEX, globalConformismProbability=0.01, ops=sim.CloneGenoTransmitter(), subPopSize=[],
                 subPops=sim.ALL_AVAIL, weight=0):
        sim.HomoMating.__init__(self,
                                chooser = sim.PyParentsChooser(),
                                generator = sim.OffspringGenerator(ops, numOffspring, sexMode),
                                # incomplete
                                )

    def probSelectParentWithMostPopularTraits(pop, subpop):
        """
        Selects parents with the "most popular" traits, with probability
        """
        pass
