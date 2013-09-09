#!/usr/bin/env python
# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache License, Version 2.0.  See the file LICENSE for details
#

"""
modify_experiment_tracking.py

CLI tool for editing the experiment_tracking database, allowing one to "clean" out a collection, mark the
processing stage as incomplete, and re-run a script.  Or to make edits to description or date fields.

Main examples:

modify_experiment_tracking.py --experiment test --undo --tag classification

This example sets the classification_complete stage of the "test" experiment to False, allowing the classification
script to be re-run.  This script does NOT remove documents from the MongoDB collection; that's your job as administrator.

modify_experiment_tracking.py --experiment test --update --tag description --value "Test experiment done by MEM Sept 2013"

This example simply edits the "description" field of the "test" experiment, setting its value to the string given.

Date fields will be included in a future edit, to enable the second example to be used to twiddle dates (if that's needed).

"""


import logging as log
import argparse
import ctpy.data as data
import ming




def setup():
    global args
    permitted_stage_tags = data.get_experiment_stage_tags()

    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", help="provide name for experiment", required=True)
    parser.add_argument("--debug", help="turn on debugging output")
    parser.add_argument("--dbhost", help="database hostname, defaults to localhost", default="localhost")
    parser.add_argument("--dbport", help="database port, defaults to 27017", default="27017")
    parser.add_argument("--tag", choices=permitted_stage_tags, help="tag for experiment tracking field to update ", required=True)
    parser.add_argument("--undo", help="Allow a stage to be re-run, by setting its completion tag to False", action="store_true")
    parser.add_argument("--update", help="Update the value of a experiment tracking field, using --value for the new value", action="store_true")
    parser.add_argument("--value", help="New value for the tag, in an --update")

    args = parser.parse_args()

    if args.debug:
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    else:
        log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    log.debug("experiment name: %s", args.experiment)
    data.set_experiment_name(args.experiment)
    data.set_database_hostname(args.dbhost)
    data.set_database_port(args.dbport)
    config = data.getMingConfiguration()
    ming.configure(**config)


####### main loop #######

if __name__ == "__main__":
    setup()



    if args.undo == True:
        data.update_field_by_stage_tag(args.experiment, args.tag, False)
        print "Experiment Tracking updated for experiment %s:  stage %s reset, can be run again" % (args.experiment, args.tag)
    elif args.update == True:
        data.update_field_by_stage_tag(args.experiment, args.tag, args.value)
    else:
        print ""








