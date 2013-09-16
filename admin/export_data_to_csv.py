#!/usr/bin/env python

# Copyright (c) 2013.  Mark E. Madsen <mark@madsenlab.org>
#
# This work is licensed under the terms of the Apache Software License, Version 2.0.  See the file LICENSE for details.

import ctpy.data as data
import ctpy.utils as utils
import ming
import os
import logging as log
import tempfile


# Prototype:
# mongoexport --db f-test_samples_postclassification --collection pergeneration_stats_postclassification --csv --out pgstats.csv --fieldFile fieldlist

mongoexport = "/usr/local/mongodb/bin/mongoexport "



## setup

def setup():
    global sargs, config, simconfig
    sargs = utils.ScriptArgs()
    if sargs.debug:
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
    else:
        log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s: %(message)s')

    simconfig = utils.CTPyConfiguration(sargs.configuration)

    log.debug("experiment name: %s", sargs.experiment_name)
    data.set_experiment_name(sargs.experiment_name)
    data.set_database_hostname(sargs.database_hostname)
    data.set_database_port(sargs.database_port)
    #### main program ####
    log.info("EXPORT DATA TO CSV - Experiment: %s", sargs.experiment_name)
    config = data.getMingConfiguration()
    ming.configure(**config)


def export_collection_to_csv(database, collection_name, fieldlist):

    outputFileName = "data_"
    outputFileName += collection_name
    outputFileName += ".csv"

    fieldFile = tempfile.NamedTemporaryFile(mode="w+t",suffix=".txt",dir="/tmp",delete=False)
    fieldFileName = fieldFile.name
    log.debug("Saving field list to %s", fieldFileName)

    for field in fieldlist:
        fieldFile.write(field)
        fieldFile.write('\n')

    fieldFile.flush()

    args = []
    args.append(mongoexport)
    args.append("--db")
    args.append(database)
    args.append("--collection")
    args.append(collection_name)
    args.append("--csv")
    args.append("--fieldFile")
    args.append(fieldFileName)
    args.append("--out")
    args.append(outputFileName)

    log.debug("args: %s", args)
    retcode = os.system(" ".join(args))
    log.debug("return code: %s", retcode)




if __name__ == "__main__":
    setup()


    export_collection_to_csv(data.pergeneration_stats_postclassification._get_collection_id(),
                             "pergeneration_stats_postclassification",
                             data.pergeneration_stats_postclassification.columns_to_export_for_analysis())















