"""
Global definitions for CTPy
"""

MAXALLELES = 1000000000
NUM_REPLICATES_FOR_RANDOM_DIMENSION_MODES = 15

# Classifications with 32 or 64 modes per dimension are rare in archaeological practice
# when classes are discrete/nominal categories, but we want to see scaling of
# observables, and we can imagine cases with random dimensions where we might
# have an ability to chop things into chunks but not understand how those map to underlying
# variation...

DIMENSION_PARTITIONS = [2,3,4,5,6,8,12,16,32]
MODETYPE_EVEN = str("EVEN")
MODETYPE_RANDOM = str('RANDOM')