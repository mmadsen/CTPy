CTPy
====

Cultural transmission models in python using simuPOP, SciPy, and NumPy.  Data storage is currently in
a MongoDB instance, which can be local or remote, if simulations are being run on multiple machines.

CTPy is a software layer on top of simuPOP by Bo Peng, currently version 1.X.  See
[http://simupop.sourceforge.net/](http://simupop.sourceforge.net/) for source code, license, and documentation.


## Directory Structure ##

analytics
:  python scripts which process simulation data from the database, and make entries into the database of their results.

ctpy
:  python modules and classes used in simulations and analytics

simulations
:  python scripts which run simuPOP simulations of cultural transmission models, logging samples to the database.

test
:  unit and functional test scripts


## Runtime Dependency ##

CTPy assumes that there is an instance of MongoDB to which it can log samples and statistical data.  The
init.py file in the ctpy/sampling directory contains the database initialization, so that remote connections
can be substituted for a local development server.  This may be more easily configurable in future releases.

CTPy uses the [Ming](http://merciless.sourceforge.net/index.html) object relational library to connect from Python to
MongoDB.


## Author ##

Mark E. Madsen
Copyright 2012-2013.  All rights reserved.  This software is made available under the Apache Software License (see
file LICENSE), which allows you to use the software for commercial or non-commercial purposes, but you must
attribute authorship, and derivatives must allow the user to find the original code and license.

mark@madsenlab.org
[Website and Lab Notebook](http://notebook.madsenlab.org)


