# Classification in Python #

April 2013
MEM

Brainstorming an efficient classification module for python and the **simuPOP** system.

## Possible Models ##

The main possibilities are:

1.  "Live" classification -- taking samples of individuals and coding their genotypes into classes as a _postOps_ step
1.  Post-processed classification -- take samples of individuals (not just genotype counts or frequencies), and post-process


## Difficulties With Variation Model ##

The **simuPOP** system has a couple of genotype representation models ("variation model") but the basic ones represent
units of variation (i.e., alleles, for simplicity, but you can interpret them as nucleotides, SNPs, etc) as integers at
a locus.  The default is to allow 256 allelic states, but with the "long" version of the modules, a very large number
of states are achievable.

The hard part with classification is that we want to specify a set of modes as "chopping up" the allelic state space,
in such a way that variation at stationarity is somewhat distributed across the classification, and isn't always (a)
concentrated into one class, or (b) evenly distributed across all classes with no empty classes.

The former would happen, for example, if the mutation model starts at the highest integer represented in the population,
and simply increments it, but the class definitions chop up the entire "long integer" range into modes.  For any
reasonable population size, and any reasonable length of simulation run, the "currently occupied" portion of the state
space is likely to be concentrated in one of the modes, since mutation is "adjacent" to existing variants.

The latter would happen if we tried to tweak the modes and the length of the situation so that we use only part of the
long integer range for modes, but we "get it wrong" and the occupied state space tends to overwhelm the "size" of the
classes we define.

The virtue of the **TransmissionFramework** implementation, which partitioned the unit interval, was that we could have
practically infinite variants, but we can easily predefine the partitions of the unit interval, and use either
uniform random doubles, or other distributions whose range could be clipped to the unit interval to generate novel
alleles.

So the big issue is how to do that in simuPOP.

### Possible Variation Model Solutions ###

1. Ensure that mutation is range-sensitive, instead