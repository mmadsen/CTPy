#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache License, Version 2.0.  See the file LICENSE for details
#

"""
Generates a parameter document (to STDOUT) for a given configuration file.  Allows a choice of
LaTeX and Markdown (Pandoc) formats.

"""


import logging as log
import argparse
import ctpy.utils as utils





def setup():
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument("--configuration", help="Configuration file for experiment", required=True)
    parser.add_argument("--experiment", help="provide name for experiment", required=True)
    parser.add_argument("--format", choices=['latex', 'pandoc'], help="Format for output ", required=True)
    parser.add_argument("--debug", help="turn on debugging output")


    args = parser.parse_args()

    if args.debug:
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    else:
        log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s')



####### main loop #######

if __name__ == "__main__":
    setup()
    simconfig = utils.CTPyConfiguration(args.configuration)


    if args.format == 'pandoc':
        print simconfig.to_pandoc_table(args.experiment)
    elif args.format == 'latex':
        print simconfig.to_latex_table(args.experiment)
    else:
        print "Unrecognized format: %s" % args.format
        exit(1)


    exit(0)








