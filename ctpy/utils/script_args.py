# Copyright (c) $today.year.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Creative Commons-GNU General Public Llicense 2.0, as "non-commercial/sharealike".  You may use, modify, and distribute this software for non-commercial purposes, and you must distribute any modifications under the same license.  
#
# For detailed license terms, see:
# http://creativecommons.org/licenses/GPL/2.0/

import logging as log
import argparse

class ScriptArgs:
    debug = False
    experiment_name = "default"
    database_hostname = "localhost"
    database_port = "27017"

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--experiment", help="provide name for experiment, to be used as prefix for database collections")
        parser.add_argument("--debug", help="turn on debugging output")
        parser.add_argument("--dbhost", help="database hostname, defaults to localhost")
        parser.add_argument("--dbport", help="database port, defaults to 27017")

        args = parser.parse_args()
        if args.debug:
            self.debug = True

        if args.experiment:
            self.experiment_name = args.experiment

        if args.dbhost:
            self.database_hostname = args.dbhost

        if args.dbport:
            self.database_port = args.dbport



